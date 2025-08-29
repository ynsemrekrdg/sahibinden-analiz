import os
import httpx
import re
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


async def generate_evaluation(data):
    if not GEMINI_API_KEY:
        print("❌ API anahtarı bulunamadı.")
        return {"puan": 0, "yorum": "API anahtarı eksik."}

    prompt = f"""
Aşağıda sahibinden.com’dan satılan bir ilana ait bilgiler yer almaktadır. Lütfen bu bilgileri **ürün açıklaması ve özellikleri üzerinden** değerlendiriniz. 

**ÖNEMLİ:** İlan tarihleriyle ilgili hiçbir yorum yapmayın. Tarihleri dikkate almayın.

Değerlendirme sırasında odaklanmanız gereken kriterler:
- Ürünün açıklığı ve yeterliliği
- Ürün bilgileri ve teknik özelliklerin tutarlılığı
- Ürünün gerçekçiliğe uygunluğu ve güvenilirliği

Bu değerlendirme sonucunda 0–100 arasında bir puan verin. Ardından kullanıcıların dikkat etmesi gereken noktaları maddeler halinde sıralayın. Son olarak 1-2 cümlelik kısa bir genel değerlendirme yapın.

Puanı açıkça belirtin: Örneğin "Puan: 78/100"

{data['metin']}
"""



    headers = { "Content-Type": "application/json" }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            content = response.json()
            text = content["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print("❌ Gemini API hatası:", e)
            text = "AI yanıtı alınamadı."

    temiz_yorum = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    puanlar = re.findall(r"\b([1-9][0-9]?)\b", temiz_yorum)
    puan = int(puanlar[0]) if puanlar else 50

    return {"puan": puan, "yorum": temiz_yorum}
