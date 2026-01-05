import streamlit as st

def handle_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.history = []

    st.sidebar.header("🔐 Login")
    user = st.sidebar.text_input("Username")
    if st.sidebar.button("Login") and user:
        st.session_state.logged_in = True
        st.session_state.username = user

def handle_logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
