import streamlit as st

st.set_page_config(page_title="세계 여행 포털", page_icon="🌏")


# 사이드바: 선택한 메뉴에 따라 본문을 바꿉니다.
menu = st.sidebar.radio("메뉴", ["홈", "미국", "중국", "일본"])

if menu == "홈":
    st.title("🌏 세계 여행 포털")
    st.header("🇰🇷 대한민국")
    st.write("대한민국은 동아시아의 한반도 남부에 위치한 나라로, 수도는 서울입니다. 전통문화와 현대적인 도시 풍경을 함께 만날 수 있습니다.")
    st.write("서울의 고궁, 부산의 바다, 제주의 자연 등 다양한 매력이 있습니다.")
    st.info("왼쪽 사이드바에서 미국, 중국, 일본을 선택해 보세요.")

elif menu == "미국":
    st.title("🇺🇸 미국")
    st.write("미국은 북아메리카에 위치한 나라로, 수도는 워싱턴 D.C.입니다. 넓은 국토에 다양한 문화와 자연환경이 공존합니다.")
    st.write("뉴욕의 도시 풍경, 그랜드 캐니언의 웅장한 지형, 하와이의 해변 등이 잘 알려져 있습니다.")
    st.link_button("미국 공식 사이트 방문 ↗", "https://www.usa.gov/visit-united-states")
    st.caption("USAGov · 미국 정부의 방문객 안내")

elif menu == "중국":
    st.title("🇨🇳 중국")
    st.write("중국은 동아시아에 위치한 나라로, 수도는 베이징입니다. 오랜 역사와 넓은 국토를 바탕으로 다양한 문화유산과 자연경관을 지니고 있습니다.")
    st.write("만리장성, 베이징의 자금성, 시안의 병마용 등이 대표적인 명소입니다.")
    st.link_button("중국 공식 사이트 방문 ↗", "https://www.travelchina.org.cn/en")
    st.caption("Travel China · 중국 문화여유부 공식 관광 사이트")

elif menu == "일본":
    st.title("🇯🇵 일본")
    st.write("일본은 동아시아의 섬나라로, 수도는 도쿄입니다. 전통적인 사찰과 현대적인 도시, 사계절의 자연 풍경을 함께 즐길 수 있습니다.")
    st.write("도쿄의 도심, 교토의 전통 거리, 후지산 등이 잘 알려져 있습니다.")
    st.link_button("일본 공식 사이트 방문 ↗", "https://www.japan.travel/en/")
    st.caption("Travel Japan · 일본정부관광국(JNTO) 공식 관광 사이트")
    
