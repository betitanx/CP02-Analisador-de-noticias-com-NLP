import streamlit as st

from interface import home, analysis

st.set_page_config(
    page_title="Analisador de Notícias NLP",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "🏠 Início": home,
    "🔍 Análise de Notícia": analysis,
}

st.sidebar.title("📰 Analisador de Notícias com NLP")
st.sidebar.markdown("---")
selected = st.sidebar.radio("Navegação", list(PAGES.keys()))
st.sidebar.markdown("---")
st.sidebar.caption("CP02 — Frontend e NLP · FIAP 2026")

PAGES[selected].render()
