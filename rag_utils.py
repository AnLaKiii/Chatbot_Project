import chromadb
from sentence_transformers import SentenceTransformer

# Embedding modeli ve yeni Chroma istemcisi
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="film_embeds")

def en_iyi_filmleri_getir(soru, top_k=None):
    """
    Kullanıcı sorgusunu embed edip en alakalı film açıklamalarını ChromaDB üzerinden getirir.
    """
    embedding = model.encode(soru).tolist()
    if top_k is None:
        all_ids = collection.get()["ids"]
        top_k = len(all_ids)
    results = collection.query(query_embeddings=[embedding], n_results=top_k)

    filmler = []
    for i in range(len(results["ids"][0])):
        plot = results["documents"][0][i]
        title = results["metadatas"][0][i].get("title", "")
        category = results["metadatas"][0][i].get("category", "")
        filmler.append({"film_title": title, "plot": plot, "category": category})
    return filmler
