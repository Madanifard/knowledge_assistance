import streamlit as st
from utils.auth import is_logged_in

st.set_page_config(page_title="اپلیکیشن من",
                   page_icon="rocket", layout="centered")

if is_logged_in():
    st.switch_page("pages/dashboard.py")
else:
    st.title("به اپلیکیشن خوش آمدید!")
    st.markdown("### لطفاً وارد حساب کاربری خود شوید یا ثبت‌نام کنید.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ثبت نام", use_container_width=True):
            st.switch_page("pages/register.py")
    with col2:
        if st.button("ورود", use_container_width=True):
            st.switch_page("pages/login.py")
