# 환율 계산기 실습
# ExchangeRate-API를 이용해서 실시간 환율을 가져와 계산한다.
# 사전준비 ExchangeRate-API 회원가입 후 API Key 발급
# pip install streamlit requests python-dotenv pandas plotly
# 상위 폴더에 이미 .env 파일이 존재함
# .env 안에는 EXCHANGE_RATE_API_KEY = 발급받은 API 키 형태로 저장되어 있음
# 새로운 .env 파일을 만들지 말고 기존 상위 폴더의 .env를 사용한다.
# python-dotenv의 load_dotenv()를 이용해서 상위 폴더의 .env를 불러온다.
# API Key는 os.getenv("EXCHANGE_RATE_API_KEY")로 가져온다.
# API Key를 Python 코드에 직접 작성하지 않는다.

## 프로젝트 목표

Python + Streamlit으로 Google 환율 계산기와 비슷한 환율 계산기를 만들어줘.

최신 환율 API는 내가 이미 발급받은 **ExchangeRate-API**를 사용한다.

API:
https://app.exchangerate-api.com/

기본 화면은 다음 기능을 포함한다.

- 기본 금액: 1
- 기본 기준 화폐: KRW
- 기본 변환 화폐: USD
- 기준 화폐와 변환 화폐를 dropdown으로 직접 선택 가능
- 입력 금액을 변경하면 자동 환산
- `⇅` 버튼으로 두 화폐 위치 변경
- 상단에 현재 환율 크게 표시
- 업데이트 시간 표시

예:

```text
1 대한민국 원 =
0.00072 미국 달러
```

## 지원 화폐

최소 다음 화폐를 선택할 수 있게 한다.

- KRW 대한민국 원
- USD 미국 달러
- JPY 일본 엔
- EUR 유로
- CNY 중국 위안
- GBP 영국 파운드
- AUD 호주 달러
- CAD 캐나다 달러
- CHF 스위스 프랑
- HKD 홍콩 달러
- SGD 싱가포르 달러
- THB 태국 바트
- VND 베트남 동

화폐를 변경하면 환율 계산 결과와 그래프도 함께 변경한다.

예:

```text
KRW → USD 선택
→ KRW/USD 환율과 그래프

USD → JPY 선택
→ USD/JPY 환율과 그래프
```

## 환율 그래프

화면 오른쪽에는 Plotly 선 그래프를 만든다.

그래프는 현재 선택된 두 화폐의 환율 변동을 보여준다.

- X축: 날짜
- Y축: 환율
- hover 시 날짜와 환율 표시
- 흰색 배경
- 연한 grid
- 반응형 크기
- Google 환율 그래프처럼 간단한 디자인

기간 선택:

```text
1일 | 5일 | 1개월 | 1년 | 5년 | 최대
```

기본값은 `1개월`.

기간을 변경하면 해당 기간의 환율 그래프가 변경되어야 한다.

ExchangeRate-API 무료 플랜에서 과거 환율 데이터가 제공되지 않는 경우에는
Frankfurter 같은 무료 historical 환율 API를 그래프용으로 사용해도 된다.

단, 실제 환율 대신 random이나 가짜 데이터를 사용하지 않는다.

## API Key 불러오기

현재 프로젝트 폴더의 **상위 폴더에 `.env`가 존재한다.**

예를 들어 구조가 다음과 같다면:

```text
project/
│
├─ .env
│
└─ exchange/
   └─ app.py
```

`app.py`에서는 상위 폴더의 `.env`를 불러오도록 한다.

예:

```python
import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".env"
)

load_dotenv(ENV_PATH)

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
```

API Key가 없을 경우 앱이 종료되지 않도록:

```text
환율 API Key를 찾을 수 없습니다.
```

같은 안내를 표시한다.

API Key의 실제 값을 화면이나 로그에 출력하지 않는다.

## UI

첨부한 Google 환율 계산기 화면과 최대한 비슷하게 만든다.

- 왼쪽: 금액 입력 + 화폐 선택
- 오른쪽: 환율 그래프
- 흰색 배경
- 둥근 입력창
- 얇은 회색 테두리
- 파란색 포인트
- 넉넉한 여백
- 전체 폭 약 1100~1200px
- 모바일에서는 세로 배치

## 프로젝트 구조

현재 폴더 구조를 먼저 확인한 뒤 필요한 파일을 만든다.

가능하면:

```text
app.py
exchange_api.py
historical_api.py
requirements.txt
```

- `app.py` : Streamlit UI
- `exchange_api.py` : ExchangeRate-API
- `historical_api.py` : 그래프용 과거 환율 데이터

코드는 Python 초보자가 이해할 수 있도록 작성한다.

- 중요한 부분 한국어 주석
- 쉬운 변수명
- 불필요한 class 사용 금지
- 너무 복잡하게 추상화하지 않기
- `st.cache_data`를 사용해 API 과도한 호출 방지
- 금액만 바뀔 때 API를 매번 호출하지 않기

설명만 하지 말고 실제 실행 가능한 코드를 직접 작성해줘.

실행:

```bash
streamlit run app.py
```

마지막으로 다음을 확인해줘.

- API Key 정상 로드
- KRW → USD 기본 환율
- 금액 자동 계산
- 기준 화폐 변경
- 변환 화폐 변경
- Swap 버튼
- 선택한 화폐에 맞는 그래프
- 기간별 그래프
- API 오류 처리
- Python 문법/import 오류