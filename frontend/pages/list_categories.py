import streamlit as st
from utils.auth import is_logged_in
from utils.auth import api_request

if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()

st.title("📋 List of Categories")

categories = api_request("GET", "/categories/")
st.write(categories)  # debug

if not categories:
    st.warning("No categories found.")
else:
    for c in categories:
        st.write(f"**ID:** {c['id']} — **Name:** {c['name']}")
