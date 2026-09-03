"""
Kouki Shop - AliExpress Price Bot
==================================
Telegram bot that takes an AliExpress product link, fetches product data
(price, images, rating, shipping to Algeria) and returns the final
customer price in DZD after buffer + shipping + Kouki Shop commission.

Run with:
    python bot.py

No environment variables are required. All credentials are hardcoded
below - replace the placeholders with your real values.
"""

import re
import time
import json
import logging
import hashlib
import threading
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from cachetools import TTLCache
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

try:
    from aliexpress_api import AliexpressApi, models as ali_models
    HAS_ALIEXPRESS_LIB = True
except Exception:  # library not installed / import failure -> fall back to raw API calls only
    HAS_ALIEXPRESS_LIB = False

# ---------------------------------------------------------------------------
# CREDENTIALS - HARDCODED ON PURPOSE (no Render environment variables)
# Replace these placeholders with your real values before deploying.
# ---------------------------------------------------------------------------

BOT_TOKEN = "8735963784:AAHpOSCihKDLNSm08qtQw8_4hAJ5yy689f8"

ALIEXPRESS_APP_KEY = "515874"
ALIEXPRESS_APP_SECRET = "jSWlobcAFLVp9Jo4QEjcbqXpbQBk4JRQ"
ALIEXPRESS_TRACKING_ID = "130740"

# PayPal - optional, only used if you wire up paid orders. Leave the
# placeholders if you don't use PayPal yet.
PAYPAL_CLIENT_ID = "YOUR_PAYPAL_CLIENT_ID"
PAYPAL_CLIENT_SECRET = "YOUR_PAYPAL_CLIENT_SECRET"
PAYPAL_MODE = "live"  # "sandbox" or "live"

# ---------------------------------------------------------------------------
# PRICING CONFIG
# ---------------------------------------------------------------------------

USD_TO_DZD_RATE = 260.0          # 1 USD = 260 DZD
PRODUCT_BUFFER_RATE = 0.14       # 14% buffer, applied to PRODUCT PRICE ONLY

# Kouki Shop commission - flat DZD amount, tweak or turn into a
# percentage-based rule if you prefer.
COMMISSION_FLAT_DZD = 300.0
COMMISSION_PERCENT = 0.0         # extra % commission on subtotal_dzd if wanted

SHIPPING_DESTINATION_COUNTRY = "DZ"  # Algeria

CACHE_TTL_SECONDS = 15 * 60      # 15 minutes

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("kouki_shop_bot")

# ---------------------------------------------------------------------------
# CACHE (short TTL - prices/shipping change often)
# ---------------------------------------------------------------------------

product_cache = TTLCache(maxsize=500, ttl=CACHE_TTL_SECONDS)
shipping_cache = TTLCache(maxsize=500, ttl=CACHE_TTL_SECONDS)

# ---------------------------------------------------------------------------
# ALIEXPRESS LINK DETECTION
# ---------------------------------------------------------------------------

ALIEXPRESS_URL_REGEX = re.compile(
    r"(https?://(?:[\w.-]*\.)?aliexpress\.(?:com|us|ru)[^\s]*)",
    re.IGNORECASE,
)
PRODUCT_ID_REGEX = re.compile(r"/item/(?:.*?)?(\d+)\.html")


def extract_aliexpress_links(text: str):
    return ALIEXPRESS_URL_REGEX.findall(text or "")


def resolve_short_link(url: str) -> str:
    """AliExpress share links (s.click.aliexpress.com / a.aliexpress.com) are
    shortened redirects. Follow them to get the real product URL."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10)
        if resp.url:
            return resp.url
    except requests.RequestException:
        try:
            resp = requests.get(url, allow_redirects=True, timeout=10)
            if resp.url:
                return resp.url
        except requests.RequestException as e:
            logger.warning("Could not resolve short link %s: %s", url, e)
    return url


def extract_product_id(url: str):
    resolved = url
    if "item" not in url:
        resolved = resolve_short_link(url)

    match = PRODUCT_ID_REGEX.search(resolved)
    if match:
        return match.group(1), resolved

    # fallback: some links carry the id as a query param
    parsed = urlparse(resolved)
    qs = parse_qs(parsed.query)
    for key in ("productId", "product_id", "id"):
        if key in qs and qs[key][0].isdigit():
            return qs[key][0], resolved

    # last resort: any long digit sequence in the path
    digits = re.findall(r"(\d{6,})", resolved)
    if digits:
        return digits[0], resolved

    return None, resolved


# ---------------------------------------------------------------------------
# RAW ALIEXPRESS OPEN PLATFORM SIGNED REQUEST
# (used for endpoints the python-aliexpress-api wrapper doesn't expose,
# e.g. shipping/freight lookups)
# ---------------------------------------------------------------------------

ALIEXPRESS_GATEWAY = "https://api-sg.aliexpress.com/sync"


def _sign_params(params: dict, secret: str) -> str:
    sorted_keys = sorted(params.keys())
    base_string = secret + "".join(f"{k}{params[k]}" for k in sorted_keys) + secret
    return hashlib.md5(base_string.encode("utf-8")).hexdigest().upper()


def aliexpress_api_call(method: str, extra_params: dict, timeout: int = 12):
    """Generic signed call to the AliExpress Open Platform gateway."""
    params = {
        "app_key": ALIEXPRESS_APP_KEY,
        "method": method,
        "sign_method": "md5",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "v": "2.0",
        "format": "json",
    }
    params.update(extra_params)
    params["sign"] = _sign_params(params, ALIEXPRESS_APP_SECRET)

    try:
        resp = requests.get(ALIEXPRESS_GATEWAY, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logger.warning("AliExpress API call failed (%s): %s", method, e)
        return None
    except json.JSONDecodeError:
        logger.warning("AliExpress API returned non-JSON response for %s", method)
        return None


def fetch_shipping_to_algeria(product_id: str, sku_id: str = None):
    """
    Attempt to get a real numeric shipping cost (USD) to Algeria for this
    product/SKU. Returns a tuple:
        (shipping_usd: float | None, status: "known" | "free" | "unknown")

    We never invent a shipping value. If the API doesn't give us a reliable
    number, status is "unknown" and the caller must display the
    "not calculated - verified at checkout" message.
    """
    cache_key = f"{product_id}:{sku_id or 'default'}"
    if cache_key in shipping_cache:
        return shipping_cache[cache_key]

    result = (None, "unknown")

    # Freight/logistics calculation endpoint. Exact param names can differ
    # slightly by account/permission tier - adjust `logistics_params` to
    # match what your AliExpress Open Platform app is authorized for.
    logistics_params = {
        "product_id": product_id,
        "country_code": SHIPPING_DESTINATION_COUNTRY,
        "ship_to_country": SHIPPING_DESTINATION_COUNTRY,
        "target_currency": "USD",
        "quantity": 1,
    }
    if sku_id:
        logistics_params["sku_id"] = sku_id

    data = aliexpress_api_call(
        "aliexpress.logistics.buyer.freight.calculate", logistics_params
    )

    if data:
        try:
            # Response shape varies; walk it defensively instead of
            # assuming one fixed structure.
            flat = json.dumps(data)
            # look for an explicit freight/shipping amount field
            freight_match = re.search(
                r'"(?:freight_amount|shipping_fee|freight_fee)"\s*:\s*"?([0-9]+\.?[0-9]*)"?',
                flat,
            )
            if freight_match:
                shipping_usd = float(freight_match.group(1))
                result = (shipping_usd, "known")
            elif '"free_shipping":true' in flat.replace(" ", ""):
                result = (0.0, "free")
        except (ValueError, TypeError) as e:
            logger.warning("Could not parse shipping response: %s", e)

    shipping_cache[cache_key] = result
    return result


# ---------------------------------------------------------------------------
# ALIEXPRESS PRODUCT LOOKUP
# ---------------------------------------------------------------------------

def get_aliexpress_client():
    if not HAS_ALIEXPRESS_LIB:
        return None
    try:
        return AliexpressApi(
            key=ALIEXPRESS_APP_KEY,
            secret=ALIEXPRESS_APP_SECRET,
            language=ali_models.Language.EN,
            currency=ali_models.Currency.USD,
            tracking_id=ALIEXPRESS_TRACKING_ID,
        )
    except Exception as e:
        logger.error("Failed to init AliexpressApi client: %s", e)
        return None


_aliexpress_client = get_aliexpress_client()


def fetch_product_details(product_id: str):
    """Returns a dict with product info, or None if it could not be fetched."""
    if product_id in product_cache:
        return product_cache[product_id]

    product_info = None

    if _aliexpress_client:
        try:
            products = _aliexpress_client.get_products(product_id)
            if products:
                p = products[0]
                product_info = {
                    "product_id": product_id,
                    "title": getattr(p, "product_title", "AliExpress Product"),
                    "price_usd": float(getattr(p, "target_sale_price", None) or getattr(p, "sale_price", 0) or 0),
                    "original_price_usd": float(getattr(p, "target_original_price", None) or getattr(p, "original_price", 0) or 0),
                    "discount": getattr(p, "discount", None),
                    "rating": getattr(p, "evaluate_rate", None),
                    "orders": getattr(p, "lastest_volume", None) or getattr(p, "volume", None),
                    "image_url": getattr(p, "product_main_image_url", None),
                    "affiliate_link": getattr(p, "promotion_link", None) or getattr(p, "product_detail_url", None),
                    "sku_id": None,
                }
        except Exception as e:
            logger.warning("get_products failed for %s: %s", product_id, e)

    # Fallback to a raw signed call if the wrapper library is unavailable
    # or returned nothing.
    if product_info is None:
        data = aliexpress_api_call(
            "aliexpress.affiliate.productdetail.get",
            {
                "product_ids": product_id,
                "target_currency": "USD",
                "target_language": "EN",
                "tracking_id": ALIEXPRESS_TRACKING_ID,
                "ship_to_country": SHIPPING_DESTINATION_COUNTRY,
                "fields": "product_id,product_title,target_sale_price,target_original_price,"
                          "product_main_image_url,promotion_link,evaluate_rate,lastest_volume",
            },
        )
        try:
            result = data.get("aliexpress_affiliate_productdetail_get_response", {})
            resp = result.get("resp_result", {}).get("result", {})
            items = resp.get("products", {}).get("product", [])
            if items:
                p = items[0]
                product_info = {
                    "product_id": product_id,
                    "title": p.get("product_title", "AliExpress Product"),
                    "price_usd": float(p.get("target_sale_price", 0) or 0),
                    "original_price_usd": float(p.get("target_original_price", 0) or 0),
                    "discount": p.get("discount"),
                    "rating": p.get("evaluate_rate"),
                    "orders": p.get("lastest_volume"),
                    "image_url": p.get("product_main_image_url"),
                    "affiliate_link": p.get("promotion_link"),
                    "sku_id": None,
                }
        except (AttributeError, KeyError, TypeError) as e:
            logger.warning("Raw product detail parse failed for %s: %s", product_id, e)

    if product_info:
        product_cache[product_id] = product_info

    return product_info


# ---------------------------------------------------------------------------
# PRICING ENGINE
# ---------------------------------------------------------------------------

def calculate_final_price(product_price_usd: float, shipping_usd: float):
    """
    PRODUCT PRICE
    + 14% BUFFER            (buffer applies to product price ONLY)
    + SHIPPING TO ALGERIA
    + KOUKI SHOP COMMISSION
    = FINAL CUSTOMER PRICE

    Returns a dict with every intermediate value so the caller can display
    a full breakdown.
    """
    buffer_amount_usd = product_price_usd * PRODUCT_BUFFER_RATE
    buffered_product_price_usd = product_price_usd * (1 + PRODUCT_BUFFER_RATE)

    subtotal_usd = buffered_product_price_usd + shipping_usd
    subtotal_dzd = subtotal_usd * USD_TO_DZD_RATE

    commission_dzd = COMMISSION_FLAT_DZD + (subtotal_dzd * COMMISSION_PERCENT)

    final_price_dzd = subtotal_dzd + commission_dzd

    return {
        "product_price_usd": round(product_price_usd, 2),
        "buffer_amount_usd": round(buffer_amount_usd, 2),
        "buffered_product_price_usd": round(buffered_product_price_usd, 2),
        "shipping_usd": round(shipping_usd, 2),
        "subtotal_usd": round(subtotal_usd, 2),
        "subtotal_dzd": round(subtotal_dzd, 2),
        "commission_dzd": round(commission_dzd, 2),
        "final_price_dzd": round(final_price_dzd, 2),
    }


def suggested_resale_price_dzd(final_price_dzd: float, markup: float = 0.15):
    return round(final_price_dzd * (1 + markup), 2)


# ---------------------------------------------------------------------------
# MESSAGE FORMATTING (Arabic UI, preserved style)
# ---------------------------------------------------------------------------

def format_shipping_line(shipping_usd, shipping_status: str):
    if shipping_status == "free":
        return "🚚 الشحن إلى الجزائر: مجاني"
    if shipping_status == "known" and shipping_usd is not None:
        return f"🚚 الشحن إلى الجزائر: +${shipping_usd:.2f}"
    return "🚚 الشحن إلى الجزائر: غير محسوب — يتحقق عند الدفع"


def format_product_message(product: dict, pricing: dict, shipping_status: str):
    lines = []
    lines.append(f"🛍️ <b>{product.get('title', 'منتج AliExpress')}</b>")
    lines.append("")
    lines.append(f"🛒 سعر المنتج: ${pricing['product_price_usd']:.2f}")
    lines.append(f"📈 Buffer 14%: +${pricing['buffer_amount_usd']:.2f}")
    lines.append(format_shipping_line(pricing["shipping_usd"] if shipping_status != "unknown" else None, shipping_status))
    lines.append(f"💵 السعر قبل العمولة: ${pricing['subtotal_usd']:.2f}")
    lines.append(f"🏷️ عمولة Kouki Shop: {pricing['commission_dzd']:.0f} DZD")
    lines.append(f"💰 السعر النهائي: {pricing['final_price_dzd']:.0f} DZD")

    if product.get("rating"):
        lines.append("")
        lines.append(f"⭐ التقييم: {product['rating']}")
    if product.get("orders"):
        lines.append(f"📦 عدد الطلبات: {product['orders']}")
    if product.get("discount"):
        lines.append(f"🔥 الخصم: {product['discount']}")

    resale = suggested_resale_price_dzd(pricing["final_price_dzd"])
    lines.append("")
    lines.append(f"💡 سعر إعادة البيع المقترح: {resale:.0f} DZD")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# TELEGRAM HANDLERS
# ---------------------------------------------------------------------------

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في Kouki Shop!\n\n"
        "أرسل رابط منتج من AliExpress وسأقوم بحساب السعر النهائي بالدينار الجزائري "
        "مع الشحن والعمولة."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل رابط منتج AliExpress (رابط كامل أو مختصر) وسأرد عليك بالتفاصيل والسعر النهائي."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    links = extract_aliexpress_links(text)

    if not links:
        return  # not an AliExpress link, ignore silently

    for link in links:
        await process_link(update, link)


async def process_link(update: Update, link: str):
    status_msg = await update.message.reply_text("🔎 جاري تحليل المنتج ...")

    product_id, resolved_url = extract_product_id(link)
    if not product_id:
        await status_msg.edit_text("⚠️ لم أتمكن من التعرف على المنتج من هذا الرابط.")
        return

    product = fetch_product_details(product_id)
    if not product or not product.get("price_usd"):
        await status_msg.edit_text(
            "⚠️ تعذر جلب بيانات هذا المنتج حالياً (قد يكون رابط غير صالح أو مشكلة مؤقتة في AliExpress API)."
        )
        return

    shipping_usd, shipping_status = fetch_shipping_to_algeria(product_id, product.get("sku_id"))

    pricing = calculate_final_price(
        product_price_usd=product["price_usd"],
        shipping_usd=shipping_usd if shipping_status in ("known", "free") else 0.0,
    )

    message_text = format_product_message(product, pricing, shipping_status)

    keyboard = None
    if product.get("affiliate_link"):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🛒 اشترِ الآن", url=product["affiliate_link"])]]
        )

    try:
        if product.get("image_url"):
            await update.message.reply_photo(
                photo=product["image_url"],
                caption=message_text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )
            await status_msg.delete()
        else:
            await status_msg.edit_text(message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    except Exception as e:
        logger.warning("Failed to send photo, falling back to text: %s", e)
        await status_msg.edit_text(message_text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Update %s caused error: %s", update, context.error)


# ---------------------------------------------------------------------------
# OPTIONAL: FASTAPI HEALTH ENDPOINT (Render web service compatibility)
# Runs in a background thread alongside the polling bot so Render's health
# checks succeed even though the bot itself uses long-polling.
# ---------------------------------------------------------------------------

def start_health_server():
    try:
        from fastapi import FastAPI
        import uvicorn

        app = FastAPI()

        @app.get("/")
        def health():
            return {"status": "ok", "service": "kouki-shop-bot", "time": datetime.utcnow().isoformat()}

        def run():
            uvicorn.run(app, host="0.0.0.0", port=10000, log_level="warning")

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        logger.info("Health check server started on port 10000")
    except Exception as e:
        logger.warning("Could not start health server (fastapi/uvicorn missing?): %s", e)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    if not BOT_TOKEN or BOT_TOKEN.startswith("YOUR_"):
        raise RuntimeError("BOT_TOKEN is not set. Edit bot.py and put your real Telegram bot token.")

    if not ALIEXPRESS_APP_KEY or ALIEXPRESS_APP_KEY.startswith("YOUR_"):
        logger.warning("AliExpress APP_KEY looks like a placeholder - product lookups will fail.")

    start_health_server()

    application: Application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    logger.info("Kouki Shop bot starting (polling mode) ...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
