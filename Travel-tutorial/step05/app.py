import streamlit as st

# 1. 앱의 기본 화면을 설정합니다.
st.set_page_config(page_title="세계 여행 포털", page_icon="🌏", layout="wide")

# 2. 나라별 페이지를 메뉴에 등록합니다.
pages = [
    st.Page("src/views/home.py", title="홈 · 대한민국", icon="🇰🇷", default=True),
    st.Page("src/views/china.py", title="중국", icon="🇨🇳"),
    st.Page("src/views/japan.py", title="일본", icon="🇯🇵"),
    st.Page("src/views/usa.py", title="미국", icon="🇺🇸"),
]

# 3. 기본 메뉴를 숨기고 제목 아래에 국가 선택 메뉴를 표시합니다.
navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.title("🌏 세계 여행 포털")
    st.caption("나라를 선택하고 다음 여행을 준비해 보세요.")
    for page in pages:
        st.page_link(page, label=page.title, icon=page.icon)

navigation.run()
