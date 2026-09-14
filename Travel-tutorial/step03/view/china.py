import streamlit as st

st.title("🇨🇳 중국")

# 중국에 대한 설명
st.write(
    "중국은 동아시아에 위치한 나라로, 수도는 베이징입니다. "
    "오랜 역사와 다양한 지역 문화, 풍부한 자연경관을 만나볼 수 있습니다."
)
st.write(
    "대표적인 관광 명소로는 만리장성과 베이징의 자금성이 있으며, "
    "전통 공예와 지역별 음식도 중국 여행의 매력입니다."
)

# 외부 사이트로 이동할 때는 st.link_button을 사용합니다.
st.link_button("중국 공식 관광 사이트 방문 ↗", url="https://www.travelchina.org.cn/en")
st.caption("Travel China · 중국 문화여유부 공식 관광 사이트")
