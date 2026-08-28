"""
Streamlit UI - واجهة جميلة للمشروع
"""
import streamlit as st
from src.search_qdrant import KhaitanSearchEngine

st.set_page_config(page_title="Ask Khaitan", page_icon="🏠", layout="wide")

st.title("🏠 Ask Khaitan - اسأل خيطان")
st.markdown("محرك بحث دلالي يفهم لهجتك، مش بس كلماتك")

@st.cache_resource
def load_engine():
    return KhaitanSearchEngine()

engine = load_engine()

query = st.text_input("🔍 اكتب سؤالك", placeholder="مثال: ابي شقة غرفتين رخيصة قريبة من المطار")

category = st.selectbox("فلتر (اختياري)", ["الكل", "عقار", "خدمات", "مطاعم", "صحة"])
top_k = st.slider("عدد النتائج", 1, 10, 3)

if query:
    cat_filter = None if category == "الكل" else category
    with st.spinner("جاري البحث في خيطان..."):
        results = engine.search(query, top_k=top_k, category_filter=cat_filter)
    
    st.success(f"لقيت {len(results)} نتائج")
    for i, res in enumerate(results, 1):
        with st.container():
            st.markdown(f"### {i}. {res['text']}")
            st.markdown(f"**التصنيف:** {res['category']} | **الموقع:** {res.get('location','خيطان')} | **Score:** `{res['score']:.4f}`")
            if res.get('price'):
                st.markdown(f"💰 **السعر:** {res['price']}")
            st.divider()

st.sidebar.markdown("### كيف يعمل؟")
st.sidebar.markdown("""
1. سؤالك يتحول لمتجه `q` بطول 768
2. نحسب $cosine(q, d)$ مع كل شيء في Qdrant
3. نرجع الأعلى
""")
