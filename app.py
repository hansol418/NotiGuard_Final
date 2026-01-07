import streamlit as st
import extra_streamlit_components as stx
import service
from core.db import init_db
from dotenv import load_dotenv
import time

load_dotenv()

st.set_page_config(page_title="그룹웨어 데모", layout="wide")

init_db()

# 세션 기본값
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("role", None)              # "ADMIN" | "EMPLOYEE"
st.session_state.setdefault("employee_id", None)
st.session_state.setdefault("employee_info", None)

# 쿠키 매니저 (키를 주어 리렌더링 방지)
cookie_manager = stx.CookieManager(key="init_cookie_manager")

# 쿠키값 읽기 (약간의 지연 필요할 수 있음)
# stx 특성상 첫 로드 시 쿠키를 다 못 읽어올 수 있으므로
# get_all()을 호출하여 state를 갱신
cookies = cookie_manager.get_all()
user_token = cookies.get("user_token")

# 자동 로그인 시도
if not st.session_state.logged_in and user_token:
    info = service.get_account_info(str(user_token))
    if info:
        st.session_state.logged_in = True
        st.session_state.role = info["role"]
        
        if info["role"] == "ADMIN":
            st.session_state.employee_id = None
            st.session_state.employee_info = None
        else:
            emp = info["employee"]
            if emp:
                st.session_state.employee_id = emp["employeeId"]
                st.session_state.employee_info = emp

# 라우팅
if st.session_state.logged_in:
    if st.session_state.role == "ADMIN":
        st.switch_page("pages/admin.py")
    else:
        st.switch_page("pages/employee.py")
else:
    st.switch_page("pages/0_Login.py")
