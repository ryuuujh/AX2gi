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
        line={'color': '#174ea6', 'width': 3}, marker={'size': 7},
        customdata=[str(value) for value in frame['rate']],
        hovertemplate='%{x|%Y-%m-%d}<br>%{customdata} ' + target + '<extra></extra>',
    ))
    figure.update_layout(height=350, margin=dict(l=10, r=10, t=15, b=15),
                         showlegend=False, paper_bgcolor='white', plot_bgcolor='white',
                         font=dict(color='#243247', size=14), hovermode='x unified',
                         hoverlabel=dict(bgcolor='white', font_color='#172033', font_size=15))
    figure.update_xaxes(showgrid=False, title=None)
    figure.update_yaxes(gridcolor='#d9e1eb', zeroline=False, tickformat='.6g', title=None)
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
        /* 기기의 다크 모드에서도 흰 배경과 진한 글자 조합을 유지한다. */
        .stApp {background: #fff; color: #172033; color-scheme: light;}
        .block-container {max-width: 1160px; padding-top: 3rem;}
        .stApp h1, .stApp h2, .stApp h3,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stWidgetLabel"],
        .stApp [data-testid="stMetricLabel"],
        .stApp [data-testid="stMetricValue"] {color: #172033;}
        .stApp [data-testid="stCaptionContainer"] {
            color: #374151; font-size: 0.95rem; line-height: 1.6;}
        .stApp [data-testid="stWidgetLabel"] p {font-weight: 650; font-size: 1rem;}
        div[data-baseweb="input"], div[data-baseweb="select"] > div {
            border: 1px solid #78879b; border-radius: 10px; background: #fff;
            color: #172033; min-height: 48px;}
        .stApp input, div[data-baseweb="select"] input {
            color: #172033 !important; -webkit-text-fill-color: #172033;
            font-size: 16px !important; font-weight: 600; caret-color: #174ea6;}
        div[data-baseweb="select"] span {color: #172033; font-weight: 600;}
        div[data-baseweb="select"] svg {color: #172033;}
        /* 선택 목록은 본문 밖에 렌더링되므로 별도로 지정한다. */
        div[data-baseweb="popover"], ul[role="listbox"], li[role="option"] {
            background: #fff; color: #172033; color-scheme: light;}
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background: #dbeafe; color: #123c80;}
        .stApp [data-testid="stButton"] button {
            background: #174ea6; color: #fff; border: 2px solid #174ea6;
            min-height: 48px; border-radius: 10px; font-weight: 700;}
        .stApp [data-testid="stButton"] button p {color: #fff; font-weight: 700;}
        .stApp [data-testid="stButton"] button:hover {
            background: #103b80; border-color: #103b80; color: #fff;}
        .stApp [data-testid="stNumberInput"] button {
            background: #e8eef7; color: #172033; border-left: 1px solid #78879b;}
        .stApp [data-testid="stNumberInput"] button:disabled {
            background: #f1f5f9; color: #64748b;}
        .stApp button:focus-visible, div[data-baseweb="input"]:focus-within,
        div[data-baseweb="select"]:focus-within {
            outline: 3px solid #174ea6; outline-offset: 3px;}
        div[role="radiogroup"] {gap: 8px; flex-wrap: wrap;}
        div[role="radiogroup"] label {
            border: 1px solid #78879b; border-radius: 22px; padding: 8px 12px;
            min-height: 44px; background: #f1f5f9; color: #172033;}
        div[role="radiogroup"] label p {color: #172033; font-weight: 600;}
        div[role="radiogroup"] label:has(input:checked) {
            background: #174ea6; border-color: #174ea6; color: #fff;}
        div[role="radiogroup"] label:has(input:checked) p {color: #fff;}
        div[role="radiogroup"] label:focus-within {outline: 3px solid #174ea6; outline-offset: 3px;}
        .stApp [data-testid="stAlert"] {background: #edf4ff; color: #172033; border: 1px solid #78879b;}
        .stApp a {color: #174ea6;}
        @media (max-width: 640px) {
            .block-container {padding: 1.5rem 1rem;}
            .stApp h1 {font-size: 2rem;}
            .stApp [data-testid="stMetricValue"] {font-size: 1.65rem; overflow-wrap: anywhere;}
        }
        </style>''', unsafe_allow_html=True)
    for key, value in {'amount': 1.0, 'base_currency': 'USD',
                       'target_currency': 'KRW', 'selected_period': '1개월'}.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.title('💱 환율 계산기')
    st.write('금액과 통화를 선택하면 환산 결과를 바로 확인할 수 있습니다. 그래프에서 기간별 환율 변화도 살펴보세요.')
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
