"""
ingest.py - تحويل داتا خيطان لمتجهات وتخزينها في Qdrant
هذا أهم ملف في المشروع
"""
import json, uuid
from pathlib import Path
from .embeddings import EmbeddingModel
from .qdrant_setup import get_qdrant_client, create_collection
from qdrant_client.models import PointStruct

COLLECTION = "khaitan_db"

def load_dataset():
    path = Path(__file__).parent.parent / "data/khaitan_dataset.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ingest():
    print("="*50)
    print("📥 بدء تخزين داتا خيطان في Qdrant")
    print("="*50)
    
    # 1. حمل الداتا
    data = load_dataset()
    texts = [item["text"] for item in data]
    print(f"📄 عدد العناصر: {len(data)}")

    # 2. حولها لمتجهات
    embedder = EmbeddingModel()
    vectors = embedder.encode_batch(texts)

    # 3. اتصل بـ Qdrant
    client = get_qdrant_client()
    create_collection(client, COLLECTION, dim=embedder.dim)

    # 4. حضر النقاط
    points = []
    for i, (item, vec) in enumerate(zip(data, vectors)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vec,
                payload=item # نخزن النص والتصنيف كـ metadata للفلترة
            )
        )

    # 5. ارفع
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"✅ تم رفع {len(points)} نقطة إلى {COLLECTION}")
    print("الآن تقدر تبحث!")

if __name__ == "__main__":
    ingest()
