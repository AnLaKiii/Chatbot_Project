import google.generativeai as genai
from config import GEMINI_API_KEY
import time
import re

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

def film_sorusu_puanla_bulk(kullanici_sorusu, film_listesi, grup_boyutu=20):
    puanlar = []

    for i in range(0, len(film_listesi), grup_boyutu):
        grup = film_listesi[i:i+grup_boyutu]
        prompt = _hazirla_prompt_puanli(kullanici_sorusu, grup)

        try:
            response = model.generate_content(prompt)
            yanit_metni = response.text.strip()
            puanlar.extend(_parse_puanlar(yanit_metni, len(grup)))
        except Exception as e:
            print(f"Hata: {e}")
            puanlar.extend([0] * len(grup))

        time.sleep(0.2)

    return puanlar

def _hazirla_prompt_puanli(kullanici_sorusu, filmler):
    prompt = f"""
Kullanıcının amacı: Aşağıda verilen açıklamaya gerçekten uyan filmleri bulmak.
\"{kullanici_sorusu}\"

Aşağıda verilen her film için 0 (tamamen alakasız) ile 10 (çok ilgili) arasında bir puan ver.

Kriter:
- Film konusu kullanıcı açıklamasına tematik olarak yakın mı?
- Aynı tarihsel dönem, olay ya da atmosfer var mı?
- Yüzeysel kelime eşleşmeleri yerine anlam benzerliğine odaklan.

Yanıt formatı sadece sıralı puanlar olacak şekilde:
1. <puan>
2. <puan>
...

Filmler:
"""
    for i, film in enumerate(filmler, 1):
        prompt += f"{i}. Başlık: {film['film_title']}\nTür: {film['category']}\nKonu: {film['plot']}\n\n"
    prompt += "\nYanıtlar sadece puan olacak şekilde ver:\n"
    return prompt


def _parse_puanlar(yanit, beklenen_adet):
    satirlar = yanit.strip().splitlines()
    puanlar = []
    for satir in satirlar:
        sayi = re.findall(r"\d+", satir)
        if sayi:
            puanlar.append(min(int(sayi[-1]), 10))
    while len(puanlar) < beklenen_adet:
        puanlar.append(0)
    return puanlar[:beklenen_adet]
