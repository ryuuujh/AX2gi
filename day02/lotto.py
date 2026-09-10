# random 모듈을 이용해서 1~45 중 중복 없는 번호 6개를 뽑고
# 자료 구조 set, 버튼을 누르면 5세트를 한번에 생성 (list는 중복/ set은 중복 안됨)
# datetime 으로 생성 시간도 함께 보여준다
# 로또 v1
# 로또 v2
# 로또 v3

import streamlit as st
import random
from datetime import datetime

st.title("🎱 로또 번호 자동 생성기")
st.caption("버튼을 누르면 1~45 사이의 중복 없는 번호 6개짜리 세트를 5개 만든다")


# 로또 번호 1세트 만들기
def lotto_one_set() -> list:
    """1~45에서 중복 없이 번호 6개를 뽑아 정렬된 리스트로 반환"""

    number = set()

    while len(number) < 6:
        number.add(random.randint(1, 45))

    return sorted(number)


# 번호에 따라 색깔 공 붙이기
def lotto_color(num):

    if num < 10:
        return "🟡"

    elif num < 20:
        return "🔴"

    elif num < 30:
        return "🔵"

    elif num < 40:
        return "🟢"

    else:
        return "🟣"


st.markdown("---")


# 버튼을 눌렀을 때만 실행
if st.button("🍀 5세트 번호 생성하기", key="lotto_generate_btn"):

    # 생성 시간
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"생성 시각 : **{now_str}**")

    # 총 5세트 생성
    for set_index in range(1, 6):

        lotto_num = lotto_one_set()

        # 번호마다 색깔 공 붙이기
        result = ""

        for num in lotto_num:
            result += f"{lotto_color(num)} {num}　"

        st.write(f"**{set_index}세트** : {result}")