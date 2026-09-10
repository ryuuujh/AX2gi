# 환율 계산기 실행

프로젝트 루트 AX2gi에서 실행합니다.

```powershell
python -m pip install -r MBTI/exchange_rate_app/requirements.txt
python -m streamlit run MBTI/exchange_rate_app/exchangerate.py
```

`MBTI/exchange_rate_app/.env`에 `EXCHANGE_API_KEY=발급받은키`를 설정할 수 있습니다.
기존 `MBTI/.env`와 프로젝트 루트 `.env`도 읽으므로 기존 키를 옮길 필요는 없습니다.
기존 루트 `.env`와 `EXCHANGE_RATE_API_KEY` 이름도 지원합니다.
Streamlit Cloud에서는 Secrets의 `EXCHANGE_API_KEY`를 우선 사용합니다.
실제 키를 소스나 문서에 넣지 마세요.

최신 환율은 ExchangeRate-API Standard endpoint를 5분 캐시하며,
금액 및 대상 통화 변경 시 전체 환율을 재사용합니다.
과거 그래프는 Frankfurter v2를 1시간 캐시합니다.
1일은 최근 가용 데이터 한 점, 5년/최대는 월별 데이터입니다.
최대는 1948년부터 요청하며 실제 통화쌍의 가용 구간만 표시됩니다.
월별 그래프의 최고/최저는 월별 표본 기준입니다.

공식 문서: https://www.exchangerate-api.com/docs/standard-requests
및 https://frankfurter.dev/

화면은 `exchangerate.py`, 최신 API는 `exchange_api.py`,
과거 API는 `historical_api.py`, 공통 포맷은 `utils.py`로 분리했습니다.
기존 `readme.md`는 원본 요구사항으로 보존합니다.
