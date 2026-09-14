import streamlit as st

st.title("🇰🇷 대한민국")

# 대한민국에 대한 설명
st.write(
    "대한민국은 동아시아의 한반도 남부에 위치한 나라로, 수도는 서울입니다. "
    "전통문화와 현대적인 도시 풍경을 함께 만날 수 있습니다."
)
st.write(
    "서울의 고궁, 부산의 바다, 제주의 자연 등 다양한 명소가 있으며, "
    "지역별 음식과 문화도 한국 여행의 매력입니다."
)

# 외부 사이트로 이동할 때는 st.link_button을 사용합니다.
st.link_button("한국 공식 관광 사이트 방문 ↗", url="https://korean.visitkorea.or.kr/")
st.caption("대한민국 구석구석 · 한국관광공사 공식 여행 정보 사이트")
