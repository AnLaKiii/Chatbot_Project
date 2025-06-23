import pandas as pd
from gemini_interface import film_sorusu_cevapla

def en_uygun_film_onerileri(soru, csv_yolu='film_verisi.csv', top_n=5):
    try:
        df = pd.read_csv(csv_yolu)

        if 'film_title' not in df.columns or 'plot' not in df.columns:
            return ["CSV dosyasında 'film_title' ve 'plot' sütunları bulunmalıdır."]
        
        # Her film için Gemini'a anlamlılık sorgusu gönder
        cevaplar = []
        for _, row in df.iterrows():
            film_adi = row['film_title']
            ozet = row['plot']
            film_bilgisi = f"Film Adı: {film_adi}\nKonusu: {ozet}"
            
            yanit = film_sorusu_cevapla(soru, film_bilgisi)
            if yanit:
                # Basit bir puanlama: "Bu film önerilir" vb. içeriyor mu?
                puan = 1 if "önerebilirim" in yanit.lower() or "uygun" in yanit.lower() else 0
                cevaplar.append((film_adi, yanit, puan))
        
        # Puanlara göre sırala
        cevaplar = sorted(cevaplar, key=lambda x: x[2], reverse=True)
        return cevaplar[:top_n]

    except Exception as e:
        return [f"Hata oluştu: {str(e)}"]
