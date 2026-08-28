# Ask Khaitan v2 - محرك بحث دلالي عربي مع Qdrant

هذا هو المشروع النهائي اللي يفرقك عن طلاب Kodyklod. نفس فكرة Ask Warren لكن للداتا المحلية في خيطان والكويت.

## 🎯 الفكرة المختلفة
بدل ما نجيب كلام Warren Buffett، بنجيب مشاكل الناس الحقيقية في خيطان:
"ابي شقة رخيصة في خيطان" -> يفهم المعنى ويرجع الأقرب حتى لو الكلمات مختلفة.

## 🆚 الفرق بين v1 و v2 (التعديلات النهائية)

| v1 (القديم) | v2 (النهائي - هذا المشروع) |
|---|---|
| In-Memory Numpy - يضيع بعد ما تقفل البرنامج | **Qdrant Vector DB - تخزين دائم وسريع** |
| 15 مثال فقط | **20 مثال واقعي مع price و location** |
| بحث بدون فلترة | **بحث + فلترة بالتصنيف والموقع** |
| CLI فقط | **API + واجهة Streamlit + CLI** |
| لا يصلح للبيع | **جاهز للـ Deployment والبيع كخدمة** |

## 🧠 المعادلات النهائية المستخدمة
1. **Embedding:** `vec = E5(text)` normalized
2. **Search in Qdrant:** `score = cosine(q_vec, doc_vec) = q·d`
3. **مع فلترة:** `Filter(category=عقار) + TopK`

## 📁 الهيكل النهائي
```
ask-khaitan-v2/
├── src/
│   ├── embeddings.py      # تحويل النص لمتجه
│   ├── qdrant_setup.py    # اتصال Qdrant
│   ├── ingest.py          # رفع الداتا (شغله مرة واحدة)
│   └── search_qdrant.py   # محرك البحث النهائي
├── api/main.py            # FastAPI - يحول المشروع لـ API
├── ui/app_streamlit.py    # واجهة ويب جميلة
├── data/khaitan_dataset.json
└── requirements.txt
```

## 🚀 خطة التشغيل النهائية - 3 خطوات

### الخطوة 1: احصل على Qdrant مجانا (دقيقتين)
1. روح https://cloud.qdrant.io
2. اعمل حساب مجاني + Create Cluster
3. انسخ URL و API Key وحطهم في ملف `.env`
```bash
cp .env.example .env
# افتح .env وحط بياناتك
```

### الخطوة 2: رفع الداتا
```bash
pip install -r requirements.txt
python -m src.ingest
# هيرفع 20 عنصر لخيطان لـ Qdrant
```

### الخطوة 3: شغل البحث
**جرب CLI:**
```bash
python -m src.search_qdrant
```

**شغل API (للبيع):**
```bash
uvicorn api.main:app --reload
# افتح http://localhost:8000/docs
```

**شغل الواجهة الجميلة:**
```bash
streamlit run ui/app_streamlit.py
```

## 💼 كيف تستخدمه في الوظيفة؟
في الانترفيو قول:
"بنيت محرك بحث دلالي عربي للسوق الكويتي باستخدام multilingual-e5 و Qdrant مع دعم الفلترة والـ API. مختلف عن مشاريع Warren لأنه يحل مشكلة محلية حقيقية ويدعم العربي العامي."

## 🔜 التطوير القادم (لمشروعك الخاص)
- [ ] اضافة 1000 عقار حقيقي من السوق
- [ ] ربطه بواتساب بوت
- [ ] Hybrid Search: Vector + BM25
- [ ] Deploy على Hugging Face Spaces

Author: Mohamed Foaad - Kodyklod AI Engineer
