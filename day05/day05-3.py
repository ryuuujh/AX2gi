# 대화 기록을 기억하는 멀티턴 챗봇
# st.session_state 에 대화 기록을 저장해서, 이전 대화 맥락을 기억하는 챗봇
# st.chat_message / st.chat_input 같은 Streamlit의 채팅 전용 위젯을 사용합니다.
# stream=True 옵션으로 답변이 실시간으로 타이핑되듯 출력됩니다.
# streamlit run day05-3.py

# 시스템 메시지를 사용자가 설정 하도록 (사이드바에 시스템 프롬포트(챗봇 역할 설정)사용자 지정 시스템 만들고 "당신은 친절하고 전문적인 AI어시스턴트 입니다." 와 같은 문구를 예로 띄워주기)
# 대화 기록 초기화 버튼

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="대화를 기억하는 챗봇", page_icon="🤖")
st.markdown("""
<style>
.stMainBlockContainer { max-width: 920px; padding-top: 2.5rem; }
[data-testid="stSidebar"] { border-right: 1px solid rgba(139, 120, 190, .18); }
.chat-hero {
    background: linear-gradient(125deg, #25203f, #493579);
    border: 1px solid #66528d; border-radius: 24px;
    padding: 32px; margin-bottom: 26px; color: #fff;
    box-shadow: 0 12px 32px rgba(44, 27, 79, .14);
}
.chat-hero .eyebrow { color: #d3c5fa; font-size: 12px; letter-spacing: .18em; font-weight: 700; }
.chat-hero h1 { color: #fff; font-size: clamp(26px, 4vw, 36px); letter-spacing: -.04em; padding: 12px 0; }
.chat-hero p { color: #e2dbee; margin: 0; line-height: 1.8; font-size: 15px; }
.welcome-card { border: 1px solid rgba(139, 120, 190, .25); border-radius: 18px; padding: 24px; margin-bottom: 20px; }
.welcome-card h3 { font-size: 19px; padding-top: 0; }
.welcome-card p { opacity: .8; line-height: 1.8; margin-bottom: 0; }
[data-testid="stChatMessage"] { border: 1px solid rgba(139, 120, 190, .18); border-radius: 18px; padding: 22px; margin-bottom: 14px; }
[data-testid="stChatMessage"] p { line-height: 1.85; }
[data-testid="stChatInput"] { border: 1px solid #9d85d0; border-radius: 18px; box-shadow: 0 4px 18px rgba(105, 73, 158, .10); }
[data-testid="stMetric"] { border: 1px solid rgba(139, 120, 190, .22); border-radius: 14px; padding: 16px; }
[data-testid="stMetricValue"] { font-size: 25px; }
.stButton > button { border-radius: 12px; }
.stButton > button:hover { border-color: #9d85d0; color: #9d85d0; }
.stButton > button:focus-visible { outline: 3px solid #9d85d0; outline-offset: 3px; }
@media (max-width: 600px) {
    .chat-hero { padding: 24px 20px; }
    [data-testid="stChatMessage"] { padding: 14px; }
    .stMainBlockContainer { padding-top: 1.5rem; }
}
</style>
<div class="chat-hero">
    <div class="eyebrow">YOUR PERSONAL AI · CHAT STUDIO</div>
    <h1>생각을 나누면, 답이 이어집니다.</h1>
    <p>이전 대화를 기억하는 나만의 AI 파트너.<br>궁금한 질문부터 새로운 아이디어까지, 편하게 이야기하세요.</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "usage" not in st.session_state:
    st.session_state.usage = None

with st.sidebar:
    st.subheader("✦ Chat Studio")
    st.caption("나에게 맞는 대화 공간")
    st.divider()
    st.markdown("#### 연결 설정")
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"])
    st.markdown("[API 발급받기](https://platform.openai.com/api-keys)")
    st.caption("● 키 입력됨" if api_key.strip() else "○ API 키를 입력하면 대화를 시작할 수 있어요.")
    st.divider()
    st.markdown("#### 어시스턴트 맞춤 설정")
    system_prompt = st.text_area(
        "시스템 프롬프트 (챗봇 역할 설정)",
        value="당신은 친절하고 전문적인 AI어시스턴트 입니다.",
        placeholder="예: 당신은 친절하고 전문적인 AI어시스턴트 입니다.",
        help="변경한 역할은 다음 질문부터 적용됩니다.",
    )
    st.divider()
    if st.button("↺ 대화 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.usage = None
    st.caption("초기화하면 현재 대화가 지워집니다.")

welcome = st.empty()
if not st.session_state.messages:
    welcome.markdown("""
    <div class="welcome-card">
        <h3>어떤 이야기를 시작해 볼까요?</h3>
        <p>💡 아이디어 · 주말에 할 수 있는 새로운 취미를 추천해 줘.<br>
        ✍️ 글쓰기 · 정중하게 일정을 변경하는 이메일을 써 줘.<br>
        📚 학습 · 어려운 개념을 쉬운 예시로 설명해 줘.</p>
    </div>
    """, unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("무엇이든 물어보세요. 대화를 이어서 기억할게요."):
    if not api_key.strip():
        st.error("OpenAI API Key를 입력하세요.")
    elif not question.strip():
        st.error("질문을 입력하세요.")
    else:
        welcome.empty()
        user_message = {"role": "user", "content": question.strip()}
        with st.chat_message("user"):
            st.markdown(question.strip())
        request_messages = list(st.session_state.messages) + [user_message]
        if system_prompt.strip():
            request_messages.insert(0, {"role": "system", "content": system_prompt.strip()})
        st.session_state.usage = None
        try:
            with st.chat_message("assistant"):
                output = st.empty()
                output.markdown("답변을 생각하는 중..")
                answer = ""
                usage = None
                with OpenAI(api_key=api_key.strip(), max_retries=0, timeout=30.0) as client:
                    with client.chat.completions.create(
                        model=model,
                        messages=request_messages,
                        stream=True,
                        stream_options={"include_usage": True},
                    ) as stream:
                        for chunk in stream:
                            if chunk.usage is not None:
                                usage = chunk.usage
                            if chunk.choices:
                                text = chunk.choices[0].delta.content
                                if text:
                                    answer += text
                                    output.markdown(answer + " ▌")
                if answer:
                    output.markdown(answer)
                    st.session_state.messages.extend([
                        user_message, {"role": "assistant", "content": answer}
                    ])
                else:
                    output.warning("텍스트 답변을 받지 못했습니다.")
                if usage is not None:
                    st.session_state.usage = {
                        "입력 토큰": usage.prompt_tokens,
                        "출력 토큰": usage.completion_tokens,
                        "총 토큰": usage.total_tokens,
                    }
        except Exception:
            output.empty()
            st.error("답변을 완료하지 못했습니다. API 키, 모델 사용 권한, API 잔액 및 네트워크 연결을 확인한 뒤 다시 질문하세요.")

if st.session_state.usage is not None:
    st.caption("최근 답변의 토큰 사용량 (입력에는 이전 대화도 포함됩니다.)")
    for column, (label, value) in zip(st.columns(3), st.session_state.usage.items()):
        column.metric(label, value)




