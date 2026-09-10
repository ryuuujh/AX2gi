"""이 폴더에서 실행: python -m streamlit run exchangerate.py"""
import streamlit as st
import plotly.graph_objects as go

from exchange_api import get_latest_rates
from historical_api import get_historical_rates
from utils import CURRENCIES, PERIODS, format_number, format_update, period_range


def swap_currencies():
    # 콜백은 위젯을 다시 만들기 전에 실행되므로 key 충돌 없이 교환한다.
    state = st.session_state
    state.base_currency, state.target_currency = state.target_currency, state.base_currency


def render_history(base, target):
    st.caption(f'📈 환율 추이 · {base} → {target}')
    period = st.radio('조회 기간', list(PERIODS), horizontal=True,
                      key='selected_period', label_visibility='collapsed')
    if base == target:
        st.info('같은 통화의 환율은 항상 1입니다. 다른 통화를 선택하면 과거 그래프가 표시됩니다.')
        return
    start, end, group = period_range(period)
    if period == '1일':
        st.info('분/시간 단위 시계열은 제공되지 않습니다. 최근 가용 영업일 데이터 한 점을 표시합니다.')
    try:
        with st.spinner('환율 그래프를 불러오는 중입니다...'):
            frame = get_historical_rates(base, target, start, end, group)
    except ValueError as error:
        st.info(str(error))
        return
    if frame.empty:
        st.info('선택한 통화쌍과 기간에 가용한 과거 데이터가 없습니다.')
        return
    if period == '1일':
        frame = frame.tail(1)
    figure = go.Figure(go.Scatter(
        x=frame['date'], y=frame['rate'], mode='lines+markers' if len(frame) < 6 else 'lines',
        line={'color': '#1a73e8', 'width': 2}, marker={'size': 6},
        customdata=[str(value) for value in frame['rate']],
        hovertemplate='%{x|%Y-%m-%d}<br>%{customdata} ' + target + '<extra></extra>',
    ))
    figure.update_layout(height=350, margin=dict(l=10, r=10, t=15, b=15),
                         showlegend=False, paper_bgcolor='white', plot_bgcolor='white',
                         font=dict(color='#5f6368'), hovermode='x unified')
    figure.update_xaxes(showgrid=False, title=None)
    figure.update_yaxes(gridcolor='#eef0f2', zeroline=False, tickformat='.6g', title=None)
    st.plotly_chart(figure, width='stretch', config={'displayModeBar': False})
    st.caption(f"표시 범위: {frame['date'].iloc[0]:%Y-%m-%d} ~ {frame['date'].iloc[-1]:%Y-%m-%d}")
    if group:
        st.caption('월별 데이터 기준 요약입니다. 일별 최고·최저와 다를 수 있습니다.')
    high, low, change = st.columns(3)
    high.metric('🔺 최고', f"{format_number(frame['rate'].max())} {target}")
    low.metric('🔻 최저', f"{format_number(frame['rate'].min())} {target}")
    variation = (frame['rate'].iloc[-1] / frame['rate'].iloc[0] - 1) * 100
    change.metric('변동률', f'{variation:+.2f}%' if len(frame) >= 2 else '—')


def main():
    st.set_page_config(page_title='환율 계산기', page_icon='💱', layout='wide')
    st.markdown('''<style>
        .stApp {background: #fff; color: #202124;}
        .block-container {max-width: 1160px; padding-top: 3rem;}
        .rate-title {font-size: clamp(32px, 5vw, 48px); font-weight: 400; margin-bottom: 8px;}
        div[data-baseweb="input"], div[data-baseweb="select"] > div {
            border-color: #dadce0; border-radius: 10px; background: white;}
        div[role="radiogroup"] {gap: 8px; flex-wrap: wrap;}
        div[role="radiogroup"] label {border-radius: 20px; padding: 5px 10px;}
        div[role="radiogroup"] label:has(input:checked) {background: #e8f0fe; color: #1a73e8;}
        </style>''', unsafe_allow_html=True)
    for key, value in {'amount': 1.0, 'base_currency': 'USD',
                       'target_currency': 'KRW', 'selected_period': '1개월'}.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.title('💱 환율 계산기')
    header = st.container()
    left, right = st.columns([4, 6], gap='large')
    with left:
        with st.container(border=True):
            amount = st.number_input('💵 기준 금액', min_value=0.0, max_value=1e15,
                                     step=1.0, key='amount', format='%0.8f')
            base = st.selectbox('기준 통화', list(CURRENCIES), key='base_currency',
                                format_func=lambda code: f'{CURRENCIES[code]} ({code})')
            st.button('🔄 통화 교환', on_click=swap_currencies, width='stretch')
            result_area = st.empty()
            target = st.selectbox('대상 통화', list(CURRENCIES), key='target_currency',
                                  format_func=lambda code: f'{CURRENCIES[code]} ({code})')
    try:
        with st.spinner('최신 환율을 불러오는 중입니다...'):
            data = get_latest_rates(base)
        rate = data['conversion_rates'].get(target)
        if rate is None:
            raise ValueError('현재 지원하지 않는 대상 통화입니다.')
        with header:
            st.write(f'1 {CURRENCIES[base]} =')
            st.markdown(f'<div class="rate-title">{format_number(rate)} {CURRENCIES[target]}</div>',
                        unsafe_allow_html=True)
            st.caption('🕒 ExchangeRate-API 제공 · 마지막 업데이트 ' + format_update(data.get('time_last_update_unix')))
            st.caption('최신 제공 고시 환율입니다. 실제 거래 시 적용되는 환율과 다를 수 있습니다.')
        result_area.metric('💰 변환 결과', f'{format_number(amount * rate)} {target}')
    except ValueError as error:
        with header:
            st.warning(str(error))
        result_area.info('최신 환율을 불러오면 환산 결과가 표시됩니다.')
    with right:
        render_history(base, target)
        st.caption('과거 환율 데이터: Frankfurter · 최신 환율과 제공 시점 및 출처가 달라 값에 차이가 있을 수 있습니다.')


if __name__ == '__main__':
    main()
