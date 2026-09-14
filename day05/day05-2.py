# OpenAI + streamlit 앱
# 질문 하나 입력하면 OpenAI chat에서 Completions API 한번 호출
# 답변을 받아오는 가장 단순한 방법
# 대화 기록을 기억하지 않는 단발성 질문-답변
# Streamlit run day05-2.py

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="나의 첫번째 챗봇", page_icon="🤖")

st.title("🤖 예제1)나의 첫번째 챗봇")

st.caption("질문 하나 입력하면 OpenAI chat Completions API 한번 호출, 답변을 받아오는 가장 단순한 방법")

# ----------사이드바 api 모델-----------

with st.sidebar:
        st.header("설정")
        api_key = st.text_input("OpenAI API Key", type="password", help="sk-로 시작하는 OpenAI API Key 를 입력하세요")
        model = st.selectbox("모델 선택",["gpt-4o-mini","gpt-4o", "gpt-4.1-mini"], index=0)
        st.markdown("[API 발급받기](https://platform.openai.com/api-keys)")


# -----------메인 화면-----------------

question = st.text_input("질문을 입력하세요", placeholder="예) 오늘 날씨가 어떤가요")


st.markdown("""
<style>
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.5rem;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca);
    color: white;
}
div.stButton > button[kind="primary"]:focus-visible {
    outline: 3px solid #a78bfa;
    outline-offset: 3px;
}
</style>
""", unsafe_allow_html=True)

if st.button("질문하기", type="primary"):
        if not api_key.strip():
            st.error("OpenAI API Key를 입력하세요.")
        elif not question.strip():
            st.error("질문을 입력하세요.")
        else:
            try:
                # 질문을 입력 받으면 "답변을 생각하는 중.." 표시
                with st.spinner("답변을 생각하는 중.."):
                    with OpenAI(api_key=api_key.strip(), max_retries=0, timeout=30.0) as client:
                        response = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": "당신은 친절한 답변가입니다. 답변은 반드시 '주인님'으로 시작하고 한국어로 친절하게 설명하세요."},
                                {"role": "user", "content": question.strip()},
                            ],
                        )

                answer = (response.choices[0].message.content or "").strip()
                if answer:
                    if not answer.startswith("주인님"):
                        answer = "주인님, " + answer
                    st.subheader("답변")
                    st.markdown(answer)
                else:
                    st.warning("텍스트 답변을 받지 못했습니다.")

                # 사용한 토큰수 표시: 입력토큰, 출력토큰, 총토큰수
                st.subheader("이번 질문의 토큰 사용량")
                if response.usage is not None:
                    input_col, output_col, total_col = st.columns(3)
                    input_col.metric("입력 토큰", response.usage.prompt_tokens)
                    output_col.metric("출력 토큰", response.usage.completion_tokens)
                    total_col.metric("총 토큰", response.usage.total_tokens)
                else:
                    st.info("이번 응답에는 토큰 사용량 정보가 없습니다.")
            except Exception:
                # 오류가 있으면 메시지 출력 (API 키 등 민감한 정보는 표시하지 않음)
                st.error("오류가 발생했습니다. API 키, 모델 사용 권한, API 잔액 및 네트워크 연결을 확인하세요.")
