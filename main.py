from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
import aiohttp
import base64
import os

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

class LinkRequest(BaseModel):
    url: str

class PayPalOrderRequest(BaseModel):
    amount: float

class PayPalCaptureRequest(BaseModel):
    order_id: str
    product_details: dict

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "AaHJFucxlQ3jgNa2irfUpqcYI7quQKmxJ6twO9yeMF4qX1jAaPyEG7ZZuzbjql9PrS9y-Gm1pSgCAO43")
PAYPAL_SECRET_KEY = os.getenv("PAYPAL_SECRET_KEY", "EORCv4q-T0alR6yMxfE-6mAPl2lKyJjjMbOdwDCRrpJl5YGajbv5CSWKMSMqkGUrY5eEKA5ZaZuNmyKf")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://axbrosibywcdxwlbjyqv.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF4YnJvc2lieXdjZHh3bGJqeXF2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY4NzE1MDAsImV4cCI6MjA5MjQ0NzUwMH0.hXs9aFZ_GZzb1TGkk0lU1WpLL1fE_EohO1enS7H8Itc")

def get_paypal_basic_auth():
    auth_str = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET_KEY}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    return {"Authorization": f"Basic {b64_auth}"}

async def get_paypal_access_token():
    async with aiohttp.ClientSession() as session:
        url = "https://api-m.paypal.com/v1/oauth2/token"
        headers = get_paypal_basic_auth()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {"grant_type": "client_credentials"}
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                return result["access_token"]
            return None

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

    smart = analyze_smart_data(rating, price, original, sales)

    data_out = {
        "title": getattr(details, 'product_title', 'منتج'),
        "image": getattr(details, 'product_main_image_url', ''),
        "price_usd": price,
        "price_dzd": smart.get("buy_dzd", 0),
        "base_dzd": smart.get("base_dzd", 0),
        "commission": smart.get("commission", 0),
        "rating": rating,
        "score": smart.get("score_10", 0),
        "status": smart.get("status", ""),
        "fake_alert": smart.get("fake_alert", "")
    }

    cache[pid] = {"data": data_out, "time": time.time()}

    return data_out

@app.post("/api/paypal/create-order")
async def create_paypal_order(req: PayPalOrderRequest):
    token = await get_paypal_access_token()
    if not token:
        return {"error": "Failed to authenticate with PayPal"}

    async with aiohttp.ClientSession() as session:
        paypal_api_url = "https://api-m.paypal.com/v2/checkout/orders"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(req.amount)
                    }
                }
            ]
        }
        
        async with session.post(paypal_api_url, json=payload, headers=headers) as resp:
            data = await resp.json()
            if resp.status not in (200, 201):
                return {"error": data}
            return {"id": data["id"]}

@app.post("/api/paypal/capture-order")
async def capture_paypal_order(req: PayPalCaptureRequest):
    token = await get_paypal_access_token()
    if not token:
        return {"success": False, "error": "Failed to authenticate with PayPal"}

    async with aiohttp.ClientSession() as session:
        paypal_api_url = f"https://api-m.paypal.com/v2/checkout/orders/{req.order_id}/capture"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        async with session.post(paypal_api_url, headers=headers) as resp:
            data = await resp.json()
            if resp.status not in (200, 201) or data.get("status") != "COMPLETED":
                return {"success": False, "error": data}
            
            # Save order to Supabase securely from backend
            supabase_headers = {
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            payer_name = data.get("payer", {}).get("name", {})
            full_name = f"{payer_name.get('given_name', '')} {payer_name.get('surname', '')}".strip() or "PayPal User"
            payer_email = data.get("payer", {}).get("email_address", "Unknown")

            order_payload = {
                "customer_name": req.product_details.get("customer_name", full_name),
                "customer_contact": payer_email,
                "type": req.product_details.get("type", "AliExpress"),
                "product_details": req.product_details,
                "amount_dzd": req.product_details.get("amount_dzd", 0),
                "status": "Pending" 
            }
            
            async with session.post(f"{SUPABASE_URL}/rest/v1/orders", json=order_payload, headers=supabase_headers) as sb_resp:
                sb_data = await sb_resp.json()
                if sb_resp.status in (200, 201) and sb_data:
                    order_db_id = sb_data[0]["id"]
                    
                    payment_payload = {
                        "order_id": order_db_id,
                        "method": "PayPal",
                        "reference": data.get("id"),
                        "amount_dzd": req.product_details.get("amount_dzd", 0),
                        "status": "Verified"
                    }
                    await session.post(f"{SUPABASE_URL}/rest/v1/payments", json=payment_payload, headers=supabase_headers)

            return {"success": True, "data": data}
