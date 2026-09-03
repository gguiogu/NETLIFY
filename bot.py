import asyncio
import aiohttp
import re
import time
import io
import base64
import os
import logging
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs, unquote

from PIL import Image, ImageDraw, ImageFont

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from aliexpress_api import AliexpressApi, models


# ============================================================
# ⚙️ CONFIGURATION — NO ENVIRONMENT VARIABLES
# ============================================================
# Put your credentials directly below.
# Do NOT share this file publicly after adding your secrets.


TOKEN = "8735963784:AAHpOSCihKDLNSm08qtQw8_4hAJ5yy689f8"
APP_KEY = "515874"
APP_SECRET = "jSWlobcAFLVp9Jo4QEjcbqXpbQBk4JRQ"
TRACKING_ID = '130740'

# Fixed Kouki Shop pricing settings
USD_TO_DZD = 260.0
CHECKOUT_BUFFER = 1.14
MAX_CHECKOUT_BUFFER = 1.20
CACHE_TTL = 900
PORT = 8000
RESELLER_MARKUP = 1.30

# Destination country for shipping lookup
SHIP_TO_COUNTRY = "DZ"

# Shipping tax parameter used by the shipping lookup.
SHIPPING_TAX_RATE = "0"

FACEBOOK_URL = "https://www.facebook.com/XBHTHAGOAT/"

# ============================================================
# 📝 LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("kouki-shop-bot")


# ============================================================
# 🔐 STARTUP VALIDATION
# ============================================================

if not TOKEN or TOKEN.startswith("PASTE_YOUR_"):
    logger.warning("BOT_TOKEN is not configured in bot.py.")

if (
    not APP_KEY or APP_KEY.startswith("PASTE_YOUR_")
    or not APP_SECRET or APP_SECRET.startswith("PASTE_YOUR_")
    or not TRACKING_ID or TRACKING_ID.startswith("PASTE_YOUR_")
):
    logger.warning("AliExpress credentials are not fully configured in bot.py.")


# ============================================================
# 🛒 ALIEXPRESS CLIENT
# ============================================================

aliexpress = AliexpressApi(
    APP_KEY,
    APP_SECRET,
    models.Language.EN,
    models.Currency.USD,
    TRACKING_ID,
)


# ============================================================
# 🔗 LINK HANDLING
# ============================================================

LINK_REGEX = re.compile(
    r"https?://(?:[a-zA-Z0-9.-]+\.)?"
    r"aliexpress\.[a-z]{2,3}"
    r"(?:/[^\s]*)?",
    re.IGNORECASE,
)

product_cache = {}


def extract_id(url: str) -> Optional[str]:
    """
    Extract AliExpress product ID from common URL formats.
    """

    patterns = [
        r"/item/(\d+)\.html",
        r"productIds=(\d+)",
        r"/(\d+)\.html",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            url,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return None


def get_safe_link(api_result, fallback_url: str) -> str:
    """
    Safely get the affiliate promotion link.
    """

    try:
        if (
            not isinstance(api_result, Exception)
            and api_result
            and hasattr(api_result[0], "promotion_link")
            and api_result[0].promotion_link
        ):
            return api_result[0].promotion_link
    except Exception:
        pass

    return fallback_url


async def extract_product_info(
    text: str,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract product ID and canonical AliExpress URL.
    """

    match = LINK_REGEX.search(text)

    if not match:
        return None, None

    url = match.group(0)

    pid = extract_id(url)

    if pid:
        return (
            pid,
            f"https://www.aliexpress.com/item/{pid}.html",
        )

    # Short / redirect links
    if any(
        domain in url
        for domain in [
            "s.click.aliexpress.com",
            "a.aliexpress.com",
        ]
    ):
        try:
            timeout = aiohttp.ClientTimeout(total=8)

            async with aiohttp.ClientSession(
                timeout=timeout
            ) as session:

                # HEAD first
                try:
                    async with session.head(
                        url,
                        allow_redirects=True,
                    ) as resp:

                        final_url = str(resp.url)
                        pid = extract_id(final_url)

                        if pid:
                            return (
                                pid,
                                f"https://www.aliexpress.com/item/{pid}.html",
                            )
                except Exception:
                    pass

                # GET fallback
                async with session.get(
                    url,
                    allow_redirects=True,
                ) as resp:

                    final_url = str(resp.url)

                    pid = extract_id(final_url)

                    if pid:
                        return (
                            pid,
                            f"https://www.aliexpress.com/item/{pid}.html",
                        )

                    if "redirectUrl=" in final_url:
                        parsed = urlparse(final_url)
                        query = parse_qs(parsed.query)

                        redirected = query.get(
                            "redirectUrl",
                            [None],
                        )[0]

                        if redirected:
                            redirected = unquote(
                                redirected
                            )

                            pid = extract_id(
                                redirected
                            )

                            if pid:
                                return (
                                    pid,
                                    f"https://www.aliexpress.com/item/{pid}.html",
                                )

        except Exception as e:
            logger.warning(
                "Redirect extraction failed: %s",
                e,
            )

    return None, None


# ============================================================
# 💰 KOOKI SHOP COMMISSION
# ============================================================

def get_commission(price_usd: float) -> int:
    """
    Kouki Shop service commission in DZD.
    """

    if price_usd < 3:
        return 100

    if price_usd <= 5:
        return 150

    if price_usd <= 11:
        return 300

    if price_usd <= 15:
        return 400

    if price_usd <= 18:
        return 500

    if price_usd <= 22:
        return 600

    if price_usd <= 25:
        return 700

    if price_usd <= 32:
        return 800

    if price_usd <= 38:
        return 900

    if price_usd <= 44:
        return 1000

    if price_usd <= 62:
        return 1200

    if price_usd <= 70:
        return 1300

    if price_usd <= 80:
        return 1500

    if price_usd <= 90:
        return 1700

    if price_usd <= 100:
        return 1900

    if price_usd <= 120:
        return 2100

    if price_usd <= 160:
        return 2300

    if price_usd <= 200:
        return 2500

    return 3000


# ============================================================
# 🧠 SMART PRODUCT ANALYSIS
# ============================================================

def parse_number(value, default=0.0) -> float:
    """
    Safely parse prices / numeric strings.

    Supports:
    11.93
    1,299.99
    11,93
    """

    try:
        if value is None:
            return default

        text = str(value).strip()

        text = re.sub(
            r"[^\d,.\-]",
            "",
            text,
        )

        if not text:
            return default

        if "," in text and "." in text:
            # 1,299.99
            if text.rfind(",") < text.rfind("."):
                text = text.replace(",", "")
            # 1.299,99
            else:
                text = text.replace(".", "")
                text = text.replace(",", ".")

        elif "," in text:
            parts = text.split(",")

            # 11,93
            if len(parts[-1]) == 2:
                text = text.replace(",", ".")
            else:
                # 1,299
                text = text.replace(",", "")

        return float(text)

    except (
        ValueError,
        TypeError,
    ):
        return default


def parse_rating(value) -> float:
    """
    Normalize AliExpress rating to 0-5.
    """

    try:
        rating = parse_number(value, 0.0)

        # If API returns percentage such as 96.5
        if rating > 5:
            rating = rating / 20

        return max(
            0.0,
            min(rating, 5.0),
        )

    except Exception:
        return 0.0


def parse_sales(value) -> int:
    """
    Parse number of orders/sales.
    """

    try:
        if value is None:
            return 0

        text = re.sub(
            r"[^\d]",
            "",
            str(value),
        )

        return int(text) if text else 0

    except (
        ValueError,
        TypeError,
    ):
        return 0


def get_numeric_attr(obj, names):
    """Return the first usable numeric attribute/key from an object."""
    if obj is None:
        return None

    for name in names:
        try:
            if isinstance(obj, dict):
                value = obj.get(name)
            else:
                value = getattr(obj, name, None)
        except Exception:
            value = None

        parsed = parse_number(value, -1.0)
        if parsed >= 0:
            return parsed

    return None


def extract_shipping_fee(shipping_result) -> Optional[float]:
    """Extract shipping_fee from the official affiliate shipping response."""
    if shipping_result is None:
        return None

    # The dedicated endpoint returns a ShippingInfo object with shipping_fee.
    direct = get_numeric_attr(
        shipping_result,
        ("shipping_fee", "shippingFee", "fee", "shipping_cost"),
    )
    if direct is not None:
        return round(max(0.0, direct), 2)

    # Be defensive in case the SDK wraps the response in nested objects/dicts.
    seen = set()
    queue = [shipping_result]
    while queue:
        obj = queue.pop(0)
        oid = id(obj)
        if oid in seen:
            continue
        seen.add(oid)

        direct = get_numeric_attr(
            obj,
            ("shipping_fee", "shippingFee", "fee", "shipping_cost"),
        )
        if direct is not None:
            return round(max(0.0, direct), 2)

        if isinstance(obj, dict):
            values = obj.values()
        elif isinstance(obj, (list, tuple, set)):
            values = obj
        else:
            try:
                values = vars(obj).values()
            except Exception:
                values = ()

        for value in values:
            if isinstance(value, (dict, list, tuple, set)) or hasattr(value, "__dict__"):
                queue.append(value)

    return None


def get_sku_id(details):
    """Get the SKU id required by the country-specific shipping API."""
    for field in ("sku_id", "skuId", "product_sku_id", "productSkuId"):
        value = getattr(details, field, None)
        if value not in (None, "", 0, "0"):
            return value
    return None


def analyze_smart_data(
    rating: str,
    price_usd: float,
    original_usd: float,
    sales: str,
    estimated_checkout_usd: Optional[float] = None,
    shipping_usd: float = 0.0,
    shipping_confirmed: bool = False,
) -> dict:
    """
    Complete product analysis.

    IMPORTANT:
    target_sale_price from the Affiliate API is NOT guaranteed
    to equal the final Checkout price.

    Therefore estimated_checkout_usd is calculated using
    CHECKOUT_BUFFER.
    """

    # --------------------------------------------------------
    # Rating
    # --------------------------------------------------------

    r = parse_rating(rating)

    # --------------------------------------------------------
    # Sales / Orders
    # --------------------------------------------------------

    s_count = parse_sales(sales)

    # --------------------------------------------------------
    # Prices
    # --------------------------------------------------------

    price_usd = parse_number(
        price_usd,
        0.0,
    )

    original_usd = parse_number(
        original_usd,
        price_usd,
    )

    if price_usd < 0:
        price_usd = 0.0

    if original_usd < price_usd:
        original_usd = price_usd

    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    if (
        original_usd > price_usd
        and original_usd > 0
    ):
        discount = round(
            (1 - price_usd / original_usd) * 100
        )

        discount = max(
            0,
            min(discount, 99),
        )
    else:
        discount = 0

    # --------------------------------------------------------
    # Checkout Buffer
    # --------------------------------------------------------

    buffer_value = max(
        1.0,
        CHECKOUT_BUFFER,
    )

    max_buffer = max(
        buffer_value,
        MAX_CHECKOUT_BUFFER,
    )

    if estimated_checkout_usd is None:
        estimated_checkout_usd = (
            price_usd * buffer_value
        )

    estimated_checkout_usd = max(
        price_usd,
        parse_number(
            estimated_checkout_usd,
            price_usd,
        ),
    )

    # Don't let the estimate exceed our configured safety limit.
    if price_usd > 0:
        estimated_checkout_usd = min(
            estimated_checkout_usd,
            price_usd * max_buffer,
        )

    estimated_checkout_usd = round(
        estimated_checkout_usd,
        2,
    )

    # --------------------------------------------------------
    # Deal score /10
    # --------------------------------------------------------

    rating_score = (
        r / 5.0
    ) * 5

    discount_score = min(
        (discount / 50.0) * 5,
        5,
    )

    score_out_of_10 = round(
        rating_score + discount_score,
        1,
    )

    score_out_of_10 = max(
        0.0,
        min(score_out_of_10, 10.0),
    )

    # --------------------------------------------------------
    # Fraud / quality warning
    # --------------------------------------------------------

    if r >= 4.9 and s_count < 10:

        fake_warning = (
            "🚨 <b>تحذير:</b> تقييم مرتفع جداً "
            "مع عدد طلبات قليل."
        )

    elif (
        price_usd < 1.0
        and r >= 4.8
        and original_usd > 15
    ):

        fake_warning = (
            "🚨 <b>تحذير:</b> تخفيض غير منطقي "
            "مقارنة بالسعر الأصلي."
        )

    elif s_count > 500 and r < 4.0:

        fake_warning = (
            "⚠️ <b>احذر:</b> مبيعات كثيرة "
            "لكن التقييم منخفض."
        )

    elif s_count == 0:

        fake_warning = (
            "ℹ️ <b>ملاحظة:</b> عدد الطلبات "
            "غير متوفر في بيانات API."
        )

    else:

        fake_warning = (
            "✔️ <b>سليم:</b> لا توجد مؤشرات غش واضحة "
            "ضمن البيانات المتاحة."
        )

    # --------------------------------------------------------
    # Shipping
    # --------------------------------------------------------
    shipping_usd = max(0.0, parse_number(shipping_usd, 0.0))

    if shipping_usd > 0:
        shipping = (
            f"🚚 <b>الشحن إلى الجزائر:</b> + ${shipping_usd:.2f}"
        )
    elif shipping_confirmed:
        shipping = (
            "🚚 <b>الشحن إلى الجزائر:</b> مجاني مؤكّد"
        )
    else:
        shipping = (
            "🚚 <b>الشحن إلى الجزائر:</b> غير متوفر في API — يتحقق عند الدفع"
        )

    # --------------------------------------------------------
    # DZD calculations
    # --------------------------------------------------------

    # Raw API price
    api_price_dzd = round(
        price_usd * USD_TO_DZD
    )

    # Estimated Checkout price
    # Final estimated checkout = product price + 14% buffer + shipping
    final_checkout_usd = round(
        estimated_checkout_usd + shipping_usd, 2
    )

    checkout_dzd = round(
        final_checkout_usd * USD_TO_DZD
    )

    # Calculate Kouki commission using estimated checkout
    commission = get_commission(
        final_checkout_usd
    )

    # Final amount charged by Kouki Shop
    final_buy_dzd = (
        checkout_dzd
        + commission
    )

    # --------------------------------------------------------
    # Suggested reseller price
    # --------------------------------------------------------

    suggested_sell = (
        round(
            (
                final_buy_dzd
                * RESELLER_MARKUP
            ) / 100
        ) * 100
    )

    profit = max(
        0,
        suggested_sell - final_buy_dzd,
    )

    # --------------------------------------------------------
    # Deal status
    # --------------------------------------------------------

    if r >= 4.8 and discount >= 40:

        status = "💎 صفقة نادرة (لقطة)"

    elif r >= 4.5 and discount >= 25:

        status = "🔥 صفقة قوية"

    elif r >= 4.0:

        status = "✅ منتج موثوق"

    elif r > 0:

        status = "⚠️ منتج عادي"

    else:

        status = "ℹ️ بيانات التقييم غير متوفرة"

    # --------------------------------------------------------
    # Buffer percentage
    # --------------------------------------------------------

    if price_usd > 0:

        buffer_percent = round(
            (
                estimated_checkout_usd
                / price_usd
                - 1
            ) * 100
        )

    else:

        buffer_percent = 0

    return {
        "status": status,

        "score_10": score_out_of_10,

        "fake_alert": fake_warning,

        "shipping": shipping,

        # Raw API price
        "api_price_usd": round(
            price_usd,
            2,
        ),

        "api_price_dzd": api_price_dzd,

        # Estimated Checkout
        "estimated_checkout_usd":
            estimated_checkout_usd,

        "checkout_dzd":
            checkout_dzd,

        "checkout_buffer_percent":
            buffer_percent,

        # Kouki Shop
        "commission":
            commission,

        "buy_dzd":
            final_buy_dzd,

        "final_dzd":
            final_buy_dzd,

        # Reseller
        "sell_dzd":
            suggested_sell,

        "profit_dzd":
            profit,

        # Shipping / price breakdown
        "shipping_usd":
            shipping_usd,
        "final_checkout_usd":
            final_checkout_usd,
        "buffer_usd":
            round(
                max(0.0, estimated_checkout_usd - price_usd),
                2,
            ),

        # Orders
        "orders":
            s_count,
    }


# ============================================================
# 🖼️ PROFESSIONAL PRODUCT IMAGE
# ============================================================

async def create_pro_image(
    image_url: str,
    price_usd: str,
    price_dzd: str,
    discount: str,
) -> Optional[io.BytesIO]:

    if not image_url:
        return None

    try:

        timeout = aiohttp.ClientTimeout(
            total=10
        )

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.get(
                image_url
            ) as resp:

                if resp.status != 200:
                    return None

                image_data = await resp.read()

        img = Image.open(
            io.BytesIO(image_data)
        ).convert("RGBA")

        draw = ImageDraw.Draw(img)

        w, h = img.size

        border_w = max(
            2,
            int(w * 0.02)
        )

        draw.rectangle(
            [0, 0, w, h],
            outline=(232, 25, 35, 200),
            width=border_w,
        )

        bar_h = max(
            80,
            int(h * 0.20)
        )

        draw.rectangle(
            [0, h - bar_h, w, h],
            fill=(232, 25, 35, 240),
        )

        try:

            font_l = ImageFont.load_default(
                size=max(
                    18,
                    int(bar_h * 0.35)
                )
            )

            font_s = ImageFont.load_default(
                size=max(
                    14,
                    int(bar_h * 0.18)
                )
            )

        except Exception:

            font_l = ImageFont.load_default()
            font_s = ImageFont.load_default()

        draw.text(
            (
                w * 0.05,
                h - bar_h + bar_h * 0.08,
            ),
            f"{price_usd}$",
            fill="white",
            font=font_l,
        )

        draw.text(
            (
                w * 0.05,
                h - bar_h + bar_h * 0.58,
            ),
            f"~ {price_dzd} DZD",
            fill="yellow",
            font=font_s,
        )

        if discount:

            draw.text(
                (
                    w * 0.45,
                    h - bar_h + bar_h * 0.30,
                ),
                f"-{discount}% OFF",
                fill="white",
                font=font_l,
            )

        # Watermark
        text = "KOUKI SHOP"

        text_bbox = draw.textbbox(
            (0, 0),
            text,
            font=font_l,
        )

        text_w = (
            text_bbox[2]
            - text_bbox[0]
        )

        padding = int(
            w * 0.05
        )

        draw.text(
            (
                w - text_w - padding,
                h * 0.05,
            ),
            text,
            fill=(0, 0, 0, 180),
            font=font_l,
        )

        output = io.BytesIO()

        img.convert("RGB").save(
            output,
            format="JPEG",
            quality=95,
        )

        output.seek(0)

        return output

    except Exception as e:

        logger.warning(
            "Image generation failed: %s",
            e,
        )

        return None


# ============================================================
# 🔍 FETCH PRODUCT
# ============================================================

async def fetch_product_data(
    pid: str,
    item_url: str,
    full_links: bool = True,
):
    """
    Fetch AliExpress product data.

    full_links=True is used by the Telegram bot.
    The API endpoint can use the same function.
    """

    loop = asyncio.get_event_loop()

    jobs = [
        loop.run_in_executor(
            None,
            lambda: aliexpress.get_products_details(
                [pid],
                country=SHIP_TO_COUNTRY,
            ),
        ),
    ]

    if full_links:

        jobs.extend([

            # Coins
            loop.run_in_executor(
                None,
                lambda: aliexpress.get_affiliate_links(
                    f"https://m.aliexpress.com/p/"
                    f"coin-index/index.html?"
                    f"productIds={pid}"
                ),
            ),

            # Super Deals
            loop.run_in_executor(
                None,
                lambda: aliexpress.get_affiliate_links(
                    f"https://star.aliexpress.com/share/"
                    f"share.htm?redirectUrl="
                    f"{item_url}?sourceType=562"
                ),
            ),

            # Limited
            loop.run_in_executor(
                None,
                lambda: aliexpress.get_affiliate_links(
                    f"https://star.aliexpress.com/share/"
                    f"share.htm?redirectUrl="
                    f"{item_url}?sourceType=561"
                ),
            ),

            # Bundle
            loop.run_in_executor(
                None,
                lambda: aliexpress.get_affiliate_links(
                    f"https://star.aliexpress.com/share/"
                    f"share.htm?redirectUrl="
                    f"https://www.aliexpress.com/ssr/"
                    f"300000512/BundleDeals2?"
                    f"productIds={pid}"
                ),
            ),

            # Big Save
            loop.run_in_executor(
                None,
                lambda: aliexpress.get_affiliate_links(
                    f"https://star.aliexpress.com/share/"
                    f"share.htm?redirectUrl="
                    f"{item_url}?sourceType=680"
                ),
            ),
        ])

    results = await asyncio.gather(
        *jobs,
        return_exceptions=True,
    )

    details_result = results[0]

    if (
        isinstance(
            details_result,
            Exception,
        )
        or not details_result
    ):
        return None

    try:

        details = details_result[0]

    except (
        IndexError,
        TypeError,
    ):

        return None

    if not details:
        return None

    # --------------------------------------------------------
    # Price
    # --------------------------------------------------------

    price_usd_str = getattr(
        details,
        "target_sale_price",
        None,
    )

    if not price_usd_str:

        price_usd_str = getattr(
            details,
            "sale_price",
            None,
        )

    if not price_usd_str:

        price_usd_str = getattr(
            details,
            "original_price",
            "0",
        )

    orig_usd_str = getattr(
        details,
        "original_price",
        price_usd_str,
    )

    p_float = parse_number(
        price_usd_str,
        0.0,
    )

    o_float = parse_number(
        orig_usd_str,
        p_float,
    )

    if o_float < p_float:
        o_float = p_float

    # --------------------------------------------------------
    # Rating
    # --------------------------------------------------------

    rate = str(
        getattr(
            details,
            "evaluate_rate",
            getattr(
                details,
                "rating",
                "0",
            ),
        )
        or "0"
    )

    # --------------------------------------------------------
    # Orders
    # IMPORTANT:
    # Do NOT use target_sale_price_currency.
    # That field is currency, not sales count.
    # --------------------------------------------------------

    sales_value = None

    sales_fields = [
        "orders",
        "order_count",
        "sales_count",
        "trade_count",
        "total_orders",
    ]

    for field in sales_fields:

        value = getattr(
            details,
            field,
            None,
        )

        if value not in (
            None,
            "",
            "0",
            0,
        ):

            sales_value = value
            break

    if sales_value is None:
        sales_value = "0"

    sales = str(sales_value)

    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    if (
        o_float > p_float
        and o_float > 0
    ):

        discount_val = round(
            (
                1
                - p_float / o_float
            ) * 100
        )

        discount_val = max(
            0,
            min(discount_val, 99),
        )

    else:

        discount_val = 0

    # --------------------------------------------------------
    # Checkout buffer + country-specific shipping
    # --------------------------------------------------------

    # IMPORTANT: the 14% buffer is applied ONLY to the product price.
    # Shipping is then added separately using the AliExpress affiliate
    # shipping-info endpoint for Algeria (DZ) and the product SKU.
    estimated_checkout_usd = round(
        p_float * max(
            1.0,
            CHECKOUT_BUFFER,
        ),
        2,
    )

    shipping_usd = 0.0
    shipping_confirmed = False
    shipping_source = "unavailable"
    sku_id = get_sku_id(details)

    # The current maintained package may not contain the shipping endpoint,
    # so use getattr rather than crashing older deployments. The Render
    # requirements below install the branch that adds this method.
    shipping_method = getattr(
        aliexpress,
        "get_affiliate_product_shipping_info",
        None,
    )

    if callable(shipping_method) and sku_id not in (None, "", 0, "0"):
        try:
            shipping_result = await asyncio.get_running_loop().run_in_executor(
                None,
                lambda: shipping_method(
                    product_id=int(pid),
                    sku_id=int(sku_id),
                    ship_to_country=SHIP_TO_COUNTRY,
                    target_currency="USD",
                    target_sale_price=str(p_float),
                    tax_rate=SHIPPING_TAX_RATE,
                ),
            )
            fee = extract_shipping_fee(shipping_result)
            if fee is not None:
                shipping_usd = fee
                shipping_confirmed = True
                shipping_source = "affiliate_shipping_api"
        except Exception as e:
            logger.warning(
                "Country-specific shipping lookup failed for %s: %s",
                pid,
                e,
            )

    # Last-resort fallback only if the product detail itself exposes a
    # numeric fee. This is NOT treated as Algeria-confirmed shipping.
    if not shipping_confirmed:
        for field in (
            "shipping_fee", "shipping_cost", "shipping_price",
            "freight", "delivery_fee", "shipping_fee_usd"
        ):
            value = getattr(details, field, None)
            parsed = parse_number(value, -1.0)
            if parsed >= 0:
                shipping_usd = parsed
                shipping_source = "product_detail_fallback"
                break

    smart_data = analyze_smart_data(
        rating=rate,
        price_usd=p_float,
        original_usd=o_float,
        sales=sales,
        estimated_checkout_usd=estimated_checkout_usd,
        shipping_usd=shipping_usd,
        shipping_confirmed=shipping_confirmed,
    )

    # --------------------------------------------------------
    # Common details
    # --------------------------------------------------------

    title = getattr(
        details,
        "product_title",
        "منتج AliExpress",
    ) or "منتج AliExpress"

    image_url = getattr(
        details,
        "product_main_image_url",
        "",
    ) or ""

    store_name = getattr(
        details,
        "shop_name",
        getattr(
            details,
            "store_name",
            "AliExpress",
        ),
    ) or "AliExpress"

    # --------------------------------------------------------
    # Links
    # --------------------------------------------------------

    buy_link = item_url
    coin_link = item_url
    super_link = item_url
    limited_link = item_url
    bundle_link = item_url
    bigsave_link = item_url

    if full_links:

        buy_link = get_safe_link(
            results[1],
            item_url,
        )

        coin_link = get_safe_link(
            results[1],
            item_url,
        )

        super_link = get_safe_link(
            results[2],
            item_url,
        )

        limited_link = get_safe_link(
            results[3],
            item_url,
        )

        bundle_link = get_safe_link(
            results[4],
            item_url,
        )

        bigsave_link = get_safe_link(
            results[5],
            item_url,
        )

    else:

        # Buy affiliate link only
        buy_link = get_safe_link(
            results[1],
            item_url,
        ) if len(results) > 1 else item_url

    # --------------------------------------------------------
    # Final data
    # --------------------------------------------------------

    data = {
        "product_id": pid,

        "title": str(title)[:100],

        "price_usd": round(
            p_float,
            2,
        ),

        "orig_usd": round(
            o_float,
            2,
        ),

        "disc": str(
            discount_val
        ),

        "rate": rate,

        "orders": smart_data[
            "orders"
        ],

        "img": image_url,

        "buy": buy_link,

        "coin": coin_link,

        "super": super_link,

        "limited": limited_link,

        "bundle": bundle_link,

        "bigsave": bigsave_link,

        "sourceUrl": item_url,

        "store_name": store_name,

        # Raw API price
        "api_price_dzd":
            smart_data[
                "api_price_dzd"
            ],

        # Estimated Checkout
        "estimated_checkout_usd":
            smart_data[
                "estimated_checkout_usd"
            ],

        "product_buffer_usd":
            smart_data[
                "buffer_usd"
            ],

        "final_checkout_usd":
            smart_data[
                "final_checkout_usd"
            ],

        "shipping_usd":
            shipping_usd,

        "shipping_confirmed":
            shipping_confirmed,

        "shipping_source":
            shipping_source,

        "shipping_source_detail":
            shipping_source,

        "ship_to_country":
            SHIP_TO_COUNTRY,

        "checkout_dzd":
            smart_data[
                "checkout_dzd"
            ],

        "checkout_buffer_percent":
            smart_data[
                "checkout_buffer_percent"
            ],

        # Kouki Shop
        "base_dzd":
            smart_data[
                "checkout_dzd"
            ],

        "commission":
            smart_data[
                "commission"
            ],

        "buy_dzd":
            smart_data[
                "buy_dzd"
            ],

        "final_dzd":
            smart_data[
                "final_dzd"
            ],

        # Reseller
        "sell_dzd":
            smart_data[
                "sell_dzd"
            ],

        "profit_dzd":
            smart_data[
                "profit_dzd"
            ],

        # Analysis
        "status":
            smart_data[
                "status"
            ],

        "score_10":
            smart_data[
                "score_10"
            ],

        "fake_alert":
            smart_data[
                "fake_alert"
            ],

        "shipping":
            smart_data[
                "shipping"
            ],
    }

    return data


# ============================================================
# 🤖 TELEGRAM RESPONSE
# ============================================================

async def send_pro_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    data: dict,
):

    keyboard = [

        [
            InlineKeyboardButton(
                f"🛒 اشتري الآن "
                f"({data['buy_dzd']:,} دج)",
                url=data["buy"],
            )
        ],

        [
            InlineKeyboardButton(
                "🪙 العملات",
                url=data["coin"],
            ),

            InlineKeyboardButton(
                "⚡ سوبر ديلز",
                url=data["super"],
            ),
        ],

        [
            InlineKeyboardButton(
                "📦 عروض Bundle",
                url=data["bundle"],
            ),

            InlineKeyboardButton(
                "⏱️ عرض محدود",
                url=data["limited"],
            ),
        ],

        [
            InlineKeyboardButton(
                "🏷️ تخفيض Big Save",
                url=data["bigsave"],
            )
        ],

        [
            InlineKeyboardButton(
                "💬 تواصل معي للطلب عبر فيسبوك",
                url=FACEBOOK_URL,
            )
        ],
    ]

    caption = f"""
🤖 <b>تقرير خبير Kouki Shop:</b>
{data['status']}

🔹 <b>{data['title']}</b>

💵 <b>سعر AliExpress:</b>
{data['price_usd']}$ <s>{data['orig_usd']}$</s>
(-{data['disc']}%)

💳 <b>حساب السعر:</b>
• سعر المنتج: <b>${data['price_usd']:.2f}</b>
• Buffer 14%: <b>+${data.get('product_buffer_usd', 0):.2f}</b>
• الشحن إلى الجزائر: <b>+${data.get('shipping_usd', 0):.2f}</b>
• الإجمالي قبل العمولة: <b>${data.get('final_checkout_usd', data['estimated_checkout_usd']):.2f}</b>

⭐ <b>التقييم:</b>
{data['rate']}/5.0

🌟 <b>جودة الصفقة:</b>
{data['score_10']}/10

🛒 <b>الطلبات:</b>
{data['orders']:,}

{data['shipping']}

🛡️ <b>نظام كشف الغش:</b>
{data['fake_alert']}

💰 <b>حساب Kouki Shop:</b>

📦 سعر Checkout المتوقع:
<b>{data['checkout_dzd']:,} دج</b>

💼 عمولة الخدمة:
<b>+{data['commission']:,} دج</b>

━━━━━━━━━━━━━━

💳 <b>السعر النهائي التقريبي:</b>
<b>{data['buy_dzd']:,} دج</b>

📤 <b>سعر البيع المقترح:</b>
<b>{data['sell_dzd']:,} دج</b>

💰 <b>الفائدة:</b>
~{data['profit_dzd']:,} دج

━━━━━━━━━━━━━━

⚠️ <b>ملاحظة مهمة:</b>
السعر النهائي في AliExpress قد يختلف عند الدفع بسبب الكوبونات، الـSKU، بلد الشحن، الضرائب أو العروض المتاحة في حسابك.

📊 هامش الحماية المستخدم:
<b>+{data['checkout_buffer_percent']}%</b>

👇 <b>اختر رابط التخفيض المناسب لك:</b>
"""

    pro_img = await create_pro_image(
        data["img"],
        str(data.get("final_checkout_usd", data["estimated_checkout_usd"])),
        str(data["buy_dzd"]).replace(
            ",",
            "",
        ),
        data["disc"],
    )

    try:

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=(
                pro_img
                if pro_img
                else data["img"]
            ),
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
            parse_mode=ParseMode.HTML,
        )

    except Exception as e:

        logger.error(
            "Telegram send error: %s",
            e,
        )

        await update.message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
            parse_mode=ParseMode.HTML,
        )


# ============================================================
# 📩 TELEGRAM MESSAGE HANDLER
# ============================================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    text = update.message.text or ""

    pid, item_url = await extract_product_info(
        text
    )

    if not pid or not item_url:

        if LINK_REGEX.search(text):

            await update.message.reply_text(
                "❌ الرابط غير صالح."
            )

        return

    # --------------------------------------------------------
    # Cache
    # --------------------------------------------------------

    cached = product_cache.get(pid)

    if cached:

        cache_age = (
            time.time()
            - cached.get(
                "time",
                0,
            )
        )

        if cache_age < CACHE_TTL:

            await send_pro_response(
                update,
                context,
                cached["data"],
            )

            return

    sent_msg = await update.message.reply_text(
        "🔎 خبير الشراء يجهز التقرير الشامل..."
    )

    try:

        data = await fetch_product_data(
            pid,
            item_url,
            full_links=True,
        )

        if not data:

            await sent_msg.edit_text(
                "❌ لم أجد بيانات المنتج."
            )

            return

        product_cache[pid] = {
            "data": data,
            "time": time.time(),
        }

        try:
            await sent_msg.delete()
        except Exception:
            pass

        await send_pro_response(
            update,
            context,
            data,
        )

    except Exception as e:

        logger.exception(
            "Product analysis failed"
        )

        try:

            await sent_msg.edit_text(
                "⚠️ حدث خطأ أثناء تحليل المنتج."
            )

        except Exception:
            pass


# ============================================================
# /START
# ============================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    msg = """
👋 أهلاً بك في <b>Kouki Shop Bot</b>!

🛍️ أرسل رابط أي منتج من AliExpress.

🤖 سيقوم البوت بـ:
• تحليل المنتج
• حساب الخصم
• عرض التقييم
• عرض عدد الطلبات
• تقدير سعر Checkout
• حساب عمولة Kouki Shop
• حساب السعر النهائي بالدينار
• إعطائك روابط Coins / Super Deals / Bundle / Big Save

💡 <b>ملاحظة:</b>
سعر Checkout تقديري وقد يتغير حسب الكوبونات والـSKU وبلد الشحن وحسابك.
"""

    await update.message.reply_text(
        msg,
        parse_mode=ParseMode.HTML,
    )


# ============================================================
# 🌐 FASTAPI
# ============================================================

api_app = FastAPI(
    title="Kouki Shop AliExpress API",
    version="2.0.0",
)

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LinkRequest(BaseModel):
    url: str


# ============================================================
# /product
# ============================================================

@api_app.get("/product")
async def product_api(
    url: str,
):

    pid, item_url = await extract_product_info(
        url
    )

    if not pid:

        return {
            "error": "Invalid AliExpress URL"
        }

    # --------------------------------------------------------
    # Cache
    # --------------------------------------------------------

    cached = product_cache.get(pid)

    if cached:

        cache_age = (
            time.time()
            - cached.get(
                "time",
                0,
            )
        )

        if cache_age < CACHE_TTL:

            return dict(
                cached["data"]
            )

    # --------------------------------------------------------
    # Fetch
    # --------------------------------------------------------

    try:

        data = await fetch_product_data(
            pid,
            item_url,
            full_links=False,
        )

        if not data:

            return {
                "error":
                    "Product not found"
            }

        product_cache[pid] = {
            "data": data,
            "time": time.time(),
        }

        return data

    except Exception as e:

        logger.exception(
            "API product error"
        )

        return {
            "error": str(e)
        }


# ============================================================
# /analyze
# ============================================================

@api_app.post("/analyze")
async def analyze_api(
    req: LinkRequest,
):

    return await product_api(
        req.url
    )


# ============================================================
# PAYPAL
# ============================================================

class PayPalOrderRequest(BaseModel):
    amount: float


class PayPalCaptureRequest(BaseModel):
    order_id: str
    product_details: dict = Field(default_factory=dict)


PAYPAL_CLIENT_ID = "PASTE_YOUR_PAYPAL_CLIENT_ID_HERE"

PAYPAL_SECRET_KEY = "PASTE_YOUR_PAYPAL_SECRET_KEY_HERE"


def get_paypal_basic_auth():

    auth_str = (
        f"{PAYPAL_CLIENT_ID}:"
        f"{PAYPAL_SECRET_KEY}"
    )

    b64_auth = base64.b64encode(
        auth_str.encode()
    ).decode()

    return {
        "Authorization":
            f"Basic {b64_auth}"
    }


async def get_paypal_access_token():

    if not PAYPAL_CLIENT_ID or not PAYPAL_SECRET_KEY:
        return None

    timeout = aiohttp.ClientTimeout(
        total=15
    )

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        url = (
            "https://api-m.paypal.com/"
            "v1/oauth2/token"
        )

        headers = get_paypal_basic_auth()

        headers[
            "Content-Type"
        ] = (
            "application/"
            "x-www-form-urlencoded"
        )

        data = {
            "grant_type":
                "client_credentials"
        }

        async with session.post(
            url,
            headers=headers,
            data=data,
        ) as resp:

            if resp.status != 200:

                logger.error(
                    "PayPal token error: %s",
                    await resp.text(),
                )

                return None

            result = await resp.json()

            return result.get(
                "access_token"
            )


@api_app.post(
    "/api/paypal/create-order"
)
async def create_paypal_order(
    req: PayPalOrderRequest,
):

    if req.amount <= 0:

        return {
            "error":
                "Amount must be greater than zero"
        }

    token = await get_paypal_access_token()

    if not token:

        return {
            "error":
                "PayPal is not configured"
        }

    timeout = aiohttp.ClientTimeout(
        total=15
    )

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        paypal_api_url = (
            "https://api-m.paypal.com/"
            "v2/checkout/orders"
        )

        headers = {
            "Authorization":
                f"Bearer {token}",

            "Content-Type":
                "application/json",
        }

        payload = {

            "intent":
                "CAPTURE",

            "purchase_units": [
                {
                    "amount": {
                        "currency_code":
                            "USD",

                        "value":
                            f"{req.amount:.2f}",
                    }
                }
            ],
        }

        async with session.post(
            paypal_api_url,
            json=payload,
            headers=headers,
        ) as resp:

            data = await resp.json()

            if resp.status not in (
                200,
                201,
            ):

                return {
                    "error":
                        data
                }

            return data


@api_app.post(
    "/api/paypal/capture-order"
)
async def capture_paypal_order(
    req: PayPalCaptureRequest,
):

    if not req.order_id:

        return {
            "error":
                "order_id is required"
        }

    token = await get_paypal_access_token()

    if not token:

        return {
            "error":
                "PayPal is not configured"
        }

    timeout = aiohttp.ClientTimeout(
        total=20
    )

    async with aiohttp.ClientSession(
        timeout=timeout
    ) as session:

        url = (
            "https://api-m.paypal.com/"
            f"v2/checkout/orders/"
            f"{req.order_id}/capture"
        )

        headers = {
            "Authorization":
                f"Bearer {token}",

            "Content-Type":
                "application/json",
        }

        async with session.post(
            url,
            headers=headers,
        ) as resp:

            data = await resp.json()

            if resp.status not in (
                200,
                201,
            ):

                return {
                    "error":
                        data
                }

            return {
                "success":
                    True,

                "paypal":
                    data,

                "product_details":
                    req.product_details,
            }


# ============================================================
# 🧹 CACHE CLEANUP
# ============================================================

async def cache_cleanup_loop():

    while True:

        try:

            now = time.time()

            expired = []

            for pid, item in list(
                product_cache.items()
            ):

                if (
                    now
                    - item.get(
                        "time",
                        0,
                    )
                    > CACHE_TTL
                ):

                    expired.append(pid)

            for pid in expired:

                product_cache.pop(
                    pid,
                    None,
                )

        except Exception as e:

            logger.warning(
                "Cache cleanup error: %s",
                e,
            )

        await asyncio.sleep(
            600
        )


# ============================================================
# 🚀 RUN FASTAPI
# ============================================================

def run_api():

    uvicorn.run(
        api_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )


# ============================================================
# 🚀 MAIN
# ============================================================

async def main():

    if not TOKEN:

        raise RuntimeError(
            "BOT_TOKEN is missing. Put your Telegram bot token in the TOKEN variable at the top of bot.py."
        )

    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            handle_message,
        )
    )

    # Start FastAPI in background thread
    api_thread = threading.Thread(
        target=run_api,
        daemon=True,
    )

    api_thread.start()

    # Cache cleanup
    asyncio.create_task(
        cache_cleanup_loop()
    )

    logger.info(
        "Kouki Shop Bot starting..."
    )

    logger.info(
        "USD_TO_DZD = %s",
        USD_TO_DZD,
    )

    logger.info(
        "SHIP_TO_COUNTRY = %s",
        SHIP_TO_COUNTRY,
    )

    logger.info(
        "CHECKOUT_BUFFER = %s (+%s%%)",
        CHECKOUT_BUFFER,
        round(
            (CHECKOUT_BUFFER - 1)
            * 100
        ),
    )

    await application.initialize()

    await application.start()

    await application.updater.start_polling()

    try:

        while True:
            await asyncio.sleep(3600)

    finally:

        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":

    try:
        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        logger.info(
            "Bot stopped."
        )
