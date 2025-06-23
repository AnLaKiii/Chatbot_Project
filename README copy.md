# 🎬 Akıllı Film Önerici

Bu proje, kullanıcının girdiği film türü veya konuya göre en uygun filmleri öneren bir yapay zekâ destekli sistemdir. Google Gemini API kullanarak film açıklamaları ile kullanıcı isteğini karşılaştırır ve filmleri 0–10 arasında puanlayarak en alakalı olanları listeler.

## 🚀 Özellikler

- Kullanıcıdan "film türü" veya "konu" kriteri alır.
- `Gemini API` ile filmleri puanlar.
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
├── utils.py              # Alternatif öneri fonksiyonları
├── requirements.txt      # Python bağımlılıkları
├── package.json          # Node.js bağımlılıkları
└── package-lock.json     # Node.js kilit dosyası
```

---

## 🧠 Gereksinimler

### Python (Streamlit uygulaması için)

```bash
pip install -r requirements.txt
```

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

### 1. Film Verisini Oluşturma (isteğe bağlı)

```bash
node imdb_fetcher.js
```

Bu komut çalıştırıldığında `film_verisi.csv` otomatik olarak güncellenir.

### 2. Streamlit Arayüzünü Başlatma

```bash
streamlit run app.py
```

Tarayıcınızda interaktif arayüz otomatik olarak açılır.

---

## 📈 Yapay Zekâ Destekli Öneri

Kullanıcının girdiği açıklama, her film ile karşılaştırılarak bir puan alır (0-10). Bu puanlama `gemini_interface.py` içinde yapılır. En yüksek puanlı filmler öneri listesine girer.

---

## 👨‍💻 Geliştirici Notları

- `ThreadPoolExecutor` ile öneriler paralel hesaplanır.
- Yüksek hız için `grup_boyutu` ayarlanabilir (`app.py` içinde).
- Veri temizliği: `plot` alanı kısa veya boş olan filmler filtrelenir.

---

## 📜 Lisans

Bu proje ISC lisansı ile lisanslanmıştır. Detaylar için `package.json` dosyasına bakabilirsiniz.
