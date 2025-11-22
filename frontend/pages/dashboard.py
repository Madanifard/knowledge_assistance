import streamlit as st
from utils.auth import is_logged_in, get_current_user, logout, api_request


if not is_logged_in():
    st.warning("لطفاً ابتدا وارد شوید.")
    if st.button("برو به ورود"):
        st.switch_page("pages/login.py")
    st.stop()

user = get_current_user()
st.title(f"خوش آمدید {user['username']} عزیز!")

# مثال درخواست محافظت‌شده
# data = api_request("GET", "/api/profile", token=st.session_state.jwt_token)
# if data:
#     st.write("اطلاعات پروفایل:", data)

if st.button("خروج از حساب"):
    logout()
    st.success("با موفقیت خارج شدید.")
    st.rerun()
