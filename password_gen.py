import streamlit as st
import secrets, string

def password_generator():
    length = st.slider("Length", 8, 32, 16)
    if st.button("Generate"):
        chars = string.ascii_letters + string.digits
        st.success(''.join(secrets.choice(chars) for _ in range(length)))
