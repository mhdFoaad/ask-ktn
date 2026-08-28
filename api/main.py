"""
FastAPI - تحويل محرك خيطان لـ API يصلح للبيع
"""
from fastapi import FastAPI
from pydantic import BaseModel
from src.search_qdrant import KhaitanSearchEngine

app = FastAPI(title="Ask Khaitan API", description="محرك بحث دلالي عربي لخيطان", version="2.0")
engine = KhaitanSearchEngine()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3
    category: str = None  # عقار, خدمات, مطاعم

@app.get("/")
def home():
    return {"message": "Ask Khaitan API شغال 🚀", "usage": "POST /search {query: 'شقة في خيطان'}"}

@app.post("/search")
def search(req: SearchRequest):
    results = engine.search(req.query, top_k=req.top_k, category_filter=req.category)
    return {"query": req.query, "results": results}

# لتشغيل: uvicorn api.main:app --reload
