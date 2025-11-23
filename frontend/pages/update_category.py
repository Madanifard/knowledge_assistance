import streamlit as st
from utils.auth import is_logged_in
from utils.auth import api_request

if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()

st.title("✏️ Update Category")

categories = api_request("GET", "/categories/")
category_dict = {f"{c['id']} - {c['name']}": c["id"] for c in categories}

selected = st.selectbox("Select category to update",
                        list(category_dict.keys()))

new_name = st.text_input("New Name")

if st.button("Update"):
    cid = category_dict[selected]
    result = api_request("PUT", f"/categories/{cid}/", json_data={"name": new_name})
    st.success(f"Updated: {result}")
