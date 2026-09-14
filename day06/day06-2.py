"""실행: python -m streamlit run day06/day06-2.py"""
import os
import importlib
from pathlib import Path
from urllib.parse import urlencode

import pydeck as pdk
import streamlit as st
from dotenv import dotenv_values
import travel_search

# Streamlit 재실행 시 메모리에 남은 이전 함수 대신 최신 모듈을 사용한다.
travel_search = importlib.reload(travel_search)

st.set_page_config(page_title="여행 준비 도우미", page_icon="✈️", layout="wide")
st.html("""
<style>
/* 밝은 아이보리, 민트, 살구색을 사용한 여행 대시보드 */
.stApp {
    background: radial-gradient(ellipse at 95% 0%, #dff3e9 0%, transparent 45%),
                radial-gradient(ellipse at 0% 85%, #fff0e2 0%, transparent 45%), #f8faf6;
    color: #24364b;
    color-scheme: light;
    --primary-color: #0f766e;
    --text-color: #24364b;
    --background-color: #f8faf6;
    --secondary-background-color: #ffffff;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #edf6ef, #f7faf5);
    border-right: 1px solid #dce8df;
}
[data-testid="stMainBlockContainer"] { padding-top: 2.5rem; padding-bottom: 3rem; }
.stApp h1, .stApp h2, .stApp h3 { color: #183247; letter-spacing: -0.035em; }
.stApp h1 { font-weight: 800; }
.stApp p, .stApp label, .stApp [data-testid="stMarkdownContainer"] { color: #33475b; }
.stApp [data-testid="stCaptionContainer"] p { color: #586d80; line-height: 1.7; }
.stApp [data-testid="stVerticalBlockBorderWrapper"] > div,
.stApp [data-testid="stExpander"] details {
    background: #ffffff;
    border: 1px solid #d7e3ea !important;
    border-radius: 18px !important;
    box-shadow: 0 12px 32px #26465b0d;
}
.stApp [data-testid="stExpander"] summary { color: #24364b; }
.stApp [data-baseweb="select"] > div {
    background: #ffffff;
    color: #183247;
    border-color: #c3d4df;
    border-radius: 10px;
}
.stApp [data-baseweb="select"] svg { fill: #526b7c; }
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"] { background: #ffffff; color: #183247; }
[data-baseweb="popover"] [role="option"]:hover { background: #e5f3f0; }
.stApp [role="radiogroup"] { gap: 0.6rem; }
.stApp [role="radiogroup"] label {
    padding: 0.6rem 0.75rem;
    border: 1px solid #d7e3ea;
    border-radius: 10px;
    background: #f8fafc;
}
.stApp [role="radiogroup"] label:has(input:checked) {
    background: #d9eee8;
    border-color: #0f766e;
}
.stApp [data-testid="stSlider"] [role="slider"] { background: #0f766e; }
.stApp [data-testid="stLinkButton"] a {
    background: #0f766e;
    color: #ffffff !important;
    border: 1px solid #0f766e;
    border-radius: 10px;
    font-weight: 700;
}
.stApp [data-testid="stLinkButton"] a p { color: #ffffff; }
.stApp [data-testid="stLinkButton"] a:hover { background: #115e59; border-color: #115e59; }
.stApp [data-testid="stCode"], .stApp [data-testid="stCode"] pre {
    background: #edf5f4;
    color: #115e59;
    border-radius: 10px;
}
.stApp [data-testid="stImage"] img { border-radius: 16px; }
.stApp [data-testid="stDeckGlJsonChart"] { border-radius: 16px; overflow: hidden; }
.stApp a:focus-visible, .stApp button:focus-visible {
    outline: 2px solid #115e59;
    outline-offset: 3px;
}
.stApp h1 { color: #214c43; font-size: clamp(2rem, 4vw, 3rem); }
.stApp h3 { font-size: 1.25rem; }
.stApp [data-testid="stTabs"] [role="tablist"] {
    background: #eaf1eb;
    border: 1px solid #dce7df;
    border-radius: 16px;
    padding: 6px;
    gap: 6px;
    margin: 1rem 0 1.5rem;
}
.stApp [data-testid="stTabs"] [role="tab"] {
    border-radius: 11px;
    padding: 0.7rem 1.2rem;
    height: auto;
    color: #52695f;
}
.stApp [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #ffffff;
    box-shadow: 0 3px 10px #34544612;
}
.stApp [data-testid="stTabs"] [role="tab"][aria-selected="true"] p {
    color: #096b58;
    font-weight: 700;
}
.stApp [data-baseweb="tab-highlight"], .stApp [data-baseweb="tab-border"] { display: none; }
.stApp [data-testid="stForm"] {
    background: linear-gradient(115deg, #ffffff, #f0f8f3);
    border: 1px solid #d6e6db;
    border-radius: 18px;
    padding: 1.3rem;
    box-shadow: 0 8px 24px #33554108;
}
.stApp .st-key-travel_search_card {
    background: linear-gradient(115deg, #ffffff, #f0f8f3);
    border: 1px solid #d6e6db;
    border-radius: 18px;
    padding: 1.3rem;
    box-shadow: 0 8px 24px #33554108;
}
.stApp .st-key-travel_search_card [data-testid="stForm"] {
    background: transparent;
    border: none;
    padding: 0;
    box-shadow: none;
}
.stApp [data-baseweb="input"], .stApp [data-baseweb="base-input"] {
    background: #ffffff;
    color: #243d35;
    border-radius: 10px;
    border-color: #cbded1;
}
.stApp input { color: #243d35; caret-color: #0f766e; }
.stApp input::placeholder { color: #6c8076; opacity: 1; }
.stApp [data-baseweb="input"]:focus-within,
.stApp [data-baseweb="select"]:focus-within > div {
    border-color: #0f766e;
    box-shadow: 0 0 0 3px #0f766e15;
}
.stApp [data-testid="stFormSubmitButton"] button {
    background: #0f766e;
    border: 1px solid #0f766e;
    border-radius: 10px;
    min-height: 2.7rem;
    padding-inline: 1.5rem;
}
.stApp [data-testid="stFormSubmitButton"] button p { color: #ffffff; font-weight: 700; }
.stApp [data-testid="stFormSubmitButton"] button:hover { background: #115e59; }
.stApp [data-testid="stMetric"] {
    background: #f0f7f2;
    border: 1px solid #dfebe2;
    border-radius: 14px;
    padding: 1rem;
}
.stApp [data-testid="stMetricValue"] { color: #1d6553; font-size: clamp(1.4rem, 2.3vw, 2rem); }
.stApp [data-testid="stMetricLabel"] p { color: #526b5f; }
.stApp [data-testid="stAlert"] {
    background: #fff5e8;
    color: #72502e;
    border: 1px solid #efdfc7;
    border-radius: 12px;
}
.stApp [data-testid="stAlert"] p { color: #72502e; }
.stApp hr { border-color: #dfe8e1; }
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] { padding-top: 1.5rem; }
    .stApp [data-testid="stTabs"] [role="tab"] { padding: 0.65rem 0.7rem; }
    .stApp [data-testid="stMetric"] { padding: 0.7rem; }
}
</style>
""")
st.title("✈️ 여행 준비 도우미")
st.caption("도쿄 명소를 둘러보거나, 해외 여행지를 검색하며 여행을 준비하세요.")

# day06/.env 우선, 없으면 프로젝트 루트의 .env 사용
app_dir = Path(__file__).resolve().parent
env_path = app_dir / ".env"
if not env_path.exists():
    env_path = app_dir.parent / ".env"
settings = dotenv_values(env_path, encoding="utf-8-sig")
token = (os.getenv("MAPBOX_ACCESS_TOKEN") or settings.get("MAPBOX_ACCESS_TOKEN") or "").strip()
if not token:
    st.info("프로젝트 폴더 또는 day06의 .env에 Mapbox 공개 토큰을 입력한 뒤 페이지를 새로고침하세요.")
    st.code("MAPBOX_ACCESS_TOKEN=pk.여기에_공개_토큰_입력", language="bash")
    st.stop()
if not token.startswith("pk."):
    st.error("pk.로 시작하는 Mapbox 공개 토큰을 사용하세요.")
    st.stop()

styles = {
    "일반 지도": "mapbox://styles/mapbox/streets-v12",
    "밝은 지도": "mapbox://styles/mapbox/light-v11",
    "위성 지도": "mapbox://styles/mapbox/satellite-streets-v12",
}
st.sidebar.subheader("🗺️ 지도 옵션")
st.sidebar.caption("두 탭의 지도에 공통으로 적용됩니다.")
map_mode = st.sidebar.radio("🖼️ 지도 보기 방식", ["🖱️ 인터랙티브 지도", "📷 정적 지도"])
style = st.sidebar.selectbox("🗺️ 지도 배경", list(styles), index=list(styles).index("위성 지도"))
static_zoom = 7
if map_mode == "📷 정적 지도":
    static_zoom = st.sidebar.slider(
        "🔍 정적 지도 확대 레벨", min_value=1, max_value=10,
        value=7, step=1, key="static_zoom",
        help="1은 넓은 지역, 10은 건물 주변까지 확대합니다. 원하는 장소를 먼저 선택하세요.",
    )

tokyo_tab, travel_tab = st.tabs(["🗼 도쿄 명소 지도", "✈️ 해외여행 도우미"])
with tokyo_tab:
    places = [
        {"name": "시부야스카이", "latitude": 35.6584, "longitude": 139.7022},
        {"name": "도쿄타워", "latitude": 35.6586, "longitude": 139.7454},
        {"name": "JR신주쿠역", "latitude": 35.6909, "longitude": 139.7003},
        {"name": "아사쿠사 센소지", "latitude": 35.7148, "longitude": 139.7967},
    ]
    # 공식 장소 안내를 참고한 정보. 좌표는 지도 표시용 대표 위치이다.
    details = [
        {"emoji": "🌇", "category": "전망대", "address": "도쿄도 시부야구 시부야 2-24-12",
         "description": "시부야 스크램블 스퀘어에 있는 전망대로, 도쿄 도심을 내려다볼 수 있습니다.",
         "website": "https://www.shibuya-scramble-square.com/kr/index.html"},
        {"emoji": "🗼", "category": "전망대 · 랜드마크", "address": "도쿄도 미나토구 시바코엔 4-2-8",
         "description": "시바코엔에 위치한 도쿄의 대표적인 타워입니다.",
         "website": "https://en.tokyotower.co.jp/company/"},
        {"emoji": "🚉", "category": "교통 · 철도역", "address": "도쿄도 신주쿠구 신주쿠 3초메",
         "description": "JR 야마노테선과 주오선 등을 이용할 수 있는 철도역입니다. 출구별 위치는 공식 역 안내도를 확인하세요.",
         "website": "https://www.jreast.co.jp/estation/station/info.aspx?StationCd=866"},
        {"emoji": "🏯", "category": "사찰 · 역사 명소", "address": "도쿄도 다이토구 아사쿠사 2-3-1",
         "description": "아사쿠사에 위치한 불교 사찰로, 경내에서 전통 건축을 둘러볼 수 있습니다.",
         "website": "https://www.senso-ji.jp/korean/"},
    ]
    for place, detail in zip(places, details):
        place.update(detail)
    focus = st.selectbox("📍 도쿄 명소 선택", ["도쿄 전체"] + [p["name"] for p in places], key="tokyo_place")
    center = {"latitude": 35.6866, "longitude": 139.7485}
    selected_place = None
    if focus != "도쿄 전체":
        selected_place = next(p for p in places if p["name"] == focus)
        center = selected_place

    for place in places:
        place["color"] = [255, 160, 30, 255] if place["name"] == focus else [235, 65, 65, 220]

    layer = pdk.Layer(
        "ScatterplotLayer", id="tokyo-places", data=places,
        get_position="[longitude, latitude]",  # 경도, 위도 순서
        get_fill_color="color",
        # 화면 픽셀 기준으로 고정하여 확대해도 마커가 커지지 않게 한다.
        get_radius=7, radius_units=pdk.types.String("pixels"), billboard=True, pickable=True,
    )
    deck = pdk.Deck(
        api_keys={"mapbox": token},
        map_provider="mapbox",
        map_style=styles[style],
        initial_view_state=pdk.ViewState(
            latitude=center["latitude"], longitude=center["longitude"],
            zoom=11 if focus == "도쿄 전체" else 15,
        ),
        layers=[layer], tooltip={"text": "{emoji} {name}\n🏷️ {category}\n📍 {address}\n🧭 위도 {latitude}, 경도 {longitude}"},
    )
    map_column, info_column = st.columns([2, 1])
    with map_column:
        if map_mode == "🖱️ 인터랙티브 지도":
            st.pydeck_chart(deck, height=600)
            st.caption("🖱️ 드래그로 이동하고 스크롤로 확대하세요. 마커에 마우스를 올리면 장소 정보가 나타납니다.")
        else:
            # Mapbox Static Images API: 좌표 순서는 경도, 위도이다.
            static_places = [selected_place] if selected_place else places
            markers = []
            for place in static_places:
                color = "ffa01e" if selected_place else "eb4141"
                number = places.index(place) + 1
                markers.append(f"pin-s-{number}+{color}({place['longitude']},{place['latitude']})")
            # 사용자 레벨 1~10을 실제 지도 줌 1~18에 대응시킨다.
            mapbox_zoom = 1 + (static_zoom - 1) * 17 / 9
            position = f"{center['longitude']},{center['latitude']},{mapbox_zoom:.2f}"
            style_id = styles[style].removeprefix("mapbox://styles/")
            query = urlencode({"access_token": token})
            static_url = (
                f"https://api.mapbox.com/styles/v1/{style_id}/static/"
                f"{','.join(markers)}/{position}/900x600@2x?{query}"
            )
            st.image(static_url, caption=f"📷 {focus} · {style} · 확대 레벨 {static_zoom}", width="stretch")
            st.caption("정적 지도는 이미지입니다. 장소와 배경은 왼쪽 메뉴에서 변경할 수 있습니다.")
            st.caption(" · ".join(f"{places.index(p) + 1}. {p['name']}" for p in static_places))
    with info_column:
        with st.container(border=True):
            if selected_place:
                st.subheader(f"{selected_place['emoji']} {selected_place['name']}")
                st.markdown(f"**🏷️ 카테고리**  \n{selected_place['category']}")
                st.markdown(f"**📍 주소**  \n{selected_place['address']}")
                st.markdown("**🧭 좌표 (위도, 경도)**")
                st.code(f"{selected_place['latitude']:.4f}, {selected_place['longitude']:.4f}", language=None)
                st.caption("좌표는 장소의 대표 위치이며, 입구 위치와 다를 수 있습니다.")
                st.markdown(f"**📝 장소 소개**  \n{selected_place['description']}")
                st.link_button("🔗 공식 안내 보기", selected_place["website"])
            else:
                st.subheader("🗺️ 도쿄 명소 둘러보기")
                st.write("위의 ‘📍 도쿄 명소 선택’에서 명소를 골라보세요. 지도 확대와 함께 주소·좌표·카테고리가 표시됩니다.")
                for place in places:
                    st.write(f"{place['emoji']} **{place['name']}** · {place['category']}")

    with st.expander("📋 전체 장소 정보"):
        st.dataframe(
            [{key: p[key] for key in ("name", "category", "address", "latitude", "longitude")} for p in places],
            hide_index=True,
            column_config={"name": "장소", "category": "카테고리", "address": "주소", "latitude": "위도", "longitude": "경도"},
        )

with travel_tab:
    weather_key = (os.getenv("OPENWEATHER_API_KEY") or settings.get("OPENWEATHER_API_KEY") or "").strip()
    exchange_key = (os.getenv("EXCHANGE_RATE_API_KEY") or settings.get("EXCHANGE_RATE_API_KEY") or "").strip()
    travel_search.render_travel_search(
        token, weather_key, exchange_key,
        map_mode=map_mode, map_style=styles[style], static_zoom=static_zoom,
    )
