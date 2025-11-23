import streamlit as st
from utils.auth import is_logged_in
from utils.auth import api_request

if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()

st.title("❌ Delete Category")

categories = api_request("GET", "/categories/")
category_dict = {f"{c['id']} - {c['name']}": c["id"] for c in categories}

selected = st.selectbox("Select Category", list(category_dict.keys()))

if st.button("Delete"):
    cid = category_dict[selected]
    api_request("DELETE", f"/categories/{cid}/")
    st.error("Category deleted!")
