import streamlit as st
from zxcvbn import zxcvbn

def password_checker():
    pwd = st.text_input("Password", type="password")
    if pwd:
        result = zxcvbn(pwd)
        st.write("Score:", result["score"])
