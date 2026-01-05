import streamlit as st
from ui.layout import setup_page, render_header
from auth.session import handle_login, handle_logout
from features.password_check import password_checker
from features.password_gen import password_generator

setup_page()
render_header()

handle_login()

if st.session_state.logged_in:
    handle_logout()

    menu = st.radio("Pilih Fitur", [
        "Cek Kekuatan Password",
        "Generate Password Kuat"
    ])

    if menu == "Cek Kekuatan Password":
        password_checker()
    else:
        password_generator()
else:
    st.info("👈 Silakan login di sidebar untuk mengakses fitur.")
