from pathlib import Path

import streamlit as st
from src.components.travel_info import TRAVEL_INFO


IMAGE_DIR = Path(__file__).resolve().parents[2] / "assets" / "images"
IMAGE_CAPTIONS = {
    "korea": "63빌딩이 보이는 서울 전경",
    "japan": "도쿄의 상징, 도쿄타워",
    "china": "도시의 불빛이 수놓은 충칭의 야경",
    "usa": "뉴욕 맨해튼의 도심 풍경",
}


def render_country_page(*, flag, name, capital, description,
                        attractions, image_name, travel_url, travel_label):
    """모든 나라가 함께 사용하는 소개 화면입니다."""
    st.title(f"{flag} {name}")

    # 이미지가 없어도 앱을 사용할 수 있습니다.
    image_path = next(
        (IMAGE_DIR / f"{image_name}{suffix}"
         for suffix in (".jpg", ".jpeg", ".png", ".webp")
         if (IMAGE_DIR / f"{image_name}{suffix}").is_file()),
        None,
    )
    if image_path:
        # 세로 사진도 화면을 과도하게 차지하지 않도록 원본 비율로 표시합니다.
        st.html("<style>[data-testid='stImage'] img {max-height: 520px; object-fit: contain;}</style>")
        st.image(str(image_path), caption=IMAGE_CAPTIONS.get(image_name, f"{name} 둘러보기"), width="stretch")
    else:
        st.info(f"{name} 여행 사진을 준비 중입니다.")

    st.write(description)

    st.caption(f"수도 · {capital}")
    st.subheader("여행 기본 정보")
    info = TRAVEL_INFO[image_name]
    for row_start in (0, 2):
        columns = st.columns(2)
        for column, (label, value, detail) in zip(columns, info[row_start:row_start + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f"**{label}**")
                    st.markdown(f"**{value}**")
                    st.write(detail)

    st.subheader("추천 여행지")
    for place, detail in attractions:
        st.markdown(f"**{place}** — {detail}")

    st.divider()
    st.link_button(travel_label, travel_url, type="primary")
