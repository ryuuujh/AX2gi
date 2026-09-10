import pandas as pd
import streamlit as st

st.title("🎤K-POP 아이돌 데이터 필터링&결측치 정리")
st.caption("한국인ㆍ외국인 조건으로 필터링해보고, 결측치를 제거해 새 csv로 저장합니다.")

upload_file = st.file_uploader("K-POP 아이돌 데이터셋 파일을 직접 업로드 해주세요", type="csv")

if upload_file is not None :
    df = pd.read_csv(upload_file)
else :
    df = None

if df is not None :

    # 나이 계산
    df["Date of Birth"] = pd.to_datetime(df["Date of Birth"], dayfirst=True)
    df["Age"] = 2026 - df["Date of Birth"].dt.year

    # 20세 미만 필터링
    st.subheader("1) 20세 미만 아이돌")

    under_20 = df[df["Age"] > 20]

    st.write(f"20세 미만 아이돌 수 : **{len(under_20)}명**")
    st.dataframe(
        under_20[["Stage Name", "Full Name", "Date of Birth", "Age", "Country"]].head()
    )
    
    # 한국인 필터링
    st.subheader("2) 한국인 아이돌")

    korean = df[df["Country"] == "South Korea"]

    st.write(f"한국인 아이돌 수 : **{len(korean)}명**")
    st.dataframe(korean[["Stage Name", "Full Name", "Country", "Gender"]].head())

    # 한국인이 아닌 아이돌 필터링
    st.subheader("3) 한국인이 아닌 아이돌")

    not_korean = df[df["Country"] != "South Korea"]

    st.write(f"한국인이 아닌 아이돌 수 : **{len(not_korean)}명**")
    st.dataframe(not_korean[["Stage Name", "Full Name", "Country", "Gender"]].head())

    st.markdown("---")

    # 두 조건을 동시에 만족하는 행 (20세 미만 한국인)

    st.subheader("4) 20세 미만 & 한국인 아이돌")

    under_20_korean = df[(df["Age"] < 20) & (df["Country"] == "South Korea")]

    st.write(f"20세 미만 & 한국인 아이돌 수: **{len(under_20_korean)}명**")

    st.dataframe(
        under_20_korean[["Stage Name", "Full Name", "Age", "Country"]].head()
    )

    st.markdown("---")

    # 국적(Country)의 결측치(NaN) 확인 및 dropna 처리
    st.subheader("4) Country 결측치 처리")

    missing_country_count = df["Country"].isna().sum()
    st.write(f"Country 열의 결측치 개수: **{missing_country_count}개**")

    # Country 열이 결측치인 행을 제거한다.
    df_clean = df.dropna(subset=["Country"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric("제거 전", f"{len(df)}행")

    with col2:
        st.metric("제거 후", f"{len(df_clean)}행")

    # 정리된 데이터를 csv 파일로 저장
    output_path = "kpop_idols_cleaned.csv"

    df_clean.to_csv(output_path, index=False)

    st.success("파일을 저장했습니다.")

    st.dataframe(df_clean.head(), use_container_width=True)