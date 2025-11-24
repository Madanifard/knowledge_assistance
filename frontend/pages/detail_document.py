import streamlit as st
from utils.auth import api_request
from utils.auth import is_logged_in


if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()
    
    
st.title("دریافت اطلاعات فایل")

doc_id = st.number_input("Document ID", min_value=1, step=1)

if st.button("جستجو"):
    doc = api_request("GET", f"/documents/{doc_id}/")
    if "id" in doc:
        st.json(doc)
    else:
        st.error("فایل یافت نشد.")