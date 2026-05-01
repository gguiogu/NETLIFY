import asyncio
import aiohttp
import base64
import os

PAYPAL_CLIENT_ID = "AaHJFucxlQ3jgNa2irfUpqcYI7quQKmxJ6twO9yeMF4qX1jAaPyEG7ZZuzbjql9PrS9y-Gm1pSgCAO43"
PAYPAL_SECRET_KEY = "EORCv4q-T0alR6yMxfE-6mAPl2lKyJjjMbOdwDCRrpJl5YGajbv5CSWKMSMqkGUrY5eEKA5ZaZuNmyKf"

async def test_paypal():
    auth_str = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET_KEY}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth}", "Content-Type": "application/json"}
    
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": "USD", "value": "100.00"}}]
    }
    
    async with aiohttp.ClientSession() as session:
        # Test Live
        async with session.post("https://api-m.paypal.com/v2/checkout/orders", json=payload, headers=headers) as resp:
            print("LIVE STATUS:", resp.status)
            print("LIVE RESP:", await resp.text())
            
        # Test Token
        async with session.post("https://api-m.paypal.com/v1/oauth2/token", data={"grant_type": "client_credentials"}, headers={"Authorization": f"Basic {b64_auth}"}) as resp:
            print("TOKEN STATUS:", resp.status)
            print("TOKEN RESP:", await resp.text())

asyncio.run(test_paypal())
