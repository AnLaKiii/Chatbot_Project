# 🎬 Akıllı Film Önerici

Bu proje, kullanıcının girdiği film türü veya konuya göre en uygun filmleri öneren yapay zekâ destekli bir sistemdir. Google Gemini API ve ChromaDB kullanılarak, film açıklamaları ile kullanıcı isteği karşılaştırılır, puanlanır ve en alakalı filmler listelenir.

## 🚀 Özellikler

- Kullanıcıdan "film türü" veya "konu" kriteri alır.
- `ChromaDB` ile film açıklamaları vektör uzayına yerleştirilir.
- Kullanıcı sorgusu embed edilerek en alakalı filmler geri getirilir (RAG - Retrieval-Augmented Generation).
- `Gemini API` ile bu filmler puanlanır.
- Puanı 5 ve üzeri olan en iyi 20 filmi önerir.
- TMDB API'den otomatik veri çekme ve CSV oluşturma imkanı sağlar (`imdb_fetcher.js`).

---

## 📁 Proje Yapısı

```
├── app.py                 # Streamlit arayüzü (ana uygulama)
├── gemini_interface.py   # Gemini API ile etkileşim
├── config.py             # API anahtar konfigürasyonu
├── imdb_fetcher.js       # TMDB'den film verisi çeken Node.js scripti
├── film_verisi.csv       # Film adı, türü ve konusu içeren veri seti
├── rag_utils.py          # ChromaDB'den film sorgusu yapan yardımcı fonksiyon
├── index_builder.py      # Film açıklamalarını ChromaDB'ye embed eden script
├── requirements.txt      # Python bağımlılıkları
├── package.json          # Node.js bağımlılıkları
└── package-lock.json     # Node.js kilit dosyası
```


---

## 🧠 Gereksinimler

### Python (Streamlit ve öneri motoru için)

```bash
venv\Scripts\activate
pip install -r requirements.txt


### Node.js (Veri çekme işlemi için)

```bash
npm install
```

---

## 🔑 API Anahtarları

### Gemini API

`config.py` dosyasına aşağıdaki gibi anahtar eklenmelidir:

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

### TMDB API

`imdb_fetcher.js` içinde API anahtarınızı aşağıdaki satıra yerleştirin:

```javascript
const TMDB_API_KEY = 'YOUR_TMDB_API_KEY';
```

---

## 🧪 Uygulamayı Çalıştırma

### 1. Film Verilerini ChromaDB'ye Eklemek (İlk kez veya veri güncellendiğinde)

```bash
venv\Scripts\activate

python index_builder.py
```

> Bu komut, `film_verisi.csv` dosyasındaki açıklamaları embed ederek ChromaDB'ye kaydeder.

### 2. Streamlit Arayüzünü Başlatma

```bash
streamlit run app.py
```

> Tarayıcınızda interaktif arayüz otomatik olarak açılır.
![alt text](img/tür.png)

Türüne göre arama işlemi için

![alt text](img/türsonuç.png)

Türüne göre aldığımız sonuç

![alt text](img/konu.png)

Konusuna göre arama işlemi için

![alt text](img/konusonuç.png)

Konusuna göre aldığımız sonuç
---

## 📈 Yapay Zekâ Destekli Öneri

Kullanıcının girdiği açıklama, önce ChromaDB ile karşılaştırılır, en alakalı filmler seçilir. Bu filmler, `gemini_interface.py` içinde 0-10 arası alaka puanı ile değerlendirilir. En yüksek puanlılar öneri listesine girer.

---

## 👨‍💻 Geliştirici Notları

- `ThreadPoolExecutor` ile öneriler paralel hesaplanır.
- Yüksek hız için `grup_boyutu` ayarlanabilir (`app.py` içinde).
- Veri temizliği: `plot` alanı kısa veya boş olan filmler filtrelenir.
- `sentence-transformers` modeli yalnızca gerektiğinde çağrılırsa uygulama daha hızlı başlar.

---
