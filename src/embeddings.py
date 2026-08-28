"""
embeddings.py - نفس المحرك لكن جاهز لـ Qdrant
"""
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name: str = "intfloat/multilingual-e5-base"):
        print(f"⏳ تحميل {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ جاهز - الأبعاد: {self.dim}")

    def encode(self, text: str, is_query: bool = True) -> list:
        """ترجع list عشان Qdrant يحب list"""
        prefix = "query: " if is_query else "passage: "
        vec = self.model.encode(prefix + text, normalize_embeddings=True)
        return vec.tolist()

    def encode_batch(self, texts: list[str]) -> list[list]:
        formatted = [f"passage: {t}" for t in texts]
        vectors = self.model.encode(formatted, normalize_embeddings=True, show_progress_bar=True)
        return vectors.tolist()
