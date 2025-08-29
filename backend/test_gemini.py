import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def test_gemini():
    prompt = "Fiat Tipo 1998 model, 200.000 km, motor yenilenmiş. Bu aracı 0-100 arasında puanla ve kısa bir yorum yap."

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        print("Status Code:", response.status_code)
        try:
            print("Response JSON:", response.json())
        except Exception as e:
            print("Yanıt çözümlenemedi:", e)
            print("Ham yanıt:", response.text)

# Çalıştırmak için
import asyncio
asyncio.run(test_gemini())
