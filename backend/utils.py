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
Aşağıda sahibinden.com’dan alınmış bir ilan metni bulunmaktadır. 
Lütfen kendinizi bir ürün inceleme uzmanı olarak düşünün ve ilanı 
aşağıdaki kriterlere göre **tarafsız, bilgilendirici ve mümkün olduğunca somut** şekilde değerlendirin. 
Amacınız ürünü övmek veya kötülemek değil, alıcıya mantıklı bir fikir sunmaktır. 
Yanıt formatına kesinlikle sadık kalın.

Yanıt formatı:

Teknik Özellikler:
(ilanda teknik özellik varsa belirt yoksa yazmana gerek yok)
- [1–2 cümleyle, ürünün teknik yeterliliğini ve öne çıkan özelliklerini açıkla]
- Puan: X/10

Kronik Sorunlar:
- Ürünü araştır ve yaygın bilinen kronik sorunları belirt.
- [Varsa bilinen kronik sorunları 1–2 cümleyle özetle. Yoksa “Belirgin kronik sorun bilinmiyor” yaz.]

Genel Değerlendirme:
- [2–4 cümlelik kısa ama anlamlı yorum; fiyat/performans, ilan açıklığının yeterliliği ve alıcı için dikkat edilmesi gereken noktaları vurgula]
- Puan: XX/100

İlan Metni:
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
