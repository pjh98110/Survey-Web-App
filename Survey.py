import streamlit as st
# st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.colored_header import colored_header

# import matplotlib.pyplot as plt
# from plotly.subplots import make_subplots


# add_page_title()

show_pages(
    [
        Page("Survey.py", "문진표", "✅"),
        Page("pages/Analysis.py", "분석 결과", "📄"),
        Page("pages/Xai_dashboard.py", "XAI_explainer", "📘"),
        Page("pages/Xai_omni.py", "XAI_omni", "📗"),
    ]
)

if "page" not in st.session_state:
    st.session_state.page = "Survey"

DATA_PATH = "./"
SEED = 42

# 데이터 불러오는 함수(캐싱)
@st.cache_data # 캐싱 데코레이터
def load_csv(path):
    return pd.read_csv(path)


def reset_seeds(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)


# 세션 변수에 저장
if 'type_of_case' not in st.session_state:
    st.session_state.type_of_case = None

if 'selected_gender' not in st.session_state:
    st.session_state.selected_gender = None

if 'selected_age' not in st.session_state:
    st.session_state.selected_age = None

if 'selected_cancer' not in st.session_state:
    st.session_state.selected_cancer = None

if 'total_score' not in st.session_state:
    st.session_state.total_score = []

if 'selected_survey' not in st.session_state:
    st.session_state.selected_survey = []




# 타이틀
colored_header(
    label='문진표를 통한 맞춤형 분석 결과 제공',
    description=None,
    color_name="green-70",
)


# [사이드바]
st.sidebar.markdown(f"""
            <span style='font-size: 20px;'>
            <div style=" color: #000000;">
                <strong>성별 및 연령대 선택</strong>
            </div>
            """, unsafe_allow_html=True)


# 사이드바에서 성별, 연령대 선택
selected_gender = st.sidebar.selectbox("(1) 당신의 성별을 선택하세요:", ('남성', '여성'))
selected_age = st.sidebar.selectbox("(2) 당신의 연령대를 선택하세요:", ('10대', '20대', '30대', '40대', '50대', '60대', '70대 이상'))
selected_cancer = st.sidebar.selectbox("(3) 당신의 암 유무를 알려주세요:", ('유', '무'))

# 사이드바 구분선
# st.sidebar.divider()


# 일반건강검진(2012~2021)
# 암 건강검진

# 중복 선택할 경우
# # 선택한 값이 세션 상태에 있으면 그 값을 기본값으로 사용하고, 그렇지 않으면 빈 리스트를 사용합니다.
# default_value = st.session_state.get('selected_survey', [])

# selected = st.multiselect(
#     "원하는 문진표를 선택하세요.",
#     options=["암검진 문진표", "일반건강검진 문진표"],
#     default=default_value,
#     placeholder="하나를 선택하세요.",
#     help="선택한 문진표에 따라 다른 분석 결과를 제공합니다."
# )

# # 사용자의 선택을 세션 상태에 저장합니다.
# if st.button("선택 완료"):
#     st.session_state.selected_survey = selected


selected_survey = st.selectbox(
    "원하는 문진표를 선택하세요.",
    options=["암검진 문진표", "일반건강검진 문진표"],
    placeholder="하나를 선택하세요.",
    help="선택한 문진표에 따라 다른 분석 결과를 제공합니다."
)

st.session_state.selected_survey = selected_survey


if selected_survey == "암검진 문진표":

    # 문진 결과를 저장할 딕셔너리
    st_results = {}

    # 문진 문항과 선택지 및 사용자 응답 수집
    questions = {
        "question1" : st.selectbox("[문진1] 현재 신체 어느 부위에 든 불편한증상이 있습니까?", ("있음", "없음")),
        "question2" : st.selectbox("[문진2] 지난 6개월 간 특별한 이유 없이 5kg 이상의 체중감소가 있었습니까?", ("아니오", "체중감소")),
        "question3" : st.multiselect("[문진3] 위암 유무", ("없다", "모르겠다", "(본인)있다", "(부모)있다", "(형제)있다", "(자매)있다", "(자녀)있다"), key="q3"),
        "question3_1" : st.multiselect("[문진3] 유방암 유무", ("없다", "모르겠다", "(본인)있다", "(부모)있다", "(형제)있다", "(자매)있다", "(자녀)있다"), key="q3_1"),
        "question3_2" : st.multiselect("[문진3] 대장암 유무", ("없다", "모르겠다", "(본인)있다", "(부모)있다", "(형제)있다", "(자매)있다", "(자녀)있다"), key="q3_2"),
        "question3_3" : st.multiselect("[문진3] 간암 유무", ("없다", "모르겠다", "(본인)있다", "(부모)있다", "(형제)있다", "(자매)있다", "(자녀)있다"), key="q3_3"),
        "question3_4" : st.multiselect("[문진3] 자궁경부암 유무", ("없다", "모르겠다", "(본인)있다", "(부모)있다", "(형제)있다", "(자매)있다", "(자녀)있다"), key="q3_4"),
        "question3_5" : st.multiselect("[문진3] 기타암 유무", ("없다", "모르겠다", "(본인)있다", "(부모)있다", "(형제)있다", "(자매)있다", "(자녀)있다"), key="q3_5"),
        "question4" : st.selectbox("[문진4] 과거병력 위.십이지장궤양 유무", ("있음", "없음"), key="q4"),
        "question5" : st.selectbox("[문진5] 위축성 위염 유무", ("있다", "없다"), key="q5"),
        "question5_1" : st.selectbox("[문진5] 장상피화생 유무", ("있다", "없다"), key="q5_1"),
        "question5_2" : st.selectbox("[문진5] 위용종 유무", ("있다", "없다"), key="q5_2"),
        "question5_3" : st.selectbox("[문진5] 기타 유무", ("있다", "없다"), key="q5_3"),
        "question6" : st.selectbox("[문진6] 암과관련된 검사경험-위투시촬영(UGI)유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q6"),
        "question6_1" : st.selectbox("[문진6] 암과관련된 검사경험-위내시경 유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q6_1"),
        "question6_2" : st.selectbox("[문진6] 암과관련된 검사경험-대변잠혈검사유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q6_2"),
        "question6_3" : st.selectbox("[문진6] 암과관련된 검사경험-대장내시경유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q6_3"),
        "question6_4" : st.selectbox("[문진6] 암과관련된 검사경험-간초음파 유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q6_4"),
        "question6_5" : st.selectbox("[문진6] 현재 또는 과거에 진단받은 대장 항문질환이 있으십니까?", ("있다", "없다"), key="q6_5"),
        "question6_6" : st.selectbox("[문진6] 크론병 유무", ("있다", "없다"), key="q6_6"),
        "question6_7" : st.selectbox("[문진6] 치질(치핵.치열) 유무", ("있다", "없다"), key="q6_7"),
        "question6_8" : st.selectbox("[문진6] 만성B형간염 유무", ("있다", "없다"), key="q6_8"),
        "question6_9" : st.selectbox("[문진6] 만성C형간염 유무", ("있다", "없다"), key="q6_9"),
        "question7" : st.selectbox("[문진7] 간 질환이 있으십니까?", ("있다", "없다"), key="q7"),

    }
    # 54개의 공통 질문


    if selected_gender == "여성":
        questions["question11"] = st.text_input("[문진11] 여성문항 - 초경연령", placeholder="만 _세", key="q11"),
        questions["question13"] = st.text_input("[문진13] 여성문항 - 폐경연령", placeholder="만 _세", key="q13"),
        questions["question14"] = st.selectbox("[문진14] 여성문항 - 여성호르몬투약 유무", ("호르몬 제제를 복용한 적 없음", "2년 미만 복용", "2년 이상~5년 미만 복용", "5년 이상 복용", "모르겠음"), key="q14"),
        questions["question15"] = st.text_input("[문진15] 여성문항 - 초경 시기", placeholder="만 _세", help="초경 없음 = 0", key="q15"),
        questions["question19"] = st.selectbox("[문진19] 먹는 피임약을 써본 적이 있습니까", ("피임약을 복용한 적 없음", "1년 미만 복용", "1년 이상 복용", "모르겠음"), key="q19"),
        questions["question20"] = st.selectbox("[문진20] 암과관련된 검사경험- 유방엑스선검사유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q20"),
        questions["question20_1"] = st.selectbox("[문진20] 암과관련된 검사경험- 자궁경부암검사유무", ("10년 이상 또는 한적 없음", "1년 이내", "1년~ 2년 사이", "2년~10년 사이"), key="q20_1"),



    # 문진 문항별 가중치
    weight_dict = {
        "question1": 1,
        "question2": 0.5,
        "question3": 1.5,
    }

    # 각 선택지에 대한 점수
    score_dict = {
        "있음": 1,
        "없음": 0,
        "있다": 1,
        "없다": 0,
        "예": 1,
        "아니오": 0,
        "체중감소": 1,
        "모르겠다": 0,
        "(본인)있다": 1, # 과거병력 유무
        "(부모)있다": 1, # 과거병력 유무
        "(형제)있다": 1, # 과거병력 유무
        "(자매)있다": 1, # 과거병력 유무
        "(자녀)있다": 1, # 과거병력 유무   
        "10년 이상 또는 한적 없음": 2, # 암 관련 검사경험
        "1년 이내": 0, # 암 관련 검사경험
        "1년~ 2년 사이": 1, # 암 관련 검사경험
        "2년~10년 사이": 1.5, # 암 관련 검사경험
        "호르몬 제제를 복용한 적 없음": 0, # 여성 호르몬 투약 유무
        "2년 미만 복용": 1, # 여성 호르몬 투약 유무
        "2년 이상~5년 미만 복용": 1.5, # 여성 호르몬 투약 유무
        "5년 이상 복용": 2, # 여성 호르몬 투약 유무
        "피임약을 복용한 적 없음": 0, # 피임약 복용 관련
        "1년 미만 복용": 0.5, # 피임약 복용 관련
        "1년 이상 복용": 1, # 피임약 복용 관련
    }

    # 총 점수를 계산하는 함수 (가중치 적용)
    # def calculate_total_score(score_dict, st_results, weight_dict):
    #     total_score = 0
    #     for question, answer in st_results.items():
    #         weight = weight_dict.get(question, 1)  # 문진에 대한 가중치를 가져옴
    #         total_score += score_dict.get(tuple(answer), 0) * weight  # 가중치를 적용하여 점수를 더함
    #         # total_score += score_dict.get(answer, 0) * weight  # 가중치를 적용하여 점수를 더함
    #     return total_score
    


    # 총 점수를 계산하는 함수 (가중치 적용)
    def calculate_total_score(score_dict, st_results, weight_dict):
        total_score = 0
        for question, answer in st_results.items():
            weight = weight_dict.get(question, 1)  # 문진에 대한 가중치를 가져옴
            
            # answer가 리스트 형태인 경우 (multiselect에서 반환된 경우)
            if isinstance(answer, list):
                for ans in answer:
                    total_score += score_dict.get(ans, 0) * weight  # 가중치를 적용하여 점수를 더함
            else:
                total_score += score_dict.get(answer, 0) * weight  # 가중치를 적용하여 점수를 더함
        return total_score



    # 총 점수 계산
    total_score = calculate_total_score(score_dict, questions, weight_dict)

    # 건강 상태 초기값 설정
    selected_item = None

    # 제출 버튼을 누를 경우
    if st.button("제출"):
        if selected_gender == "남성":
            # 남성일 때의 기준
            if total_score <= 20:
                selected_item = "건강"
            elif 20 < total_score <= 25:
                selected_item = "보통"
            else:
                selected_item = "위험"

        elif selected_gender == "여성":
            # 여성일 때의 기준
            if total_score <= 20:
                selected_item = "건강"
            elif 20 < total_score <= 25:
                selected_item = "보통"
            else:
                selected_item = "위험"
        st.markdown(f"당신의 성별은 {selected_gender}이며, 연령대는 {selected_age}입니다.")
        st.markdown(f"당신의 건강 상태는 '{selected_item}'입니다.")
        st.markdown(f"문진 결과를 기반으로 원하는 정보를 선택하세요")



    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #A7FFEB;
            width: 100%; /
            display: inline-block;
            margin: 0; /
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    def page1():
        want_to_analysis = st.button("분석 결과")
        if want_to_analysis:
            st.session_state.type_of_case = "Analysis"
            switch_page("분석 결과")


    def page2():
        want_to_Xai_dashboard = st.button("XAI_explainer")
        if want_to_Xai_dashboard:
            st.session_state.type_of_case = "Xai_dashboard"
            switch_page("XAI_explainer")

    def page3():
        want_to_Xai_dashboard2 = st.button("XAI_omni")
        if want_to_Xai_dashboard2:
            st.session_state.type_of_case = "Xai_dashboard2"
            switch_page("XAI_omni")


    col1, col2, col3 = st.columns(3)
    with col1:
        page1()
    with col2:
        page2()
    with col3:
        page3()


if selected_survey == "일반건강검진 문진표":

    # 문진 결과를 저장할 딕셔너리
    st_results = {}

    # 문진 문항과 선택지 및 사용자 응답 수집
    questions = {
        "question1" : st.selectbox("[문진1] 뇌졸증(중풍) 진단여부", ("있음", "없음"), key="p1"),
        "question1_1" : st.selectbox("[문진1] 심장병(심근경색/협심증) 진단여부", ("있음", "없음"), key="p1_1"),
        "question1_2" : st.selectbox("[문진1] 고혈압 진단여부", ("있음", "없음"), key="p1_2"),
        "question1_3" : st.selectbox("[문진1] 당뇨병 진단여부", ("있음", "없음"), key="p1_3"),
        "question1_4" : st.selectbox("[문진1] 이상지질혈증 진단여부", ("있음", "없음"), key="p1_4"),
        "question1_5" : st.selectbox("[문진1] 폐결핵 진단여부", ("있음", "없음"), key="p1_5"),
        "question1_6" : st.selectbox("[문진1] 기타(암포함) 진단여부", ("있음", "없음"), key="p1_6"),
        "question1_7" : st.selectbox("[문진1] 뇌졸증(중풍) 약물치료여부", ("있음", "없음"), key="p1_7"),
        "question1_8" : st.selectbox("[문진1] 심장병(심근경색/협심증) 약물치료여부", ("있음", "없음"), key="p1_8"),
        "question1_9" : st.selectbox("[문진1] 고혈압 약물치료여부", ("있음", "없음"), key="p1_9"),
        "question1_10" : st.selectbox("[문진1] 당뇨병 약물치료여부", ("있음", "없음"), key="p1_10"),
        "question1_11" : st.selectbox("[문진1] 이상지질혈증 약물치료여부", ("있음", "없음"), key="p1_11"),
        "question1_12" : st.selectbox("[문진1] 폐결핵 약물치료여부", ("있음", "없음"), key="p1_12"),
        "question1_13" : st.selectbox("[문진1] 기타(암포함) 약물치료여부", ("있음", "없음"), key="p1_13"),
        "question2_1" : st.selectbox("[문진2] 뇌졸증(중풍) 가족력여부", ("있음", "없음"), key="p2_1"),
        "question2_2" : st.selectbox("[문진2] 심장병(심근경색/협심증) 가족력여부", ("있음", "없음"), key="p2_2"),
        "question2_3" : st.selectbox("[문진2] 고혈압 가족력여부", ("있음", "없음"), key="p2_3"),
        "question2_4" : st.selectbox("[문진2] 당뇨병 가족력여부", ("있음", "없음"), key="p2_4"),
        "question2_5" : st.selectbox("[문진2] 기타(암포함) 가족력여부", ("있음", "없음"), key="p2_5"),
        "question3" : st.selectbox("[문진3] B형간염 항원보유자입니까?", ("예", "아니요", "모름"), key="p3"),
    }

    questions["question4"] = st.selectbox("[문진4] 지금까지 평생 총 5갑(100개비)이상의 담배를 피운 적이 있습니까?", ("예", "아니요"), key="p4")
    if questions["question4"] == "예":
        questions["question4_1"] = st.text_input("[문진4-1] 현재 일반담배(궐련)을 피운다. ", placeholder="총__년", key="p4_1")
        questions["question4_2"] = st.text_input("[문진4-1] 현재 일반담배(궐련)를 피운다. ", placeholder="하루평균__개비", key="p4_2")
        questions["question4_3"] = st.text_input("[문진4-2] 과거에는 일반담배(궐련)를 피웠으나 현재 피우지 않음", placeholder="총__년", key="p4_3")
        questions["question4_4"] = st.text_input("[문진4-2] 과거에는 일반담배(궐련)를 피웠으나 현재 피우지 않음", placeholder="흡연했을 때 하루평균__개비", key="p4_4")
        questions["question4_5"] = st.text_input("[문진4-2] 과거에는 일반담배(궐련)를 피웠으나 현재 피우지 않음", placeholder="끊은 지__년", key="p4_5")

    questions["question5"] = st.selectbox("[문진5] 지금까지 궐련형 전자담배 (가열담배, 예)아이코스, 글로, 릴 등)을 피운적 있습니까?", ("예", "아니요"), key="p5")
    if questions["question5"] == "예":
        questions["question5_1"] = st.text_input("[문진5-1] 현재 궐련형 전자담배(가열담배)를 피운다.", placeholder="총__년", key="p5_1")
        questions["question5_2"] = st.text_input("[문진5-1] 현재 궐련형 전자담배(가열담배)를 피운다.", placeholder="하루평균__개비", key="p5_2")
        questions["question5_3"] = st.text_input("[문진5-2] 과거에는 궐련형 전자담배(가열담배)를 피웠으나 현재 피우지 않음", placeholder="총__년", key="p5_3")
        questions["question5_4"] = st.text_input("[문진5-2] 과거에는 궐련형 전자담배(가열담배)를 피웠으나 현재 피우지 않음", placeholder="흡연했을 때 하루평균__개비", key="p5_4")
        questions["question5_5"] = st.text_input("[문진5-2] 과거에는 궐련형 전자담배(가열담배)를 피웠으나 현재 피우지 않음", placeholder="끊은 지__년", key="p5_5")

    questions["question6"] = st.selectbox("[문진6] 액상형 전자담배를 사용한 경험이 있습니까?", ("예", "아니요"), key="p6")
    if questions["question6"] == "예":
        questions["question6_1"] = st.selectbox("[문진6-1] 최근 한 달 동안 액상형 전자담배를 사용한 경험이 있습니까?", ("아니요", "월 1~2일", "월 3~9일", "월 10~29일", "매일"), key="p6_1")

    questions["question7"] = st.selectbox("[문진7] 술을 마시는 횟수는 어느 정도입니까?", ("일주일에 ( )번", "한 달에 ( )번", "1년에 ( )번", "술을 마시지 않는다."), key="p7")
    if questions["question7"] == "일주일에 ( )번":
        questions["question7_1"] = st.text_input("[문진7] 술을 마시는 횟수", placeholder="일주일에 ( )번", key="p7_1")
    elif questions["question7"] == "한 달에 ( )번":
        questions["question7_2"] = st.text_input("[문진7] 술을 마시는 횟수", placeholder="한 달에 ( )번", key="p7_2")
    elif questions["question7"] == "1년에 ( )번":
        questions["question7_3"] = st.text_input("[문진7] 술을 마시는 횟수", placeholder="1년에 ( )번", key="p7_3")

    questions["question7_4"] = st.selectbox("[문진7-1] 술을 마시는 날은 보통 어느 정도 마십니까?(소주)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_4")
    if questions["question7_4"] == "잔":
        questions["question7_5"] = st.text_input("[문진7-1] 하루에 마시는 소주 총 양", placeholder="소주 ( )잔", key="p7_5")
    elif questions["question7_4"] == "병":
        questions["question7_6"] = st.text_input("[문진7-1] 하루에 마시는 소주 총 양", placeholder="소주 ( )병", key="p7_6")
    elif questions["question7_4"] == "캔":
        questions["question7_7"] = st.text_input("[문진7-1] 하루에 마시는 소주 총 양", placeholder="소주 ( )캔", key="p7_7")
    elif questions["question7_4"] == "cc":
        questions["question7_8"] = st.text_input("[문진7-1] 하루에 마시는 소주 총 양", placeholder="소주 ( )cc", key="p7_8")

    questions["question7_9"] = st.selectbox("[문진7-1] 술을 마시는 날은 보통 어느 정도 마십니까?(맥주)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_9")
    if questions["question7_9"] == "잔":
        questions["question7_10"] = st.text_input("[문진7-1] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )잔", key="p7_10")
    elif questions["question7_9"] == "병":
        questions["question7_11"] = st.text_input("[문진7-1] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )병", key="p7_11")
    elif questions["question7_9"] == "캔":
        questions["question7_12"] = st.text_input("[문진7-1] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )캔", key="p7_12")
    elif questions["question7_9"] == "cc":
        questions["question7_13"] = st.text_input("[문진7-1] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )cc", key="p7_13")

    questions["question7_14"] = st.selectbox("[문진7-1] 술을 마시는 날은 보통 어느 정도 마십니까?(양주)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_14")
    if questions["question7_14"] == "잔":
        questions["question7_15"] = st.text_input("[문진7-1] 하루에 마시는 양주 총 양", placeholder="양주 ( )잔", key="p7_15")
    elif questions["question7_14"] == "병":
        questions["question7_16"] = st.text_input("[문진7-1] 하루에 마시는 양주 총 양", placeholder="양주 ( )병", key="p7_16")
    elif questions["question7_14"] == "캔":
        questions["question7_17"] = st.text_input("[문진7-1] 하루에 마시는 양주 총 양", placeholder="양주 ( )캔", key="p7_17")
    elif questions["question7_14"] == "cc":
        questions["question7_18"] = st.text_input("[문진7-1] 하루에 마시는 양주 총 양", placeholder="양주 ( )cc", key="p7_18")

    questions["question7_19"] = st.selectbox("[문진7-1] 술을 마시는 날은 보통 어느 정도 마십니까?(막걸리)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_19")
    if questions["question7_19"] == "잔":
        questions["question7_20"] = st.text_input("[문진7-1] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )잔", key="p7_20")
    elif questions["question7_19"] == "병":
        questions["question7_21"] = st.text_input("[문진7-1] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )병", key="p7_21")
    elif questions["question7_19"] == "캔":
        questions["question7_22"] = st.text_input("[문진7-1] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )캔", key="p7_22")
    elif questions["question7_19"] == "cc":
        questions["question7_23"] = st.text_input("[문진7-1] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )cc", key="p7_23")

    questions["question7_24"] = st.selectbox("[문진7-1] 술을 마시는 날은 보통 어느 정도 마십니까?(와인)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_24")
    if questions["question7_24"] == "잔":
        questions["question7_25"] = st.text_input("[문진7-1] 하루에 마시는 와인 총 양", placeholder="와인 ( )잔", key="p7_25")
    elif questions["question7_24"] == "병":
        questions["question7_26"] = st.text_input("[문진7-1] 하루에 마시는 와인 총 양", placeholder="와인 ( )병", key="p7_26")
    elif questions["question7_24"] == "캔":
        questions["question7_27"] = st.text_input("[문진7-1] 하루에 마시는 와인 총 양", placeholder="와인 ( )캔", key="p7_27")
    elif questions["question7_24"] == "cc":
        questions["question7_28"] = st.text_input("[문진7-1] 하루에 마시는 와인 총 양", placeholder="와인 ( )cc", key="p7_28")

    questions["question7_29"] = st.selectbox("[문진7-2] 하루 동안 가장 많이 마셨던 음주량은 어느 정도입니까?(소주)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_29")
    if questions["question7_29"] == "잔":
        questions["question7_30"] = st.text_input("[문진7-2] 하루에 마시는 소주 총 양", placeholder="와인 ( )잔", key="p7_30")
    elif questions["question7_29"] == "병":
        questions["question7_31"] = st.text_input("[문진7-2] 하루에 마시는 소주 총 양", placeholder="와인 ( )병", key="p7_31")
    elif questions["question7_29"] == "캔":
        questions["question7_32"] = st.text_input("[문진7-2] 하루에 마시는 소주 총 양", placeholder="와인 ( )캔", key="p7_32")
    elif questions["question7_29"] == "cc":
        questions["question7_33"] = st.text_input("[문진7-2] 하루에 마시는 소주 총 양", placeholder="와인 ( )cc", key="p7_33")

    questions["question7_34"] = st.selectbox("[문진7-2] 하루 동안 가장 많이 마셨던 음주량은 어느 정도입니까?(맥주)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_34")
    if questions["question7_34"] == "잔":
        questions["question7_35"] = st.text_input("[문진7-2] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )잔", key="p7_35")
    elif questions["question7_34"] == "병":
        questions["question7_36"] = st.text_input("[문진7-2] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )병", key="p7_36")
    elif questions["question7_34"] == "캔":
        questions["question7_37"] = st.text_input("[문진7-2] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )캔", key="p7_37")
    elif questions["question7_34"] == "cc":
        questions["question7_38"] = st.text_input("[문진7-2] 하루에 마시는 맥주 총 양", placeholder="맥주 ( )cc", key="p7_38")

    questions["question7_39"] = st.selectbox("[문진7-2] 하루 동안 가장 많이 마셨던 음주량은 어느 정도입니까?(양주)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_39")
    if questions["question7_39"] == "잔":
        questions["question7_40"] = st.text_input("[문진7-2] 하루에 마시는 양주 총 양", placeholder="양주 ( )잔", key="p7_40")
    elif questions["question7_39"] == "병":
        questions["question7_41"] = st.text_input("[문진7-2] 하루에 마시는 양주 총 양", placeholder="양주 ( )병", key="p7_41")
    elif questions["question7_39"] == "캔":
        questions["question7_42"] = st.text_input("[문진7-2] 하루에 마시는 양주 총 양", placeholder="양주 ( )캔", key="p7_42")
    elif questions["question7_39"] == "cc":
        questions["question7_43"] = st.text_input("[문진7-2] 하루에 마시는 양주 총 양", placeholder="양주 ( )cc", key="p7_43")

    questions["question7_44"] = st.selectbox("[문진7-2] 하루 동안 가장 많이 마셨던 음주량은 어느 정도입니까?(막걸리)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_44")
    if questions["question7_44"] == "잔":
        questions["question7_45"] = st.text_input("[문진7-2] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )잔", key="p7_45")
    elif questions["question7_44"] == "병":
        questions["question7_46"] = st.text_input("[문진7-2] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )병", key="p7_46")
    elif questions["question7_44"] == "캔":
        questions["question7_47"] = st.text_input("[문진7-2] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )캔", key="p7_47")
    elif questions["question7_44"] == "cc":
        questions["question7_48"] = st.text_input("[문진7-2] 하루에 마시는 막걸리 총 양", placeholder="막걸리 ( )cc", key="p7_48")

    questions["question7_49"] = st.selectbox("[문진7-2] 하루 동안 가장 많이 마셨던 음주량은 어느 정도입니까?(와인)", ("잔", "병", "캔", "cc", "X"), help="잔 또는 병 또는 캔 또는 cc 중 한 곳에만 작성해 주십시오(술 종류는 복수응답 가능, 하루에 마신 총 양으로 합산, 기타 술 종류는 비슷한 술 종류에 표기)", key="p7_49")
    if questions["question7_49"] == "잔":
        questions["question7_50"] = st.text_input("[문진7-2] 하루에 마시는 와인 총 양", placeholder="와인 ( )잔", key="p7_50")
    elif questions["question7_49"] == "병":
        questions["question7_51"] = st.text_input("[문진7-2] 하루에 마시는 와인 총 양", placeholder="와인 ( )병", key="p7_51")
    elif questions["question7_49"] == "캔":
        questions["question7_52"] = st.text_input("[문진7-2] 하루에 마시는 와인 총 양", placeholder="와인 ( )캔", key="p7_52")
    elif questions["question7_49"] == "cc":
        questions["question7_53"] = st.text_input("[문진7-2] 하루에 마시는 와인 총 양", placeholder="와인 ( )cc", key="p7_53")


    # 문진 문항별 가중치
    weight_dict = {
        "question1": 1,
        "question2": 0.5,
        "question3": 1.5,
    }

    # 각 선택지에 대한 점수
    score_dict = {
        "있음": 1,
        "없음": 0,
        "예": 1,
        "아니요": 0,
        "모름": 0,
        "월 1~2일": 0.5, 
        "월 3~9일": 1,
        "월 10~29일": 1.5, 
        "매일": 2,
        "일주일에 ( )번": 1.5, 
        "한 달에 ( )번": 1, 
        "1년에 ( )번": 0.5, 
        "술을 마시지 않는다.": 0, 

    }


    # 총 점수를 계산하는 함수 (가중치 적용)
    def calculate_total_score(score_dict, st_results, weight_dict):
        total_score = 0
        for question, answer in st_results.items():
            weight = weight_dict.get(question, 1)  # 문진에 대한 가중치를 가져옴
            
            # answer가 리스트 형태인 경우 (multiselect에서 반환된 경우)
            if isinstance(answer, list):
                for ans in answer:
                    total_score += score_dict.get(ans, 0) * weight  # 가중치를 적용하여 점수를 더함
            else:
                total_score += score_dict.get(answer, 0) * weight  # 가중치를 적용하여 점수를 더함
        return total_score



    # 총 점수 계산
    total_score = calculate_total_score(score_dict, questions, weight_dict)

    # 건강 상태 초기값 설정
    selected_item = None

    # 제출 버튼을 누를 경우
    if st.button("제출"):
        if selected_gender == "남성":
            # 남성일 때의 기준
            if total_score <= 20:
                selected_item = "건강"
            elif 20 < total_score <= 25:
                selected_item = "보통"
            else:
                selected_item = "위험"

        elif selected_gender == "여성":
            # 여성일 때의 기준
            if total_score <= 20:
                selected_item = "건강"
            elif 20 < total_score <= 25:
                selected_item = "보통"
            else:
                selected_item = "위험"
        st.markdown(f"당신의 성별은 {selected_gender}이며, 연령대는 {selected_age}입니다.")
        st.markdown(f"당신의 건강 상태는 '{selected_item}'입니다.")
        st.markdown(f"문진 결과를 기반으로 원하는 정보를 선택하세요")



    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #A7FFEB;
            width: 100%; /
            display: inline-block;
            margin: 0; /
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


    def page1():
        want_to_analysis = st.button("분석 결과")
        if want_to_analysis:
            st.session_state.type_of_case = "Analysis"
            switch_page("분석 결과")


    def page2():
        want_to_Xai_dashboard = st.button("XAI_explainer")
        if want_to_Xai_dashboard:
            st.session_state.type_of_case = "Xai_dashboard"
            switch_page("XAI_explainer")

    def page3():
        want_to_Xai_dashboard2 = st.button("XAI_omni")
        if want_to_Xai_dashboard2:
            st.session_state.type_of_case = "Xai_dashboard2"
            switch_page("XAI_omni")


    col1, col2, col3 = st.columns(3)
    with col1:
        page1()
    with col2:
        page2()
    with col3:
        page3()


