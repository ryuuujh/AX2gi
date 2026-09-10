# raw_trade_data.csv 파일 활용
# HS코드가 85로 시작하는 (반도체류) + 국가명 미국 또는 베트남 +  수출금액 0 보다 큰 수(실제 수출실적이 있는) 행만
# 다중 조건으로 필더링 한 뒤, 수출금액 상위 10건을 화면에 보여주고 report.csv 로 저장
# streamlit 사용 streamlit run day04-01.py 11

from pathlib import Path  # 파일 경로 처리

import pandas as pd  # CSV 읽기와 필터링
import streamlit as st  # 웹 화면 표시


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "common" / "raw_trade_data.csv"
REPORT_PATH = BASE_DIR / "report.csv"

st.set_page_config(page_title="무역 데이터 분석", layout="wide")
st.title("수출금액 상위 10건")
st.caption("HS 코드 85로 시작 · 국가명 미국 또는 베트남 · 수출금액 0 초과")

# 1. CSV를 읽습니다. HS 코드는 앞자리 검색을 위해 문자열로 읽습니다.
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", dtype={"hs_code": "string"})
    required = {"hs_code", "국가명", "수출금액"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"필수 컬럼이 없습니다: {', '.join(sorted(missing))}")
    df["수출금액"] = pd.to_numeric(df["수출금액"], errors="coerce")
except (OSError, ValueError) as error:
    st.error(f"CSV 파일을 읽을 수 없습니다: {error}")
    st.stop()

# 2. &는 모든 조건을 만족하는 행을 선택합니다.
condition = (
    df["hs_code"].str.strip().str.startswith("85", na=False)
    & df["국가명"].str.strip().isin(["미국", "베트남"])
    & (df["수출금액"] > 0)
)
filtered = df.loc[condition]

# 3. 수출금액이 큰 순서로 정렬하고 상위 10건을 추출합니다.
# 금액이 같으면 원본 행 순서를 유지합니다.
top10 = filtered.sort_values("수출금액", ascending=False, kind="stable").head(10)
st.metric("조건에 맞는 전체 데이터", f"{len(filtered):,}건")
st.caption("금액은 원본 CSV의 단위를 사용합니다.")
if top10.empty:
    st.info("조건에 맞는 데이터가 없습니다.")
st.dataframe(top10, hide_index=True)

# 4. 파이썬 파일과 같은 폴더에 보고서를 저장합니다.
# UTF-8 BOM을 포함하면 엑셀에서도 한글을 읽기 쉽습니다.
report = top10.to_csv(index=False).encode("utf-8-sig")
try:
    REPORT_PATH.write_bytes(report)
    st.success(f"보고서 저장 완료: {REPORT_PATH}")
except OSError as error:
    st.error(f"보고서 저장에 실패했습니다: {error}")

st.download_button(
    "report.csv 다운로드",
    data=report,
    file_name="report.csv",
    mime="text/csv",
)
