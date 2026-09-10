import io
import pandas as pd
import streamlit as st

st.title("🎤K-POP 테이터셋 기초 탐색")
st.caption("pandas의 head/tail/shape/info/columns로 데이터셋 기본 정보를 확인합니다.")

upload_file = st.file_uploader("K-POP 아이돌 데이터셋 파일을 직접 업로드 해주세요", type="csv")

if upload_file is not None :
    df = pd.read_csv(upload_file)
else:
    # st.error("K-POP 데이터셋 파일을 업로드 해주세요")
    # st.info("csv파일을 폴더에 넣고 새로고침 하세요")
    df= None

if df is not None :
    st.subheader("1) head() : 데이터의 앞부분 5개 행 미리보기")
    st.dataframe(df.head(),use_container_width=True) # 기본행 5개

    st.subheader("2) tail() : 데이터의 뒷부분 5개 행 미리보기")
    st.dataframe(df.tail(),use_container_width=True) # 기본행 5개

    st.subheader("3) shape() : 행 개수, 열 개수")
    col1, col2 = st.columns(2)
    with col1 : 
        st.metric("행 개수",f"{df.shape[0]}개")

    with col2 : 
        st.metric("열 개수",f"{df.shape[1]}개")

    st.subheader("4) columns : 전체 열(컬럼) 이름 목록")
    # st.write(df.columns)
    st.write(list(df.columns))

    st.subheader("5) info() : 각 열의 자료형과 결측치(Nan) 여부 요약")
    # df.info 는 값을 리턴하지 않고 화면에 직접 출력만 해주는 함수라서
    # io.StringIO() 라는 "메모리 위의 가짜 파일"에 결과를 받아 낸 뒤 그 내용을 text로 보여준다

    # buffer = io.StringIO()
    # df.info(buf=buffer)
    # st.text(buffer.getvalue())

    info_df = pd.DataFrame({
        "타입" : df.dtypes,
        "결측치 아닌 개수" :  df.notna().sum(),
        "결측치 개수" : df.isna().sum(),

    })
    st.dataframe(info_df, use_container_width= True)

    st.success("기초 정보 확인이 끝났습니다.")