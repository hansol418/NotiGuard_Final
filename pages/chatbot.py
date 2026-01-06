# STREAMLIT/pages/chatbot.py
import streamlit as st
import service
from core.layout import (
    apply_portal_theme,
    render_topbar,
    portal_sidebar,
    render_floating_widget,
)
from core.chatbot_engine import ChatbotEngine

st.set_page_config(page_title="Chatbot", layout="wide")

# -------------------------
# 로그인 체크
# -------------------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("role", None)
st.session_state.setdefault("employee_id", None)
st.session_state.setdefault("employee_info", None)

if (not st.session_state.logged_in) or (st.session_state.role != "EMPLOYEE"):
    st.switch_page("pages/0_Login.py")

# -------------------------
# 메뉴 변경 핸들러
# -------------------------
def on_menu_change(new_menu: str):
    st.session_state.emp_menu = new_menu

# -------------------------
# 상태값
# -------------------------
st.session_state.setdefault("emp_menu", "챗봇")

# -------------------------
# 테마/사이드바/상단바
# -------------------------
apply_portal_theme(
    hide_pages_sidebar_nav=True,
    hide_sidebar=False,
    active_menu="챗봇",
)

portal_sidebar(role="EMPLOYEE", active_menu="챗봇", on_menu_change=on_menu_change)
render_topbar("전사 Portal")
render_floating_widget(img_path="assets/chatimg_r.png")

# -------------------------
# 챗봇 UI
# -------------------------

# 채팅 히스토리 초기화 (대화 세션)
st.session_state.setdefault("chatbot_sessions", {})  # {session_id: {name, messages}}
st.session_state.setdefault("current_session_id", None)
st.session_state.setdefault("session_counter", 0)

# 엔진 초기화
employee_id = st.session_state.get("employee_id", "guest")
engine = ChatbotEngine(user_id=employee_id)

# 대화 히스토리 관리 함수
def create_new_session():
    """새 대화 세션 생성"""
    st.session_state.session_counter += 1
    session_id = f"session_{st.session_state.session_counter}"
    st.session_state.chatbot_sessions[session_id] = {
        "name": f"대화 {st.session_state.session_counter}",
        "messages": []
    }
    st.session_state.current_session_id = session_id
    return session_id

def delete_session(session_id):
    """대화 세션 삭제"""
    if session_id in st.session_state.chatbot_sessions:
        del st.session_state.chatbot_sessions[session_id]
        # 현재 세션이 삭제된 경우
        if st.session_state.current_session_id == session_id:
            if st.session_state.chatbot_sessions:
                st.session_state.current_session_id = list(st.session_state.chatbot_sessions.keys())[0]
            else:
                st.session_state.current_session_id = None

# 첫 세션이 없으면 생성
if not st.session_state.chatbot_sessions:
    create_new_session()

# 현재 세션이 없으면 첫 세션으로 설정
if st.session_state.current_session_id is None and st.session_state.chatbot_sessions:
    st.session_state.current_session_id = list(st.session_state.chatbot_sessions.keys())[0]

# 레이아웃: 왼쪽 히스토리, 오른쪽 채팅
col_history, col_chat = st.columns([1, 3], gap="medium")

# -------------------------
# 왼쪽: 대화 히스토리
# -------------------------
with col_history:
    st.markdown("### 대화 히스토리")
    
    # 새 대화 버튼
    if st.button("➕ 새 대화", use_container_width=True, type="primary"):
        create_new_session()
        st.rerun()
    
    st.divider()
    
    # 세션 목록
    for session_id, session_data in st.session_state.chatbot_sessions.items():
        is_current = session_id == st.session_state.current_session_id
        
        # 세션 버튼 컨테이너
        session_container = st.container()
        with session_container:
            col_btn, col_del = st.columns([4, 1])
            
            with col_btn:
                button_type = "primary" if is_current else "secondary"
                if st.button(
                    session_data["name"],
                    key=f"session_{session_id}",
                    use_container_width=True,
                    type=button_type if is_current else None,
                ):
                    st.session_state.current_session_id = session_id
                    st.rerun()
            
            with col_del:
                if st.button("🗑️", key=f"delete_{session_id}", help="대화 삭제"):
                    delete_session(session_id)
                    st.rerun()

# -------------------------
# 오른쪽: 채팅
# -------------------------
with col_chat:
    st.markdown("### 🤖 노티가드 AI 챗봇")
    
    # 현재 세션 가져오기
    current_session = st.session_state.chatbot_sessions.get(st.session_state.current_session_id)
    
    if current_session:
        # 챗봇 인사말 및 안내
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 24px; 
                    border-radius: 12px; 
                    margin-bottom: 20px;
                    color: white;">
            <h3 style="margin: 0 0 12px 0; color: white;">👋 안녕하세요!</h3>
            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
                저는 노티가드 AI 챗봇입니다.<br>
                효성전기의 공지사항과 관련된 질문에 답변해 드립니다.<br>
                궁금한 점을 편하게 물어보세요!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 예시 질문 (대화가 없을 때만 표시)
        if len(current_session["messages"]) == 0:
            st.markdown("#### 💡 예시 질문")
            example_questions = [
                "이번 주 안전교육 일정 알려줘",
                "최근 공지사항 요약해줘",
                "휴가 신청 방법 알려줘",
                "복지 제도에 대해 알려줘"
            ]
            
            cols = st.columns(2)
            for i, question in enumerate(example_questions):
                with cols[i % 2]:
                    if st.button(f"💬 {question}", key=f"example_{i}", use_container_width=True):
                        # 예시 질문을 사용자 메시지로 추가
                        current_session["messages"].append({
                            "role": "user",
                            "content": question
                        })
                        
                        # 챗봇 응답 생성
                        with st.spinner("답변 생성 중..."):
                            result = engine.ask(question)
                            response = result["response"]
                            
                            current_session["messages"].append({
                                "role": "assistant",
                                "content": response
                            })
                        
                        st.rerun()
            
            st.divider()
        
        # 채팅 메시지 표시
        chat_container = st.container(height=400, border=True)
        with chat_container:
            if len(current_session["messages"]) == 0:
                st.info("👆 위의 예시 질문을 클릭하거나 아래에 메시지를 입력하세요.")
            else:
                for msg in current_session["messages"]:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
        
        # 채팅 입력창 (채팅 기록 밑에 위치)
        st.markdown("---")
        prompt = st.chat_input("메시지를 입력하세요...", key="chatbot_input")
        
        if prompt:
            # 사용자 메시지 추가
            current_session["messages"].append({
                "role": "user",
                "content": prompt
            })
            
            # 챗봇 응답 생성
            with st.spinner("답변 생성 중..."):
                result = engine.ask(prompt)
                response = result["response"]
                
                current_session["messages"].append({
                    "role": "assistant",
                    "content": response
                })
            
            st.rerun()
        
        # 하단 버튼
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 현재 대화 초기화", use_container_width=True):
                current_session["messages"] = []
                st.rerun()
        with col2:
            if st.button("📧 담당자에게 문의", use_container_width=True):
                st.info("담당자 문의 기능은 준비 중입니다.")
    else:
        st.warning("대화 세션을 선택하거나 새로 만들어주세요.")
