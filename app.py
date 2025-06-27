import streamlit as st
import pandas as pd
from gemini_interface import film_sorusu_puanla_bulk
from concurrent.futures import ThreadPoolExecutor
from rag_utils import en_iyi_filmleri_getir
import time

# Sayfa ayarı
st.set_page_config(page_title="Akıllı Film Önerici", layout="wide")
st.title("🎬 Akıllı Film Önerici")

def kisa_plot(plot, max_len=350):
    return plot[:max_len] + "..." if len(plot) > max_len else plot

st.subheader("Hangi kritere göre öneri istersiniz?")
kriter = st.radio("Kriter seçin:", ["Tür", "Konu"])

kullanici_girdisi = st.text_input("🎯 Türleri gir (virgülle ayır):", "") if kriter == "Tür" else st.text_area("🧠 Konu:", height=100)

if st.button("🎯 Önerileri Getir") and kullanici_girdisi:
    status_kutusu = st.empty()
    status_kutusu.info("Gemini ile puanlama yapılıyor, lütfen bekleyin...")

    filmler = en_iyi_filmleri_getir(kullanici_girdisi)
    grup_boyutu = 100
    start = time.time()

    def gruplara_bol(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def puanla(batch):
        return film_sorusu_puanla_bulk(kullanici_girdisi, batch, grup_boyutu=grup_boyutu)

    puanlar = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        kutular = [st.empty() for _ in range((len(filmler) + grup_boyutu - 1) // grup_boyutu)]
        futures = []

        for i, grup in enumerate(gruplara_bol(filmler, grup_boyutu)):
            kutular[i].info(f"{i+1}. grup işleniyor...")
            futures.append(executor.submit(puanla, grup))

        for i, future in enumerate(futures):
            puanlar.extend(future.result())
            kutular[i].empty()

    status_kutusu.empty()
    st.success(f"⏱️ İşlem süresi: {round(time.time() - start, 2)} saniye")

    puanli_filmler = list(zip(filmler, puanlar))
    sirali = sorted(puanli_filmler, key=lambda x: x[1], reverse=True)
    sirali = [film for film in sirali if film[1] >= 5][:20]

    if sirali:
        st.success(f"🎉 {len(sirali)} film bulundu!")
        for film, puan in sirali:
            st.subheader(f"🎬 {film['film_title']} ({puan}/10)")
            st.markdown(f"🎞️ **Tür:** `{film['category']}`")
            st.markdown(f"📖 **Konu:** {kisa_plot(film['plot'])}")
    else:
        st.warning("❌ Yeterince alakalı film bulunamadı.")
