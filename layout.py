import streamlit as st
from ui.styles import inject_css

def setup_page():
    st.set_page_config(page_title="PassGuard", page_icon="🔒", layout="wide")
    inject_css()
    theme = st.sidebar.selectbox("🌗 Tema", ["Gelap", "Cerah"], index=0)
    st._config.set_option("theme.base", "light" if theme == "Cerah" else "dark")

def render_header():
    st.markdown('<h1 class="typing-title fade-in">🔒 PassGuard</h1>', unsafe_allow_html=True)
