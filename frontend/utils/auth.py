import streamlit as st
import requests
import jwt
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

def api_request(method: str, endpoint: str, form_data=None, json_data=None, token=None, files=None):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Accept": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    if files:
        data = form_data
        json = None
    else:
        if form_data:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data = form_data
            json = None
        elif json_data:
            headers["Content-Type"] = "application/json"
            json = json_data
            data = None
        else:
            data = None
            json = None

    try:
        response = requests.request(
            method.upper(),
            url=url,
            data=data,
            json=json,
            headers=headers,
            files=files,
            timeout=15
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def is_logged_in():
    token = st.session_state.get("jwt_token")
    if not token:
        return False

    try:
        payload = jwt.decode(
            token,
            options={
                "verify_signature": False,
                "verify_exp": True,
                "verify_aud": False
            }
        )
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.now():
            st.warning("جلسه شما منقضی شده است.")
            logout()
            return False
        return True
    except Exception as e:
        if os.getenv("ENVIRONMENT") == "development":
            st.sidebar.error(f"خطا در توکن: {e}")
        logout()
        return False


def logout():
    for key in ["jwt_token", "user_info", "logged_in"]:
        st.session_state.pop(key, None)


def get_current_user():
    return st.session_state.get("user_info") if is_logged_in() else None