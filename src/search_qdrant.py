"""
search_qdrant.py - محرك البحث النهائي مع فلترة
"""
from .embeddings import EmbeddingModel
from .qdrant_setup import get_qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue

COLLECTION = "khaitan_db"

class KhaitanSearchEngine:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.client = get_qdrant_client()

    def search(self, query: str, top_k: int = 3, category_filter: str = None):
        """
        بحث دلالي + فلترة اختيارية
        المعادلة: score = cosine(query_vec, doc_vec)
        """
        q_vec = self.embedder.encode(query, is_query=True)

        # فلتر لو المستخدم اختار تصنيف
        query_filter = None
        if category_filter:
            query_filter = Filter(
                must=[FieldCondition(key="category", match=MatchValue(value=category_filter))]
            )

        results = self.client.search(
            collection_name=COLLECTION,
            query_vector=q_vec,
            query_filter=query_filter,
            limit=top_k
        )

        # تحويل النتائج لشكل سهل
        output = []
        for r in results:
            output.append({
                "score": r.score,
                "text": r.payload["text"],
                "category": r.payload["category"],
                "price": r.payload.get("price", ""),
                "location": r.payload.get("location", "")
            })
        return output

if __name__ == "__main__":
    engine = KhaitanSearchEngine()
    print(engine.search("ابي شقة رخيصة في خيطان", top_k=3))
