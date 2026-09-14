import streamlit as st

st.title("🇺🇸 미국")

# 미국에 대한 설명
st.write(
    "미국은 북아메리카에 위치한 나라로, 수도는 워싱턴 D.C.입니다. "
    "넓은 국토에 다양한 문화와 자연환경이 공존합니다."
)
st.write(
    "뉴욕의 도시 풍경, 그랜드 캐니언의 웅장한 지형, 하와이의 해변 등 "
    "지역마다 서로 다른 여행의 매력을 만나볼 수 있습니다."
)

# 외부 사이트로 이동할 때는 st.link_button을 사용합니다.
st.link_button("미국 공식 사이트 방문 ↗", url="https://www.usa.gov/visit-united-states")
st.caption("USAGov · 미국 정부의 방문객 안내")
