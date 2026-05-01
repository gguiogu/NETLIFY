import asyncio
import aiohttp
import re
import time
import io
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs, unquote

# Requires Pillow: pip install Pillow
from PIL import Image, ImageDraw, ImageFont

# Requires python-telegram-bot: pip install python-telegram-bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from telegram.constants import ParseMode

from aliexpress_api import AliexpressApi, models

# ==========================================
# ⚙️ الإعدادات الأساسية
# ==========================================
TOKEN = "7250440174:AAE886dWCGSh6JqCdtd66SpNDQPZPoz4w4g"
APP_KEY = "515874"
APP_SECRET = "jSWlobcAFLVp9Jo4QEjcbqXpbQBk4JRQ"
TRACKING_ID = '130740'

USD_TO_DZD = 250
PROFIT_MARGIN = 1.4 # هامش الربح للتاجر

aliexpress = AliexpressApi(APP_KEY, APP_SECRET, models.Language.EN, models.Currency.USD, TRACKING_ID)
LINK_REGEX = re.compile(r'https?://([a-zA-Z0-9.-]+\.)?aliexpress\.[a-z]{2,3}(/[^\s]*)?', re.IGNORECASE)

product_cache = {}
CACHE_TTL = 21600

# ==========================================
# 🔗 دوال مساعدة للروابط
# ==========================================
def extract_id(url: str) -> Optional[str]:
    match = re.search(r'/item/(\d+)\.html|productIds=(\d+)|/(\d+)\.html', url, re.IGNORECASE)
    return match.group(1) or match.group(2) or match.group(3) if match else None

def get_safe_link(api_result, fallback_url):
    """استخراج رابط التخفيض بأمان لتجنب الأخطاء"""
    if not isinstance(api_result, Exception) and api_result and hasattr(api_result[0], 'promotion_link'):
        return api_result[0].promotion_link
    return fallback_url

async def extract_product_info(text: str) -> Tuple[Optional[str], Optional[str]]:
    match = LINK_REGEX.search(text)
    if not match: return None, None
    url = match.group(0)
    pid = extract_id(url)
    if pid: return pid, f"https://www.aliexpress.com/item/{pid}.html"

    if any(d in url for d in ['s.click.aliexpress.com', 'a.aliexpress.com']):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True, timeout=5) as resp:
                    pid = extract_id(str(resp.url))
                    if pid: return pid, f"https://www.aliexpress.com/item/{pid}.html"
                async with session.get(url, allow_redirects=True, timeout=5) as resp:
                    final_url = str(resp.url)
                    pid = extract_id(final_url)
                    if pid: return pid, f"https://www.aliexpress.com/item/{pid}.html"
                    if 'redirectUrl=' in final_url:
                        parsed = urlparse(final_url)
                        query = parse_qs(parsed.query)
                        redirected = query.get('redirectUrl', [None])[0]
                        if redirected:
                            pid = extract_id(unquote(redirected))
                            if pid: return pid, f"https://www.aliexpress.com/item/{pid}.html"
        except: pass
    return None, None

def get_commission(price_usd: float) -> int:
    if price_usd < 3: return 100
    if price_usd <= 5: return 150
    if price_usd <= 11: return 300
    if price_usd <= 15: return 400
    if price_usd <= 18: return 500
    if price_usd <= 22: return 600
    if price_usd <= 25: return 700
    if price_usd <= 32: return 800
    if price_usd <= 38: return 900
    if price_usd <= 44: return 1000
    if price_usd <= 62: return 1200
    if price_usd <= 70: return 1300
    if price_usd <= 80: return 1500
    if price_usd <= 90: return 1700
    if price_usd <= 100: return 1900
    if price_usd <= 120: return 2100
    if price_usd <= 160: return 2300
    if price_usd <= 200: return 2500
    return 3000

# ==========================================
# 🧠 الذكاء الاصطناعي (تحليل، كشف الغش، وتقييم 10/10)
# ==========================================
def analyze_smart_data(rating: str, price_usd: float, original_usd: float, sales: str) -> dict:
    try: r = float(rating)
    except: r = 0.0
    
    try: s_count = int(re.sub(r'\D', '', sales)) if sales else 0
    except: s_count = 0

    discount = round((1 - price_usd/original_usd) * 100) if original_usd > price_usd else 0

    # 🌟 حساب تقييم الصفقة من 10 (يجمع بين التقييم والخصم)
    score_out_of_10 = round(((r / 5.0) * 5) + min((discount / 50.0) * 5, 5), 1)
    if score_out_of_10 > 10: score_out_of_10 = 10.0

    # 1. 🚨 كشف الغش
    fake_warning = ""
    if r >= 4.9 and s_count < 10:
        fake_warning = "🚨 <b>تحذير:</b> تقييم عالي جداً مع مبيعات شبه معدومة."
    elif price_usd < 1.0 and r >= 4.8 and original_usd > 15:
        fake_warning = "🚨 <b>تحذير:</b> تخفيض غير منطقي (احتمال منتج رديء)."
    elif s_count > 500 and r < 4.0:
        fake_warning = "⚠️ <b>احذر:</b> مبيعات كثيرة لكن الزبائن غير راضين."
    else:
        fake_warning = "✔️ <b>سليم:</b> لا توجد مؤشرات غش واضحة."

    # 2. 🚚 الشحن
    if price_usd < 4.0:
        shipping = "🚚 <b>الشحن:</b> Cainiao Super Economy\n⏱️ <b>المدة:</b> 30 - 60 يوم"
    else:
        shipping = "🚚 <b>الشحن:</b> AliExpress Standard (مُتتبع)\n⏱️ <b>المدة:</b> 15 - 35 يوم"

    # 3. 💸 وضع التاجر وحساب العمولة
    base_dzd = int(price_usd * USD_TO_DZD)
    commission = get_commission(price_usd)
    final_buy_dzd = base_dzd + commission
    
    suggested_sell = round(int(final_buy_dzd * 1.3) / 100) * 100 # Reseller adds 30% for themselves
    profit = suggested_sell - final_buy_dzd

    if r >= 4.8 and discount >= 40: status = "💎 صفقة نادرة (لقطة)"
    elif r >= 4.5 and discount >= 25: status = "🔥 صفقة قوية"
    elif r >= 4.0: status = "✅ منتج موثوق"
    else: status = "⚠️ منتج عادي"

    return {
        "status": status,
        "score_10": score_out_of_10,
        "fake_alert": fake_warning,
        "shipping": shipping,
        "buy_dzd": final_buy_dzd,
        "base_dzd": base_dzd,
        "commission": commission,
        "sell_dzd": suggested_sell,
        "profit_dzd": profit
    }

# ==========================================
# 🖼️ الصورة الاحترافية (علامة مائية أعلى اليمين)
# ==========================================
async def create_pro_image(image_url: str, price_usd: str, price_dzd: str, discount: str) -> Optional[io.BytesIO]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, timeout=5) as resp:
                if resp.status != 200: return None
                image_data = await resp.read()

        img = Image.open(io.BytesIO(image_data)).convert("RGBA")
        draw = ImageDraw.Draw(img)
        w, h = img.size

        border_w = int(w * 0.02)
        draw.rectangle([0, 0, w, h], outline=(232, 25, 35, 200), width=border_w)

        bar_h = int(h * 0.20)
        draw.rectangle([0, h - bar_h, w, h], fill=(232, 25, 35, 240))

        try: font_l = ImageFont.load_default(size=int(bar_h * 0.4))
        except: font_l = ImageFont.load_default()
        try: font_s = ImageFont.load_default(size=int(bar_h * 0.2))
        except: font_s = ImageFont.load_default()
        
        draw.text((w * 0.05, h - bar_h + (bar_h * 0.1)), f"{price_usd}$", fill="white", font=font_l)
        draw.text((w * 0.05, h - bar_h + (bar_h * 0.6)), f"~ {price_dzd} DZD", fill="yellow", font=font_s)
        
        if discount:
            draw.text((w * 0.45, h - bar_h + (bar_h * 0.3)), f"-{discount}% OFF", fill="white", font=font_l)

        # العلامة المائية: أعلى اليمين (أسود شفاف)
        text = "KOUKI SHOP"
        text_bbox = draw.textbbox((0, 0), text, font=font_l)
        text_w = text_bbox[2] - text_bbox[0]
        padding = int(w * 0.05)
        draw.text((w - text_w - padding, h * 0.05), text, fill=(0, 0, 0, 180), font=font_l)

        output = io.BytesIO()
        img.convert("RGB").save(output, format="JPEG", quality=95)
        output.seek(0)
        return output
    except: return None

# ==========================================
# 🚀 المعالج الرئيسي للروابط (توازي فائق السرعة)
# ==========================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    pid, item_url = await extract_product_info(text)
    
    if not pid or not item_url:
        if LINK_REGEX.search(text):
            await update.message.reply_text("❌ الرابط غير صالح.")
        return

    if pid in product_cache and (time.time() - product_cache[pid]['time'] < CACHE_TTL):
        await send_pro_response(update, context, product_cache[pid]['data'])
        return

    sent_msg = await update.message.reply_text("🔎 خبير الشراء يجهز التقرير الشامل...")

    loop = asyncio.get_event_loop()
    try:
        # 🏎️ جلب جميع روابط التخفيضات في نفس اللحظة!
        results = await asyncio.gather(
            loop.run_in_executor(None, lambda: aliexpress.get_products_details([pid])), # 0 details
            loop.run_in_executor(None, lambda: aliexpress.get_affiliate_links(f"https://m.aliexpress.com/p/coin-index/index.html?productIds={pid}")), # 1 coin
            loop.run_in_executor(None, lambda: aliexpress.get_affiliate_links(f"https://star.aliexpress.com/share/share.htm?redirectUrl={item_url}?sourceType=562")), # 2 super
            loop.run_in_executor(None, lambda: aliexpress.get_affiliate_links(f"https://star.aliexpress.com/share/share.htm?redirectUrl={item_url}?sourceType=561")), # 3 limited
            loop.run_in_executor(None, lambda: aliexpress.get_affiliate_links(f"https://star.aliexpress.com/share/share.htm?redirectUrl=https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds={pid}")), # 4 bundle
            loop.run_in_executor(None, lambda: aliexpress.get_affiliate_links(f"https://star.aliexpress.com/share/share.htm?redirectUrl={item_url}?sourceType=680")), # 5 bigsave
            return_exceptions=True
        )

        details = results[0][0] if not isinstance(results[0], Exception) and results[0] else None
        if not details:
            await sent_msg.edit_text("❌ لم أجد بيانات المنتج.")
            return

        price_usd_str = getattr(details, 'target_sale_price', getattr(details, 'original_price', '0'))
        orig_usd_str = getattr(details, 'original_price', price_usd_str)
        rate = str(getattr(details, 'evaluate_rate', '0.0'))
        sales = str(getattr(details, 'target_sale_price_currency', '0'))
        
        try: p_float = float(price_usd_str)
        except: p_float = 0.0
        try: o_float = float(orig_usd_str)
        except: o_float = p_float
        
        discount_val = round((1 - p_float/o_float) * 100) if o_float > p_float else 0

        # الذكاء الاصطناعي
        smart_data = analyze_smart_data(rate, p_float, o_float, sales)

        data = {
            'title': getattr(details, 'product_title', 'منتج')[:60],
            'price_usd': price_usd_str,
            'orig_usd': orig_usd_str,
            'disc': str(discount_val) if discount_val > 0 else "0",
            'rate': rate,
            'img': getattr(details, 'product_main_image_url', ''),
            'buy': getattr(details, 'promotion_link', item_url),
            'coin': get_safe_link(results[1], item_url),
            'super': get_safe_link(results[2], item_url),
            'limited': get_safe_link(results[3], item_url),
            'bundle': get_safe_link(results[4], item_url),
            'bigsave': get_safe_link(results[5], item_url),
            **smart_data
        }

        product_cache[pid] = {'data': data, 'time': time.time()}
        await sent_msg.delete()
        await send_pro_response(update, context, data)

    except Exception as e:
        await sent_msg.edit_text("⚠️ خطأ في التحليل.")

# ==========================================
# 🎯 إرسال التقرير الشامل
# ==========================================
async def send_pro_response(update, context, data):
    # تنسيق الأزرار (كل رابطين في سطر لتوفير المساحة وجعلها منظمة)
    keyboard = [
        [InlineKeyboardButton(f"🛒 اشتري الآن ({data['buy_dzd']:,} دج)", url=data['buy'])],
        [
            InlineKeyboardButton("🪙 العملات", url=data['coin']),
            InlineKeyboardButton("⚡ سوبر ديلز", url=data['super'])
        ],
        [
            InlineKeyboardButton("📦 عروض Bundle", url=data['bundle']),
            InlineKeyboardButton("⏱️ عرض محدود", url=data['limited'])
        ],
        [InlineKeyboardButton("🏷️ تخفيض Big Save", url=data['bigsave'])],
        [
            InlineKeyboardButton("💬 تواصل معي للطلب عبر فيسبوك", url="https://www.facebook.com/XBHTHAGOAT/")
        ]
    ]

    caption = f"""🤖 <b>تقرير خبير Kouki Shop:</b>
{data['status']}

🔹 <b>{data['title']}...</b>
💵 <b>السعر:</b> {data['price_usd']}$ <s>{data['orig_usd']}$</s> (-{data['disc']}%)
⭐ <b>التقييم:</b> {data['rate']}/5.0 | 🌟 <b>جودة الصفقة:</b> {data['score_10']}/10

{data['shipping']}

🛡️ <b>نظام كشف الغش:</b>
{data['fake_alert']}

💸 <b>مقترح التاجر (Reseller):</b>
📥 شراء: <b>{data['buy_dzd']:,} دج</b> | 📤 بيع: <b>{data['sell_dzd']:,} دج</b>
💰 الفائدة: <b>~{data['profit_dzd']:,} دج</b>

⚠️ <b>ملاحظة هامة جداً:</b>
هذا السعر مبدئي. السعر النهائي يعتمد على الكوبونات الخاصة بك، وعلى تغيير البلد من الجزائر إلى كندا، والعملات المتوفرة في حسابك.

👇 <b>اختر رابط التخفيض المناسب لك:</b>"""

    pro_img = await create_pro_image(data['img'], data['price_usd'], str(data['buy_dzd']).replace(',', ''), data['disc'])
    
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=pro_img if pro_img else data['img'],
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "👋 أهلاً بك في <b>Kouki Shop Bot</b>!\nأرسل رابط أي منتج، وسأحلله وأعطيك تقييماً من 10 مع أقوى روابط التخفيضات (Bundle, Coins, Big Save...)."
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML)

# ==========================================
# 🌐 FastAPI (لربط الموقع بنفس البوت)
# ==========================================
api_app = FastAPI()

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/product")
async def product_api(url: str):
    pid, item_url = await extract_product_info(url)
    if not pid:
        return {"error": "Invalid URL"}
    
    if pid in product_cache and (time.time() - product_cache[pid]['time'] < CACHE_TTL):
        cached_data = product_cache[pid]['data']
        # إذا لم تكن البيانات محسوبة مسبقاً بشكل تفصيلي للـ API، نقوم بتنسيقها
        if 'base_dzd' not in cached_data:
            price_usd = float(cached_data.get('price_usd', 0))
            commission = get_commission(price_usd)
            base_dzd = int(price_usd * USD_TO_DZD)
            cached_data['base_dzd'] = base_dzd
            cached_data['commission'] = commission
            cached_data['final_dzd'] = base_dzd + commission
            cached_data['sourceUrl'] = item_url
        return cached_data
        
    loop = asyncio.get_event_loop()
    try:
        results = await asyncio.gather(
            loop.run_in_executor(None, lambda: aliexpress.get_products_details([pid])),
            loop.run_in_executor(None, lambda: aliexpress.get_affiliate_links(f"https://star.aliexpress.com/share/share.htm?redirectUrl={item_url}?sourceType=562")),
            return_exceptions=True
        )

        details = results[0][0] if not isinstance(results[0], Exception) and results[0] else None
        if not details:
            return {"error": "Product not found"}

        price_usd_str = getattr(details, 'target_sale_price', getattr(details, 'original_price', '0'))
        orig_usd_str = getattr(details, 'original_price', price_usd_str)
        rate = str(getattr(details, 'evaluate_rate', '0.0'))
        sales = str(getattr(details, 'target_sale_price_currency', '0'))
        
        try: p_float = float(price_usd_str)
        except: p_float = 0.0
        try: o_float = float(orig_usd_str)
        except: o_float = p_float
        
        discount_val = round((1 - p_float/o_float) * 100) if o_float > p_float else 0
        smart_data = analyze_smart_data(rate, p_float, o_float, sales)

        commission = get_commission(p_float)
        base_dzd = int(p_float * USD_TO_DZD)
        final_dzd = base_dzd + commission

        data = {
            'title': getattr(details, 'product_title', 'منتج'),
            'price_usd': price_usd_str,
            'orig_usd': orig_usd_str,
            'disc': str(discount_val) if discount_val > 0 else "0",
            'rate': rate,
            'img': getattr(details, 'product_main_image_url', ''),
            'buy': get_safe_link(results[1], item_url),
            'base_dzd': base_dzd,
            'commission': commission,
            'final_dzd': final_dzd,
            'sourceUrl': item_url,
            'store_name': getattr(details, 'shop_name', 'AliExpress'),
            'orders': getattr(details, 'target_sale_price_currency', '0'),
            **smart_data
        }

        product_cache[pid] = {'data': data, 'time': time.time()}
        return data

    except Exception as e:
        return {"error": str(e)}

def run_api():
    uvicorn.run(api_app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    # تشغيل API في Thread
    threading.Thread(target=run_api, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Kouki Shop Bot and API Server are now running on port 8000.")
    app.run_polling()
