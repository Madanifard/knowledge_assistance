import streamlit as st
from utils.auth import api_request
from utils.auth import is_logged_in


if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()
    
st.title("آپلود فایل")

user_id = st.number_input("User ID", min_value=1, step=1)
category_id = st.number_input("Category ID", min_value=1, step=1)
uploaded_file = st.file_uploader("انتخاب فایل", type=["pdf", "md", "docx"])

if st.button("آپلود"):
    if uploaded_file:
        result = api_request(
            "POST",
            endpoint="/documents/upload/",
            files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
            form_data={"user_id": user_id, "category_id": category_id}
        )
        st.success(result)
    else:
        st.error("فایلی انتخاب نشده است.")
