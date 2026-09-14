"""여행 기본 정보. 2026-09-14 확인. 추천 시기는 지역별 기후 안내를 바탕으로 정리."""

# 통화·기후·음식: 한국관광공사 / 일본정부관광국 / 중국 여행 안내 / USAGov
# https://english.visitkorea.or.kr/svc/contents/infoHtmlView.do?vcontsId=140040
# https://english.visitkorea.or.kr/svc/contents/infoBscView.do?vcontsId=140636
# https://english1.visitkorea.or.kr/enu/AKR/AK_ENG_2_3.jsp
# https://www.japan.travel/en/faq/
# https://www.japan.travel/en/guide/november/
# https://www.chinahighlights.com/chongqing/index.htm
# https://english.www.gov.cn/2025special/bizexpatsinchina2025
# https://www.ichongqing.info/2025/07/31/hotpot-heir-stirs-century-long-legacy-with-modern-fire/
# https://www.usa.gov/currency
# https://www.newyork.com/articles/post/the-best-time-to-visit-new-york-city-seasons-months-and-what-to-expect/
# https://www.nyc.gov/mayors-office/news/2022/03/new-york-city-launches-new-get-local-nyc-campaign-inviting-visitors-explore-all-five-boroughs
# 시차: https://www.timeanddate.com/worldclock/converted.html?p1=33&p2=248&p3=235
# https://www.timeanddate.com/time/zone/usa/new-york
# https://www.timeanddate.com/time/zone/usa/los-angeles
# https://www.timeanddate.com/time/zone/usa/honolulu

TRAVEL_INFO = {
    "korea": [
        ("💰 통화", "대한민국 원 · KRW", "기호는 ₩입니다. 지폐는 1천·5천·1만·5만 원권을 사용합니다."),
        ("🌤️ 추천 여행 시기", "봄 3월–5월 · 가을 9월–11월", "도시 산책과 야외 관광에 좋은 계절입니다. 꽃과 단풍 시기는 지역과 해마다 달라집니다."),
        ("🕒 한국과의 시차", "시차 없음 · UTC+9", "전국에서 같은 한국 표준시를 사용합니다. 서울과 부산, 제주 모두 시간이 같습니다."),
        ("🍽️ 대표 음식", "비빔밥 · 불고기 · 한정식", "다양한 재료를 비비는 비빔밥, 양념한 고기를 굽는 불고기, 여러 반찬을 맛보는 한정식이 있습니다."),
    ],
    "japan": [
        ("💰 통화", "일본 엔 · JPY", "기호는 ¥입니다. 중국 위안과 기호가 같으므로 통화 코드 JPY로 구분할 수 있습니다."),
        ("🌤️ 추천 여행 시기", "봄 3월–5월 · 가을 10월–11월", "도쿄·교토의 꽃과 단풍 여행을 기준으로 한 추천입니다. 홋카이도·오키나와는 계절 흐름이 다릅니다."),
        ("🕒 한국과의 시차", "시차 없음 · UTC+9", "한국이 낮 12시면 일본도 낮 12시입니다. 서머타임을 적용하지 않습니다."),
        ("🍽️ 대표 음식", "스시 · 라멘 · 덴푸라", "생선과 밥이 어우러진 스시, 지역별 국물이 다른 라멘, 재료를 바삭하게 튀긴 덴푸라를 즐겨보세요."),
    ],
    "china": [
        ("💰 통화", "중국 위안 · CNY", "중국 본토의 통화는 인민폐(RMB)이며 기본 단위는 위안입니다. 일본 엔과 구분해 주세요."),
        ("🌤️ 추천 여행 시기", "충칭: 3월–5월 · 10월–11월", "사진 속 충칭은 봄·가을 여행을 추천합니다. 중국은 넓어 방문 도시마다 적합한 시기가 다릅니다."),
        ("🕒 한국과의 시차", "한국보다 1시간 느림", "중국 본토의 공식 시간은 UTC+8입니다. 한국이 낮 12시면 베이징·상하이·충칭은 오전 11시입니다."),
        ("🍽️ 대표 음식", "충칭 훠궈", "매콤한 국물에 여러 재료를 익혀 먹는 충칭의 대표 음식입니다. 지역마다 음식의 맛과 조리법이 다릅니다."),
    ],
    "usa": [
        ("💰 통화", "미국 달러 · USD", "기호는 $입니다. 다른 나라의 달러와 구분할 때는 US$ 또는 USD로 표시합니다."),
        ("🌤️ 추천 여행 시기", "뉴욕: 봄·가을", "맨해튼 도심 산책을 기준으로 한 추천입니다. 하와이·사막·국립공원은 목적지별 기후를 살펴보세요."),
        ("🕒 한국과의 시차", "도시·서머타임별로 다름", "한국보다 뉴욕은 14시간(서머타임 13시간), LA는 17시간(16시간) 느립니다. 하와이는 연중 19시간 느립니다."),
        ("🍽️ 대표 음식", "뉴욕식 피자 · 베이글", "사진 속 맨해튼 여행에서 즐기기 좋은 뉴욕의 대표 먹거리입니다. 미국은 지역마다 음식 문화가 다양합니다."),
    ],
}
