import streamlit as st

def inject_css():
    st.markdown("""<style>
    .fade-in { animation: fadeIn 1s ease-out; }
    </style>""", unsafe_allow_html=True)
