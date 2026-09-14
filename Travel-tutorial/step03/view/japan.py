import streamlit as st

st.title("🇯🇵 일본")

# 일본에 대한 설명
st.write(
    "일본은 동아시아의 섬나라로, 수도는 도쿄입니다. "
    "전통적인 사찰과 현대적인 도시, 사계절의 자연 풍경을 함께 즐길 수 있습니다."
)
st.write(
    "도쿄의 도심, 교토의 전통 거리, 후지산 등이 잘 알려져 있으며, "
    "지역별 음식과 온천도 일본 여행의 매력입니다."
)

# 외부 사이트로 이동할 때는 st.link_button을 사용합니다.
st.link_button("일본 공식 관광 사이트 방문 ↗", url="https://www.japan.travel/en/")
st.caption("Travel Japan · 일본정부관광국(JNTO) 공식 관광 사이트")
