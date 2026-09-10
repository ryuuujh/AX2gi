"""화면에서 사용하는 숫자 및 날짜 포맷."""
from datetime import date, datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta

KST = timezone(timedelta(hours=9))
CURRENCIES = {
    'KRW': '대한민국 원', 'USD': '미국 달러', 'JPY': '일본 엔',
    'EUR': '유로', 'CNY': '중국 위안', 'GBP': '영국 파운드',
    'AUD': '호주 달러', 'CAD': '캐나다 달러', 'CHF': '스위스 프랑',
    'HKD': '홍콩 달러', 'SGD': '싱가포르 달러', 'THB': '태국 바트',
    'VND': '베트남 동',
}
PERIODS = {'1일': '1D', '5일': '5D', '1개월': '1M', '1년': '1Y', '5년': '5Y', '최대': 'MAX'}


def format_number(value):
    if value == 0:
        return '0'
    if abs(value) >= 1:
        return f'{value:,.2f}'.rstrip('0').rstrip('.')
    return f'{value:.8g}'


def format_update(timestamp):
    try:
        moment = datetime.fromtimestamp(float(timestamp), KST)
        return moment.strftime('%Y년 %m월 %d일 %H:%M (한국 시간)')
    except (ValueError, TypeError, OSError, OverflowError):
        return '업데이트 시간 정보 없음'


def period_range(period):
    end = datetime.now(KST).date()
    starts = {
        '1일': end - timedelta(days=14), '5일': end - timedelta(days=5),
        '1개월': end - relativedelta(months=1), '1년': end - relativedelta(years=1),
        '5년': end - relativedelta(years=5), '최대': date(1948, 1, 1),
    }
    return starts[period], end, 'month' if period in ('5년', '최대') else None
