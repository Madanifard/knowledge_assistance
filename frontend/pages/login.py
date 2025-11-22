# pages/2_ورود.py
import streamlit as st
from utils.auth import api_request

st.set_page_config(page_title="ورود", page_icon="key")
st.title("ورود به حساب کاربری")

if st.session_state.get("logged_in"):
    st.switch_page("pages/dashboard.py")

with st.form("login_form"):
    username = st.text_input("نام کاربری")
    password = st.text_input("رمز عبور", type="password")

    if st.form_submit_button("ورود"):
        if not username or not password:
            st.error("همه فیلدها الزامی هستند.")
        else:
            with st.spinner("در حال ورود..."):
                result = api_request(
                    method="POST",
                    endpoint="/auth/login",
                    form_data={"username": username, "password": password}
                )

            if result:
                token = result.get("access_token") 
                if token:
                    # ذخیره توکن و اطلاعات
                    st.session_state.jwt_token = token
                    st.session_state.user_info = {"username": username}
                    st.session_state.logged_in = True

                    st.success("ورود موفق!")
                    st.balloons()

                    # ریدایرکت فوری (مهم!)
                    st.switch_page("pages/dashboard.py")
                else:
                    st.error("توکن دریافت نشد. پاسخ سرور: " + str(result))
            else:
                st.error("ورود ناموفق. لطفاً دوباره تلاش کنید.")
