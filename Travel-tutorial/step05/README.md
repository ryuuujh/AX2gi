# 세계 여행 포털

## 1. 설치와 실행

PowerShell에서 다음 순서로 실행하세요. 테마 설정이 적용되도록 step05 폴더에서 실행합니다.

```powershell
cd C:\Users\user\AX2gi\Travel-tutorial\step05
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 2. 코드 흐름

1. `.streamlit/config.toml`에서 화면 테마를 정합니다.
2. `app.py`에서 앱 기본 설정과 한국·중국·일본·미국 메뉴를 만듭니다.
3. `src/views/`의 나라별 파일에서 소개, 수도, 언어, 여행지, 링크를 전달합니다.
4. `src/components/country_card.py`의 공통 함수가 화면을 표시합니다.
5. 여행 사이트 버튼을 누르면 외부 사이트로 이동합니다.

## 3. 이미지 추가

`assets/images/`에 `korea.jpg`, `china.jpg`, `japan.jpg`, `usa.jpg`를 넣고 새로고침하세요.
PNG, JPEG, WebP도 지원합니다. 이미지가 없으면 안내 문구가 표시됩니다.

## 4. 내용 변경

나라 소개와 링크는 `src/views/`에서, 공통 화면 모양은 `src/components/country_card.py`에서 수정하세요.
