"""
qdrant_setup.py - الاتصال بـ Qdrant
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

def get_qdrant_client():
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY")
    
    if "localhost" in url:
        print("🔌 اتصال محلي Qdrant")
        return QdrantClient(url=url)
    else:
        print(f"☁️ اتصال سحابي Qdrant: {url}")
        return QdrantClient(url=url, api_key=api_key)

def create_collection(client: QdrantClient, collection_name: str = "khaitan_db", dim: int = 768):
    """ينشئ الـ Collection لو مش موجود"""
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
            # المعادلة المستخدمة هنا: cosine = dot(a,b) / (||a||*||b||)
        )
        print(f"✅ Collection '{collection_name}' تم إنشاؤه - Distance: COSINE")
    else:
        print(f"ℹ️ Collection '{collection_name}' موجود بالفعل")

if __name__ == "__main__":
    client = get_qdrant_client()
    create_collection(client)
