# 날씨 API 실습
# OpenWeatherMap 현재 날씨 API로 특정 도시의 날씨를 가져와 출력한다.
# 사전준비 OpenWeatherMap 회원 가입 후 API 발급
# pip install streamlit requests python-dotenv
# .env 파일을 생성하고 이곳에 OPENWEATHER_API_KEY = 발급받은 API 키
# .env.example OPENWEATHER_API_KEY = your_key
# .env.example 받아서 .env로 이름 바꾸고 자기 API를 채운다

import base64
import math
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


# 실제 키는 .env에서 읽는다. .env.example은 공유용 설정 예시이다.
app_directory = Path(__file__).resolve().parent
load_dotenv(app_directory / ".env")
load_dotenv(app_directory.parent / ".env")

# 도시 중심 좌표: 지도와 날씨 조회에 동일한 위치를 사용한다.
CITIES = {
    "대한민국": {"서울": (37.5665, 126.9780), "부산": (35.1796, 129.0756), "인천": (37.4563, 126.7052), "대구": (35.8714, 128.6014), "대전": (36.3504, 127.3845), "광주": (35.1595, 126.8526), "제주": (33.4996, 126.5312)},
    "일본": {"도쿄": (35.6762, 139.6503), "오사카": (34.6937, 135.5023), "삿포로": (43.0618, 141.3545), "후쿠오카": (33.5904, 130.4017)},
    "미국": {"뉴욕": (40.7128, -74.0060), "로스앤젤레스": (34.0522, -118.2437), "시카고": (41.8781, -87.6298), "샌프란시스코": (37.7749, -122.4194)},
    "영국": {"런던": (51.5074, -0.1278), "맨체스터": (53.4808, -2.2426), "에든버러": (55.9533, -3.1883)},
    "프랑스": {"파리": (48.8566, 2.3522), "리옹": (45.7640, 4.8357), "마르세유": (43.2965, 5.3698)},
    "호주": {"시드니": (-33.8688, 151.2093), "멜버른": (-37.8136, 144.9631), "브리즈번": (-27.4698, 153.0251)},
    "베트남": {"하노이": (21.0278, 105.8342), "호찌민": (10.8231, 106.6297), "다낭": (16.0544, 108.2022)},
    "태국": {"방콕": (13.7563, 100.5018), "치앙마이": (18.7883, 98.9853), "푸껫": (7.8804, 98.3923)},
}

st.set_page_config(page_title="도시 날씨 조회", page_icon="🌤️", layout="wide")


@st.cache_data
def load_font_data(font_path, modified_time):
    """글꼴을 캐시하고 파일이 바뀌면 다시 읽는다."""
    return base64.b64encode(Path(font_path).read_bytes()).decode("ascii")


font_path = Path(__file__).resolve().parent / "NanumGothicEco.otf"
if font_path.is_file():
    font_data = load_font_data(str(font_path), font_path.stat().st_mtime_ns)
    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'NanumGothicEco';
            src: url('data:font/otf;base64,{font_data}') format('opentype');
            font-weight: 400;
            font-style: normal;
            font-display: swap;
        }}
        html, body, [data-testid="stApp"],
        h1, h2, h3, h4, h5, h6, p, label, button, input, textarea,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
        [data-baseweb="select"] div,
        [role="listbox"], [role="option"] {{
            font-family: 'NanumGothicEco', sans-serif !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning("NanumGothicEco.otf 파일을 찾을 수 없어 기본 글꼴을 사용합니다.")

st.title("🌤️ 도시 날씨 조회")
st.write("국가와 도시를 선택하고 지도와 함께 현재 날씨를 확인하세요.")
st.caption("8개 국가의 주요 도시를 제공합니다.")

# 폼 밖에 두어 국가 변경 시 도시 목록도 즉시 바뀌게 한다.
country_column, city_column = st.columns(2)
selected_country = country_column.selectbox("국가 선택", list(CITIES))
city = city_column.selectbox("도시 선택", list(CITIES[selected_country]), key=f"city_{selected_country}")
latitude, longitude = CITIES[selected_country][city]
weather_column, map_column = st.columns([1, 1.2])
with map_column:
    st.subheader(f"📍 {selected_country} · {city}")
    st.map({"lat": [latitude], "lon": [longitude]}, zoom=10, height=420)
    st.caption("선택한 도시의 중심 위치 · 지도를 확대하거나 이동할 수 있습니다.")

with weather_column:
    st.subheader("현재 날씨")
    submitted = st.button("날씨 조회 / 새로고침", type="primary")
    if not submitted and f"weather_{latitude}_{longitude}" not in st.session_state:
        st.info("국가와 도시를 선택한 뒤 날씨 조회 버튼을 눌러 주세요.")

def render_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        st.warning(".env 파일에 OPENWEATHER_API_KEY를 설정한 뒤 앱을 다시 실행해 주세요.")
        st.code("OPENWEATHER_API_KEY=발급받은_API_키", language="bash")
        return

    weather_key = f"weather_{latitude}_{longitude}"
    if submitted or weather_key in st.session_state:
        try:
            if submitted:
                with st.spinner("날씨를 가져오는 중입니다..."):
                    response = requests.get(
                        "https://api.openweathermap.org/data/2.5/weather",
                        params={"lat": latitude, "lon": longitude, "appid": api_key, "units": "metric", "lang": "kr"},
                        timeout=10,
                    )
                if response.status_code == 401:
                    st.error("API 키가 유효하지 않거나 아직 활성화되지 않았습니다. 키를 확인해 주세요.")
                    return
                if response.status_code == 404:
                    st.error("선택한 위치의 날씨를 찾을 수 없습니다. 다른 도시를 선택해 주세요.")
                    return
                if response.status_code == 429:
                    st.error("API 요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.")
                    return
                response.raise_for_status()
                weather = response.json()
            else:
                weather = st.session_state[weather_key]
            # 필요한 데이터를 먼저 확인한 뒤 화면에 출력한다.
            description = weather["weather"][0]["description"]
            condition = int(weather["weather"][0]["id"])
            observed_at = datetime.fromtimestamp(weather["dt"], tz=timezone.utc)
            local_time = observed_at.astimezone(timezone(timedelta(seconds=weather["timezone"])))
            temperature = float(weather["main"]["temp"])
            feels_like = float(weather["main"]["feels_like"])
            humidity = weather["main"]["humidity"]
            wind_speed = float(weather["wind"]["speed"])
        except requests.exceptions.Timeout:
            st.error("날씨 서버의 응답이 늦어지고 있습니다. 잠시 후 다시 시도해 주세요.")
        except requests.exceptions.RequestException:
            # 예외 원문에는 API 키가 포함된 URL이 들어갈 수 있어 표시하지 않는다.
            st.error("날씨 정보를 가져오지 못했습니다. 인터넷 연결 및 API 서비스 상태를 확인해 주세요.")
        except (ValueError, KeyError, IndexError, TypeError):
            st.error("날씨 응답 형식이 올바르지 않습니다. 잠시 후 다시 시도해 주세요.")
        else:
            st.session_state[weather_key] = weather
            icon = "☀️" if condition == 800 else {2: "⛈️", 3: "🌦️", 5: "🌧️", 6: "❄️", 7: "🌫️", 8: "☁️"}.get(condition // 100, "🌤️")
            with weather_column:
                with st.container(border=True):
                    st.subheader(f"{icon} {city} · {description}")
                    st.metric("현재 기온", f"{temperature:.1f} °C")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("체감 온도", f"{feels_like:.1f} °C")
                    col2.metric("습도", f"{humidity}%")
                    col3.metric("풍속", f"{wind_speed:.1f} m/s")
                    st.caption(f"관측 시각: {local_time:%Y-%m-%d %H:%M} (도시 현지 시간)")
                st.caption("날씨 데이터: OpenWeatherMap · 현재 관측 날씨입니다.")


render_weather()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_exchange_rates(exchange_api_key):
    """KRW 기준 전체 환율을 1시간 캐시한다."""
    response = requests.get(
        f"https://v6.exchangerate-api.com/v6/{exchange_api_key}/latest/KRW",
        timeout=10,
    )
    data = response.json()
    if data.get("result") != "success":
        raise ValueError("환율 API 조회 실패")
    response.raise_for_status()
    if data.get("base_code") != "KRW":
        raise ValueError("KRW 기준 환율 응답이 아닙니다.")
    return data


def render_exchange_rates():
    st.divider()
    st.header("💱 KRW 기준 환율")
    currencies = {
        "미국": "USD", "일본": "JPY", "대한민국": "KRW",
        "영국": "GBP", "프랑스": "EUR", "호주": "AUD",
        "베트남": "VND", "태국": "THB", "중국": "CNY",
        "캐나다": "CAD", "스위스": "CHF", "싱가포르": "SGD",
    }
    country = st.selectbox("환율 국가 선택", list(currencies), key="exchange_country")
    currency = currencies[country]
    amount = st.number_input("환산할 원화 금액 (KRW)", min_value=0.0, value=10000.0, step=1000.0)
    exchange_api_key = os.getenv("EXCHANGE_RATE_API_KEY", "").strip()
    if not exchange_api_key:
        st.warning("프로젝트 루트 .env에 EXCHANGE_RATE_API_KEY를 설정해 주세요.")
        return
    try:
        with st.spinner("환율을 가져오는 중입니다..."):
            data = fetch_exchange_rates(exchange_api_key)
        rate = float(data["conversion_rates"][currency])
        if not math.isfinite(rate) or rate <= 0:
            raise ValueError("환율 응답 값이 올바르지 않습니다.")
        updated_at = datetime.fromtimestamp(data["time_last_update_unix"], timezone(timedelta(hours=9)))
        next_update = datetime.fromtimestamp(data["time_next_update_unix"], timezone(timedelta(hours=9)))
    except requests.exceptions.RequestException:
        st.error("환율 서버에 연결하지 못했습니다. 잠시 후 다시 시도해 주세요.")
        return
    except (ValueError, KeyError, TypeError, OverflowError, OSError):
        st.error("환율을 불러오지 못했습니다. API 키, 계정 인증, 요청 한도를 확인해 주세요.")
        return
    with st.container(border=True):
        st.subheader(f"{country} · {currency}")
        left, right = st.columns(2)
        left.metric(f"1,000 KRW → {currency}", f"{1000 * rate:,.2f} {currency}")
        right.metric(f"1 {currency} → KRW", f"{1 / rate:,.2f} 원")
        st.markdown(
            f"""
            <div style="margin: 1rem 0; padding: 1.5rem;
                        background: rgba(46, 160, 90, 0.12);
                        border: 1px solid rgba(46, 160, 90, 0.4);
                        border-radius: 12px;">
                <p style="margin: 0 0 0.5rem; font-size: 1.1rem;">
                    환전 결과 · {amount:,.2f} KRW
                </p>
                <p style="margin: 0; font-size: clamp(2rem, 5vw, 3.5rem);
                          font-weight: 700; line-height: 1.3; overflow-wrap: anywhere;">
                    {amount * rate:,.2f} {currency}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"환율 기준 시각: {updated_at:%Y-%m-%d %H:%M} (한국 시간)")
        st.caption(f"다음 갱신 예정: {next_update:%Y-%m-%d %H:%M} (한국 시간)")
    st.caption("제공: ExchangeRate-API · 제공처의 최신 기준 환율을 사용하며 조회 결과는 1시간 캐시합니다. 실제 환전 금액은 수수료 등에 따라 다를 수 있습니다.")


render_exchange_rates()
