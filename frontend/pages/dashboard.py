import streamlit as st
from utils.auth import is_logged_in, get_current_user, logout, api_request


if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()

user = get_current_user()
st.title(f"خوش آمدید {user['username']} عزیز!")

col1, col2 = st.columns(2)
with col1:
    if st.button("دسته بندی ها", use_container_width=True):
        st.switch_page("pages/list_categories.py")
with col2:
    if st.button("ورود", use_container_width=True):
        st.switch_page("pages/login.py")

if st.button("خروج از حساب"):
    logout()
    st.success("با موفقیت خارج شدید.")
    st.rerun()
