import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page


if "page" not in st.session_state:
    st.session_state.page = "Survey"

DATA_PATH = "./"
SEED = 42

# 데이터 불러오는 함수(캐싱)
@st.cache_data # 캐싱 데코레이터 (ttl=900)
def load_csv(path):
    return pd.read_csv(path)

# data = load_csv(f"{DATA_PATH}암사망자수.csv")

# st.dataframe(data)

st.markdown(f"""
            <span style='font-size: 20px;'>
            <div style=" color: #000000;">
                <strong>XAI_omni
            </strong>
            </div>
            """, unsafe_allow_html=True)

# st.markdown(f"""
#             <span style='font-size: 14px;'>
#             <div style=" color: #000000;">
#             <strong>
#             explainerdashboard는 머신러닝 모델의 해석을 돕는 Python 라이브러리입니다. <br>
#             이 라이브러리는 대시보드 형태로 모델의 예측을 해석하고 시각화할 수 있는 도구를 제공합니다. 주로 SHAP(SHapley Additive exPlanations) 값과 같은 여러 유형의 모델 해석 방법을 지원합니다. <br>
#             <핵심 기능> <br>
#             예측 설명: 모델이 특정 예측을 하는 데 있어 어떤 특성이 중요한지, 그리고 그 특성들이 예측에 어떤 영향을 미치는지 해석할 수 있습니다. <br>
#             특성 중요도: 전체 데이터셋에 대해 각 특성의 중요도를 평가하고 시각화합니다. <br>
#             모델 성능: 분류 문제의 경우 ROC 곡선, 정밀도-재현율 곡선 등을 통해 모델의 성능을 평가합니다. <br>
#             커스터마이징: 대시보드는 사용자의 요구에 맞게 커스터마이징이 가능합니다. <br>
#             통합성: explainerdashboard는 Flask, Django, Streamlit 등 다양한 웹 프레임워크와 통합이 가능합니다. <br>
#             다양한 모델 지원: RandomForest, XGBoost, LightGBM, CatBoost, scikit-learn 등 다양한 모델을 지원합니다. <br>
#             </strong>
#             </div>
#             """, unsafe_allow_html=True)



st.components.v1.html(
    """
    <iframe src="https://omnixai-24e10803fd23.herokuapp.com/" style="width:100%; height:600px;"></iframe>
    """,
    height=600,
)




