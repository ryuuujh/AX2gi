"""해외 도시·주소 검색 화면. 검색 결과는 현재 세션에서만 사용한다."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import pydeck as pdk
import streamlit as st
from travel_conditions import render_conditions


def search_locations(query, token):
    params = urlencode({"q": query, "access_token": token, "language": "ko", "limit": 5})
    url = f"https://api.mapbox.com/search/geocode/v6/forward?{params}"
    with urlopen(url, timeout=15) as response:
        payload = json.load(response)
    results = []
    for feature in payload.get("features", []):
        props = feature.get("properties", {})
        coordinates = feature.get("geometry", {}).get("coordinates", [])
        if len(coordinates) < 2:
            continue
        results.append({
            "name": props.get("name", "이름 없는 장소"),
            "address": props.get("full_address") or props.get("place_formatted") or props.get("name", ""),
            "category": props.get("feature_type", "place"),
            "longitude": coordinates[0], "latitude": coordinates[1],
            "country": props.get("context", {}).get("country", {}).get("name", "정보 없음"),
            "country_code": props.get("context", {}).get("country", {}).get("country_code", ""),
        })
    return results


def render_travel_search(token, weather_key="", exchange_key="", *,
                         map_mode="🖱️ 인터랙티브 지도",
                         map_style="mapbox://styles/mapbox/streets-v12", static_zoom=7):
    st.subheader("✈️ 해외여행 도우미")
    st.caption("여행할 도시·지역·주소를 검색해 위치를 확인하세요. 예: Paris, London, 타이베이")
    st.caption("도시와 주소 검색을 지원합니다. 상호명이나 관광시설 이름은 주소로 검색해주세요.")
    with st.container(border=True, key="travel_search_card"):
        with st.form("travel_search_form", border=False):
            query = st.text_input("🔎 여행지 검색", placeholder="도시 또는 주소 입력", max_chars=200)
            submitted = st.form_submit_button("검색", type="primary")
        if submitted:
            st.session_state.pop("travel_result", None)
            st.session_state["travel_results"] = []
            st.session_state["travel_message"] = ""
            if not query.strip():
                st.session_state["travel_message"] = "검색할 도시나 주소를 입력해주세요."
            else:
                try:
                    with st.spinner("🌍 여행지를 찾고 있어요…"):
                        st.session_state["travel_results"] = search_locations(query.strip(), token)
                    if not st.session_state["travel_results"]:
                        st.session_state["travel_message"] = "검색 결과가 없습니다. 영문 도시명이나 더 자세한 주소로 검색해주세요."
                except HTTPError as error:
                    messages = {
                        401: "Mapbox 토큰이 유효한지 확인해주세요.",
                        403: "검색 접근이 거부되었습니다. Mapbox 토큰 권한과 URL 제한을 확인해주세요.",
                        429: "검색 요청이 많습니다. 잠시 후 다시 시도해주세요.",
                    }
                    st.session_state["travel_message"] = messages.get(error.code, "검색 서버에 문제가 있습니다. 잠시 후 다시 시도해주세요.")
                except (URLError, TimeoutError, ValueError, OSError):
                    # 예외에는 토큰이 포함된 URL이 있을 수 있으므로 그대로 출력하지 않는다.
                    st.session_state["travel_message"] = "검색 정보를 불러오지 못했습니다. 네트워크 연결을 확인하고 다시 시도해주세요."

        message = st.session_state.get("travel_message")
        if message:
            st.info(message)
        results = st.session_state.get("travel_results", [])
        if not results:
            return
        index = st.selectbox("📍 검색 결과 선택", range(len(results)),
                             format_func=lambda i: f"{results[i]['name']} · {results[i]['address']}",
                             key="travel_result")
    place = results[index]
    map_col, detail_col = st.columns([2, 1])
    with map_col:
        deck = pdk.Deck(
            api_keys={"mapbox": token}, map_provider="mapbox",
            map_style=map_style,
            initial_view_state=pdk.ViewState(
                longitude=place["longitude"], latitude=place["latitude"],
                zoom=14 if place["category"] in ("address", "street") else 10,
            ),
            layers=[pdk.Layer("ScatterplotLayer", id="travel-result", data=[place],
                              get_position="[longitude, latitude]", get_radius=7,
                              radius_units=pdk.types.String("pixels"), billboard=True,
                              get_fill_color=[15, 118, 110, 230], pickable=True)],
            tooltip={"text": "{name}\n{address}"},
        )
        if map_mode == "🖱️ 인터랙티브 지도":
            st.pydeck_chart(deck, height=550, key="travel_map")
        else:
            mapbox_zoom = 1 + (static_zoom - 1) * 17 / 9
            position = f"{place['longitude']},{place['latitude']},{mapbox_zoom:.2f}"
            marker = f"pin-s+0f766e({place['longitude']},{place['latitude']})"
            style_id = map_style.removeprefix("mapbox://styles/")
            query_string = urlencode({"access_token": token})
            image_url = (
                f"https://api.mapbox.com/styles/v1/{style_id}/static/"
                f"{marker}/{position}/900x600@2x?{query_string}"
            )
            st.image(image_url, caption=f"📷 {place['name']} · 확대 레벨 {static_zoom}", width="stretch")
            st.caption("왼쪽 지도 옵션에서 배경과 확대 레벨을 변경할 수 있습니다.")
    with detail_col:
        categories = {"country": "국가", "region": "지역", "place": "도시", "district": "행정구역",
                      "locality": "지역", "neighborhood": "동네", "address": "주소", "street": "도로", "postcode": "우편번호"}
        with st.container(border=True):
            st.subheader("📍 여행지 정보")
            st.text(place["name"])
            st.markdown("**🌏 국가**")
            st.text(place["country"])
            st.markdown("**🏷️ 카테고리**")
            st.text(categories.get(place["category"], place["category"]))
            st.markdown("**📮 주소 / 지역**")
            st.text(place["address"])
            st.markdown("**🧭 좌표 (위도, 경도)**")
            st.code(f"{place['latitude']:.5f}, {place['longitude']:.5f}", language=None)
            st.caption("도시·지역 검색 결과는 대표 위치를 표시합니다.")
    render_conditions(place, weather_key, exchange_key)
