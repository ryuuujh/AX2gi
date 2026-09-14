"""app_basic.py와 같은 OpenWeatherMap 및 ExchangeRate-API 연동."""
import math
from datetime import datetime, timedelta, timezone

import requests
import streamlit as st


@st.cache_data(ttl=600, show_spinner=False)
def fetch_weather(latitude, longitude, api_key):
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"lat": latitude, "lon": longitude, "appid": api_key, "units": "metric", "lang": "kr"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_rates(api_key):
    response = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/latest/KRW", timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("result") != "success" or data.get("base_code") != "KRW":
        raise ValueError("Invalid exchange response")
    return data


def render_weather(place, api_key):
    st.subheader("🌤️ 현재 날씨")
    if not api_key:
        st.info(".env에 OPENWEATHER_API_KEY를 추가하면 선택한 여행지의 날씨가 표시됩니다.")
        return
    try:
        with st.spinner("날씨를 불러오는 중…"):
            data = fetch_weather(place["latitude"], place["longitude"], api_key)
        condition = data["weather"][0]
        code = int(condition["id"])
        temperature = float(data["main"]["temp"])
        feels_like = float(data["main"]["feels_like"])
        humidity = float(data["main"]["humidity"])
        wind = float(data["wind"]["speed"])
        if not all(math.isfinite(v) for v in (temperature, feels_like, humidity, wind)):
            raise ValueError("Invalid weather values")
        local_time = datetime.fromtimestamp(data["dt"], timezone(timedelta(seconds=data["timezone"])))
        description = condition["description"]
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else None
        st.error({401: "날씨 API 키가 유효하지 않거나 아직 활성화되지 않았습니다.",
                  429: "날씨 조회 한도를 초과했습니다. 잠시 후 다시 시도해주세요."}.get(status, "날씨 서버가 요청을 처리하지 못했습니다."))
        return
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, OverflowError, OSError):
        st.error("날씨를 불러오지 못했습니다. 네트워크와 API 설정을 확인해주세요.")
        return
    icon = "☀️" if code == 800 else {2: "⛈️", 3: "🌦️", 5: "🌧️", 6: "❄️", 7: "🌫️", 8: "☁️"}.get(code // 100, "🌤️")
    st.text(f"{icon} {place['name']} · {description}")
    st.metric("현재 기온", f"{temperature:.1f} °C")
    cols = st.columns(3)
    cols[0].metric("체감 온도", f"{feels_like:.1f} °C")
    cols[1].metric("습도", f"{humidity:.0f}%")
    cols[2].metric("풍속", f"{wind:.1f} m/s")
    st.caption(f"관측 시각: {local_time:%Y-%m-%d %H:%M} (여행지 현지 시간)")
    st.caption("OpenWeatherMap · 선택 좌표 주변의 현재 날씨 · 조회 결과 10분 캐시")


# 주요 여행 국가의 기본 통화. 나머지 국가는 사용자가 통화를 선택한다.
COUNTRY_CURRENCIES = {
    "KR": "KRW", "JP": "JPY", "US": "USD", "GB": "GBP", "FR": "EUR", "DE": "EUR",
    "IT": "EUR", "ES": "EUR", "PT": "EUR", "NL": "EUR", "AT": "EUR", "GR": "EUR",
    "IE": "EUR", "BE": "EUR", "FI": "EUR", "AU": "AUD", "NZ": "NZD", "CA": "CAD",
    "VN": "VND", "TH": "THB", "CN": "CNY", "TW": "TWD", "HK": "HKD", "SG": "SGD",
    "CH": "CHF", "MY": "MYR", "ID": "IDR", "PH": "PHP", "IN": "INR", "AE": "AED",
}


def render_exchange(place, api_key):
    st.subheader("💱 여행지 환율")
    if not api_key:
        st.info(".env에 EXCHANGE_RATE_API_KEY를 추가하면 환율과 환전 계산기를 사용할 수 있습니다.")
        return
    try:
        with st.spinner("환율을 불러오는 중…"):
            data = fetch_rates(api_key)
        rates = {code: float(value) for code, value in data["conversion_rates"].items()}
        rates = {code: value for code, value in rates.items() if math.isfinite(value) and value > 0}
        if not rates:
            raise ValueError("Empty rates")
        updated = datetime.fromtimestamp(data["time_last_update_unix"], timezone(timedelta(hours=9)))
    except (requests.RequestException, ValueError, KeyError, TypeError, OverflowError, OSError):
        st.error("환율을 불러오지 못했습니다. API 키·요청 한도와 네트워크를 확인해주세요.")
        return
    country_code = place.get("country_code", "").upper()
    default = COUNTRY_CURRENCIES.get(country_code)
    currencies = sorted(rates)
    if default not in rates:
        default = None
    currency = st.selectbox("환산할 통화", currencies, index=currencies.index(default) if default else None,
                            placeholder="여행지에서 사용하는 통화를 선택하세요", key=f"travel_currency_{country_code}")
    if not default:
        st.caption("이 국가의 통화는 직접 선택해주세요.")
    if currency is None:
        return
    amount = st.number_input("환산할 원화 금액 (KRW)", min_value=0.0, max_value=1e12,
                             value=10000.0, step=1000.0, key="travel_krw_amount")
    rate = rates[currency]
    st.metric(f"1 {currency}", f"{1 / rate:,.2f} 원")
    st.metric(f"{amount:,.0f} 원 환산", f"{amount * rate:,.2f} {currency}")
    st.caption(f"환율 기준: {updated:%Y-%m-%d %H:%M} (한국 시간)")
    st.caption("ExchangeRate-API · 조회 결과 1시간 캐시 · 실제 환전 금액은 수수료 등에 따라 다릅니다.")


def render_conditions(place, weather_key, exchange_key):
    st.divider()
    weather_col, exchange_col = st.columns(2)
    with weather_col, st.container(border=True):
        render_weather(place, weather_key)
    with exchange_col, st.container(border=True):
        render_exchange(place, exchange_key)
