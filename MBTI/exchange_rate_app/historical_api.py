"""최신 계산과 독립적으로 Frankfurter v2의 실제 과거 데이터를 조회한다."""
import requests
import pandas as pd
import streamlit as st


@st.cache_data(ttl=3600, show_spinner=False)
def get_historical_rates(base_currency, target_currency, start_date, end_date,
                         group: str | None = None) -> pd.DataFrame:
    params = {'base': base_currency, 'quotes': target_currency,
              'from': str(start_date), 'to': str(end_date)}
    if group:
        params['group'] = group
    try:
        response = requests.get('https://api.frankfurter.dev/v2/rates',
                                params=params, timeout=10)
        if response.status_code in (400, 404, 422):
            raise ValueError('해당 통화쌍 또는 기간의 과거 데이터를 지원하지 않습니다.')
        response.raise_for_status()
        rows = response.json()
    except requests.exceptions.Timeout:
        raise ValueError('과거 환율 서버 응답 시간이 초과되었습니다.') from None
    except requests.exceptions.ConnectionError:
        raise ValueError('과거 환율 서버에 연결할 수 없습니다.') from None
    except requests.exceptions.RequestException:
        raise ValueError('과거 환율을 불러오지 못했습니다.') from None
    if not isinstance(rows, list):
        raise ValueError('과거 환율 응답 형식이 올바르지 않습니다.')
    if not rows:
        return pd.DataFrame(columns=['date', 'rate'])
    if any(not isinstance(row, dict) or row.get('base') != base_currency
           or row.get('quote') != target_currency for row in rows):
        raise ValueError('과거 환율 응답의 통화 방향이 올바르지 않습니다.')
    frame = pd.DataFrame(rows)
    if not {'date', 'rate'}.issubset(frame.columns):
        raise ValueError('과거 환율 응답에 필요한 필드가 없습니다.')
    frame['date'] = pd.to_datetime(frame['date'], errors='coerce')
    frame['rate'] = pd.to_numeric(frame['rate'], errors='coerce')
    frame = frame.dropna(subset=['date', 'rate'])
    frame = frame[(frame['rate'] > 0) & (frame['rate'] < float('inf'))]
    return frame[['date', 'rate']].drop_duplicates('date').sort_values('date').reset_index(drop=True)
