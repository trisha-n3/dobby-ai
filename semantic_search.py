# semantic_search.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, documents, top_k=3):

    # Extract just the text for embedding
    doc_texts = [doc["text"] for doc in documents]

    query_embedding = model.encode(query, convert_to_tensor=True)
    doc_embeddings = model.encode(doc_texts, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    results = []
    for i in range(len(documents)):
        results.append({
            "text": documents[i]["text"],
            "source": documents[i]["source"],
            "score": scores[i].item()
        })

    # Sort by score, return top 3
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_k]