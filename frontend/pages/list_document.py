import streamlit as st
from utils.auth import api_request
from utils.auth import is_logged_in


if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()
    
st.title("لیست فایل‌ها")

docs = api_request("GET", "/documents/")

if docs:
    for doc in docs:
        st.write(f"ID: {doc['id']} | Name: {doc['name']} | Type: {doc['file_type']}")
else:
    st.warning("فایلی یافت نشد.")