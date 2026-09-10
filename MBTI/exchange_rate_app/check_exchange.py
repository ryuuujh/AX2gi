"""이 폴더에서 실행 점검: python check_exchange.py [--live]. 테스트 응답은 화면용 데이터가 아니다."""
import sys
from unittest.mock import patch
import requests
from streamlit.testing.v1 import AppTest
import exchange_api
import historical_api
from utils import period_range


def live_check():
    try:
        data = exchange_api.get_latest_rates('KRW')
        print('Live KRW -> USD:', data['conversion_rates']['USD'])
    except ValueError as error:
        print('Latest API:', str(error))
    start, end, group = period_range('1개월')
    try:
        frame = historical_api.get_historical_rates('KRW', 'USD', start, end, group)
        print('Live historical rows:', len(frame))
    except ValueError as error:
        print('Historical API:', str(error))


def app_check():
    exchange_api._fetch_latest.clear()
    historical_api.get_historical_rates.clear()
    calls = []

    def response(url, **kwargs):
        calls.append(url)
        result = requests.Response()
        result.status_code = 200
        if '/latest/' in url:
            base = url.rsplit('/', 1)[-1]
            rates = {'KRW': 1, 'USD': 0.00072, 'JPY': 0.108}
            divisor = rates[base]
            payload = {'result': 'success', 'base_code': base,
                       'conversion_rates': {key: value / divisor for key, value in rates.items()},
                       'time_last_update_unix': 1788998400}
        else:
            params = kwargs['params']
            payload = [{'date': '2026-09-08', 'base': params['base'],
                        'quote': params['quotes'], 'rate': 0.00070},
                       {'date': '2026-09-09', 'base': params['base'],
                        'quote': params['quotes'], 'rate': 0.00072}]
        import json
        result._content = json.dumps(payload).encode()
        return result

    with patch.object(exchange_api, 'get_setting', side_effect=lambda name: 'test-key' if name == 'EXCHANGE_API_KEY' else ''), patch('requests.get', side_effect=response):
        app = AppTest.from_file('exchangerate.py', default_timeout=20).run()
        assert not app.exception
        assert app.session_state['amount'] == 1.0
        assert app.session_state['base_currency'] == 'USD'
        assert app.session_state['target_currency'] == 'KRW'
        assert app.metric[0].value == '1,388.89 KRW'
        count = len(calls)
        app.number_input[0].set_value(1000).run()
        assert not app.exception and len(calls) == count
        assert app.metric[0].value == '1,388,888.89 KRW'
        app.selectbox[1].select('JPY').run()
        assert sum('/latest/' in url for url in calls) == 1
        app.button[0].click().run()
        assert app.session_state['base_currency'] == 'JPY'
        assert app.session_state['target_currency'] == 'USD'
        for period in ('1일', '5일', '1년', '5년', '최대'):
            app.radio[0].set_value(period).run()
            assert not app.exception
        app.selectbox[1].select('JPY').run()
        assert not app.exception
    with patch.object(exchange_api, 'get_setting', return_value=''), patch('requests.get', side_effect=response):
        app = AppTest.from_file('exchangerate.py').run()
        assert not app.exception and app.warning
    for code in exchange_api.ERRORS:
        exchange_api._fetch_latest.clear()
        result = requests.Response()
        result.status_code = 403
        import json
        result._content = json.dumps({'result': 'error', 'error-type': code}).encode()
        with patch('requests.get', return_value=result):
            try:
                exchange_api._fetch_latest('KRW', 'test-key', 'https://example.invalid')
                raise AssertionError('Error response was accepted')
            except ValueError as error:
                assert str(error) == exchange_api.ERRORS[code]
    print('PASS: rendering, conversion, caching, swap, periods, same currency, missing key, API errors')


if __name__ == '__main__':
    live_check() if '--live' in sys.argv else app_check()
