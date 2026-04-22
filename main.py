from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
import motor.motor_asyncio
from datetime import datetime
from supabase import create_client, Client

# استيراد دوال البوت لمعالجة المنتج
from bot import (
    extract_product_info,
    analyze_smart_data,
    get_safe_link,
    aliexpress
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Configuration
SUPABASE_URL = "https://axbrosibywcdxwlbjyqv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF4YnJvc2lieXdjZHh3bGJqeXF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4NzE1MDAsImV4cCI6MjA5MjQ0NzUwMH0.hXs9aFZ_GZzb1TGkk0lU1WpLL1fE_EohO1enS7H8Itc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class LinkRequest(BaseModel):
    url: str

class CommentModel(BaseModel):
    name: str
    city: str
    text: str
    rating: int
    product: str = ""

cache = {}

@app.post("/analyze")
async def analyze(data: LinkRequest):
    pid, item_url = await extract_product_info(data.url)

    if not pid:
        return {"error": "invalid link"}

    if pid in cache and time.time() - cache[pid]["time"] < 3600:
        return cache[pid]["data"]

    loop = asyncio.get_event_loop()

    results = await asyncio.gather(
        loop.run_in_executor(None, lambda: aliexpress.get_products_details([pid])),
        return_exceptions=True
    )

    details = results[0][0] if not isinstance(results[0], Exception) and results[0] else None

    if not details:
        return {"error": "not found"}

    price = float(getattr(details, 'target_sale_price', 0))
    original = float(getattr(details, 'original_price', price))
    rating = str(getattr(details, 'evaluate_rate', '0'))
    sales = "0"
    
    discount_val = round((1 - price/original) * 100) if original > price else 0

    smart = analyze_smart_data(rating, price, original, sales)

    data_out = {
        "title": getattr(details, 'product_title', 'منتج'),
        "image": getattr(details, 'product_main_image_url', ''),
        "price_usd": price,
        "orig_usd": original,
        "discount": discount_val,
        "price_dzd": smart.get("buy_dzd", 0),
        "base_dzd": smart.get("base_dzd", 0),
        "commission": smart.get("commission", 0),
        "sell_dzd": smart.get("sell_dzd", 0),
        "profit_dzd": smart.get("profit_dzd", 0),
        "rating": rating,
        "score": smart.get("score_10", 0),
        "status": smart.get("status", ""),
        "fake_alert": smart.get("fake_alert", "")
    }

    cache[pid] = {"data": data_out, "time": time.time()}

    return data_out

@app.post("/api/comments")
async def add_comment(comment: CommentModel):
    comment_dict = comment.dict()
    comment_dict["date"] = datetime.now().strftime("%Y-%m-%d")
    
    try:
        response = supabase.table("comments").insert(comment_dict).execute()
        return {"message": "Success", "data": response.data}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/comments")
async def get_comments():
    try:
        response = supabase.table("comments").select("*").order("id", desc=True).limit(50).execute()
        return response.data
    except Exception as e:
        return []
