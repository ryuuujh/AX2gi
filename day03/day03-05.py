# 인코딩을 순서대로 시도하고, 나눔고딕 에코로 그래프를 그려 저장합니다.
# 같은 폴더에 titanic_cleaned.csv와 NanumGothicEco.otf가 있어야 합니다.
# 실행: streamlit run day03-05.py

import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib import font_manager

CSV_PATH = os.path.join(os.path.dirname(__file__), "titanic_cleaned.csv")
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothicEco.otf")

st.title("📊 인코딩 자동 감지 + 한글 폰트 막대그래프 (Titanic 연습)")
st.caption("여러 인코딩을 순서대로 시도해서 파일을 읽고, 객실등급별 생존율을 그래프로 그립니다.")


def read_csv_auto_encoding(file_path):
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            st.write(f"{encoding}으로 읽었습니다.")
            return df
        except UnicodeDecodeError:
            pass
        except FileNotFoundError:
            st.error("titanic_cleaned.csv 파일을 찾을 수 없습니다.")
            return None

    st.error("지원하는 인코딩으로 파일을 디코딩할 수 없습니다.")
    return None


# 1. CSV 읽기
st.subheader("1) 인코딩 자동 감지")
df = read_csv_auto_encoding(CSV_PATH)

if df is None:
    st.stop()

# 2. 객실등급별 생존율 계산
st.markdown("---")
st.subheader("2) 객실등급별 생존율 표")

# Survived는 사망 0, 생존 1이므로 평균이 생존 비율입니다.
pclass_survival_rate = df.groupby("Pclass")["Survived"].mean().sort_index()
st.dataframe((pclass_survival_rate * 100).round(1).rename("생존율(%)"))

# 3. 나눔고딕 에코 폰트 설정 후 그래프 그리기
st.markdown("---")
st.subheader("3) 객실등급별 생존율 막대그래프")

try:
    # 폰트 파일을 등록합니다.
    font_manager.fontManager.addfont(FONT_PATH)

    # 파일에서 폰트 이름을 가져와 기본 폰트로 지정합니다.
    font_prop = font_manager.FontProperties(fname=FONT_PATH)
    plt.rcParams["font.family"] = font_prop.get_name()

    # 안내 문구는 한 번만 출력합니다.
    st.write("NanumGothicEco 폰트를 적용했습니다.")

except FileNotFoundError:
    st.error("NanumGothicEco.otf 파일을 파이썬 파일과 같은 폴더에 넣어주세요.")
    st.stop()

fig, ax = plt.subplots(figsize=(8, 5))
(pclass_survival_rate * 100).plot(kind="bar", color="blue", ax=ax)

ax.set_title("객실 등급별 생존율")
ax.set_xlabel("객실등급(Pclass)")
ax.set_ylabel("생존율(%)")
fig.tight_layout()

st.pyplot(fig)

# 4. 그래프를 같은 폴더에 PNG 파일로 저장
output_png = os.path.join(os.path.dirname(__file__), "pclass_survival_rate.png")
fig.savefig(output_png, dpi=150, bbox_inches="tight")
plt.close(fig)

st.caption("그래프를 pclass_survival_rate.png로 저장했습니다.")