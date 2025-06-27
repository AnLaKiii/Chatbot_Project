import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# Embedding modeli
model = SentenceTransformer("all-MiniLM-L6-v2")

# Yeni ChromaDB istemcisi (güncel yapı)
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="film_embeds")

# CSV dosyasını oku
df = pd.read_csv("film_verisi.csv").dropna(subset=["plot"])

# Koleksiyon temizleme (yalnızca veri varsa)
existing_ids = collection.get()["ids"]
if existing_ids:
    collection.delete(ids=existing_ids)

# Embed ve ekle
for i, row in df.iterrows():
    film_id = str(i)
    film = row["film_title"]
    plot = row["plot"]
    embedding = model.encode(plot).tolist()

    collection.add(
        documents=[plot],
        embeddings=[embedding],
        ids=[film_id],
        metadatas=[{"title": film, "category": row.get("category", "")}]
    )

print("✅ Embedding ve ChromaDB yükleme tamamlandı.")
