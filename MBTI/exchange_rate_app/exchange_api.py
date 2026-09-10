"""ExchangeRate-API 최신 환율. 요청 URL에는 비밀 키가 있으므로 출력하지 않는다."""
import math
import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


def get_setting(name: str) -> str:
    # 로컬 설정을 우선 탐색하되, 이미 등록된 환경변수는 보존한다.
    folder = Path(__file__).resolve().parent
    load_dotenv(folder / '.env')
    load_dotenv(folder.parent / '.env')
    load_dotenv(folder.parent.parent / '.env')
    try:
        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        pass
    return os.getenv(name, '').strip()


ERRORS = {
    'unsupported-code': '현재 지원하지 않는 통화입니다.',
    'unknown-code': '현재 지원하지 않는 통화입니다.',
    'malformed-request': '환율 요청 형식이 올바르지 않습니다.',
    'invalid-key': 'API Key가 올바르지 않습니다.',
    'inactive-account': '계정 이메일 인증을 완료해 주세요.',
    'quota-reached': '이번 API 사용량을 모두 사용했습니다.',
    'plan-upgrade-required': '현재 요금제에서 지원하지 않는 요청입니다.',
}


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_latest(base_currency: str, api_key: str, base_url: str) -> dict:
    try:
        response = requests.get(
            f'{base_url}/{api_key}/latest/{base_currency}', timeout=10
        )
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError('환율 응답 형식이 올바르지 않습니다.')
        if data.get('result') != 'success':
            raise ValueError(ERRORS.get(data.get('error-type'), '환율 제공 서비스 오류입니다.'))
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ValueError('환율 서버 응답 시간이 초과되었습니다.') from None
    except requests.exceptions.ConnectionError:
        raise ValueError('환율 서버에 연결할 수 없습니다.') from None
    except requests.exceptions.JSONDecodeError:
        raise ValueError('환율 서버가 올바른 JSON을 반환하지 않았습니다.') from None
    except requests.exceptions.RequestException:
        raise ValueError('환율 요청에 실패했습니다. 잠시 후 다시 시도해 주세요.') from None
    rates = data.get('conversion_rates')
    if data.get('base_code') != base_currency or not isinstance(rates, dict):
        raise ValueError('환율 응답에 필요한 필드가 없습니다.')
    if not rates or any(
        isinstance(value, bool) or not isinstance(value, (int, float))
        or not math.isfinite(value) or value <= 0 for value in rates.values()
    ):
        raise ValueError('환율 응답에 유효하지 않은 값이 있습니다.')
    return data


def get_latest_rates(base_currency: str) -> dict:
    """전체 환율과 업데이트 메타데이터를 반환한다. 금액은 캐시 키에 포함하지 않는다."""
    api_key = get_setting('EXCHANGE_API_KEY') or get_setting('EXCHANGE_RATE_API_KEY')
    if not api_key or api_key.startswith('your_'):
        raise ValueError('MBTI/.env 또는 Streamlit Secrets에 EXCHANGE_API_KEY를 설정해 주세요.')
    base_url = get_setting('EXCHANGE_API_BASE_URL') or 'https://v6.exchangerate-api.com/v6'
    if base_url.rstrip('/') != 'https://v6.exchangerate-api.com/v6':
        raise ValueError('EXCHANGE_API_BASE_URL을 https://v6.exchangerate-api.com/v6 로 설정해 주세요.')
    return _fetch_latest(base_currency, api_key, base_url.rstrip('/'))


def get_latest_rate(base_currency: str, target_currency: str) -> float:
    rates = get_latest_rates(base_currency)['conversion_rates']
    if target_currency not in rates:
        raise ValueError('현재 지원하지 않는 대상 통화입니다.')
    return float(rates[target_currency])


def convert_currency(amount: float, base_currency: str, target_currency: str) -> float:
    if not math.isfinite(amount) or amount < 0:
        raise ValueError('금액은 0 이상의 유한한 숫자여야 합니다.')
    return amount * get_latest_rate(base_currency, target_currency)
