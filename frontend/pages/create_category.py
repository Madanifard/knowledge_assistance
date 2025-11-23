import streamlit as st
from utils.auth import is_logged_in
from utils.auth import api_request

if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()

st.title("➕ Create New Category")

name = st.text_input("Category Name")

if st.button("Create"):
    if name.strip() == "":
        st.error("Name cannot be empty")
    else:
        result = api_request("POST", '/categories/', json_data={"name": name})
        st.success(f"Category created: {result}")
