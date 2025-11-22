import streamlit as st
from utils.auth import api_request

st.set_page_config(page_title="ثبت نام", page_icon="register")

st.title("ثبت نام کاربر جدید")

with st.form("register_form"):
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("نام کاربری", placeholder="فقط حروف، عدد و _")
    with col2:
        email = st.text_input("ایمیل", placeholder="example@gmail.com")

    password = st.text_input("رمز عبور", type="password")
    password2 = st.text_input("تکرار رمز عبور", type="password")

    submit = st.form_submit_button("ثبت نام کن")

    if submit:
        if not all([email, username, password]):
            st.error("همه فیلدها الزامی هستند.")
        elif password != password2:
            st.error("رمزهای عبور مطابقت ندارند.")
        elif len(password) < 6:
            st.error("رمز عبور باید حداقل ۶ کاراکتر باشد.")
        else:
            data = {
                "email": email,
                "username": username,
                "password": password
            }
            with st.spinner("در حال ثبت نام..."):
                result = api_request(
                    method="POST",
                    endpoint="/auth/register",
                    json_data={
                        "email": email,
                        "username": username,
                        "password": password
                    }
                )
            if result:
                st.success("ثبت نام با موفقیت انجام شد!")
                st.balloons()
                st.info("حالا می‌توانید وارد شوید.")

if st.button("برو به صفحه ورود"):
    st.switch_page("pages/login.py")
