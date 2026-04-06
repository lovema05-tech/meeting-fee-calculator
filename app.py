import streamlit as st

# 페이지 설정
st.set_page_config(page_title="모임 회비 관리 계산기", layout="wide")

# 제목 설정
st.title("모임 회비 관리 계산기")

# 세션 상태 초기화 (Clear 기능용)
if 'total_amount' not in st.session_state:
    st.session_state.total_amount = 0
if 'num_people' not in st.session_state:
    st.session_state.num_people = 1
if 'tip_ratio' not in st.session_state:
    st.session_state.tip_ratio = 0.0

# 화면 레이아웃 (왼쪽: 입력, 오른쪽: 결과)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("사용 금액 입력")
    # 입력 필드 (총금액, 인원수, 팁 비율)
    # session_state를 직접 사용하여 값을 초기화할 수 있도록 구성
    total_amount = st.number_input("총금액 (원)", min_value=0, value=st.session_state.total_amount, key="input_total")
    num_people = st.number_input("인원수 (명)", min_value=1, value=st.session_state.num_people, key="input_people")
    tip_ratio = st.number_input("팁/서비스 비율 (%)", min_value=0.0, max_value=100.0, value=st.session_state.tip_ratio, step=0.1, key="input_tip")

with col_right:
    st.subheader("계산 결과")
    # 초기값 설정
    res_amount_per_person = 0
    res_total_with_tip = 0
    
    # 세션에 저장된 결과가 있으면 표시 (Submit 클릭 후 유지용)
    if 'res_amount_per_person' in st.session_state:
        res_amount_per_person = st.session_state.res_amount_per_person
        res_total_with_tip = st.session_state.res_total_with_tip

    st.metric("1인당 금액 (원)", f"{int(res_amount_per_person):,}원")
    st.metric("팁 포함 총 금액 (원)", f"{int(res_total_with_tip):,}원")

# 하단 버튼 레이아웃
btn_col1, btn_col2, _ = st.columns([1, 1, 4])

# Submit 버튼 클릭 시 계산 수행
if btn_col2.button("Submit"):
    # 계산 로직
    total_with_tip = total_amount * (1 + tip_ratio / 100)
    amount_per_person = total_with_tip / num_people if num_people > 0 else 0
    
    # 결과를 세션에 저장하여 화면 유지
    st.session_state.res_amount_per_person = amount_per_person
    st.session_state.res_total_with_tip = total_with_tip
    st.rerun()

# Clear 버튼 클릭 시 입력값 및 결과 초기화
if btn_col1.button("Clear"):
    st.session_state.total_amount = 0
    st.session_state.num_people = 1
    st.session_state.tip_ratio = 0.0
    if 'res_amount_per_person' in st.session_state:
        del st.session_state.res_amount_per_person
    if 'res_total_with_tip' in st.session_state:
        del st.session_state.res_total_with_tip
    st.rerun()
