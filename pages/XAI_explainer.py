import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import numpy as np
import random
import os
import datetime as dt
from streamlit_extras.switch_page_button import switch_page


from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from explainerdashboard import ClassifierExplainer, ExplainerDashboard, RegressionExplainer
from explainerdashboard.datasets import titanic_embarked, titanic_fare, feature_descriptions
import dash_bootstrap_components as dbc
import threading
import graphviz





if "page" not in st.session_state:
    st.session_state.page = "Survey"

DATA_PATH = "./"
SEED = 42

# 데이터 불러오는 함수(캐싱)
@st.cache_data # 캐싱 데코레이터 (ttl=900)
def load_csv(path):
    return pd.read_csv(path)


st.markdown(f"""
            <span style='font-size: 24px;'>
            <div style=" color: #000000;">
                <strong>Explainer_dashboard
            </strong>
            </div>
            """, unsafe_allow_html=True)


selected_xai = st.selectbox(
    label = "원하는 XAI_분석을 선택하세요.",
    options=["XAI_분류", "XAI_회귀"],
    placeholder="하나를 선택하세요.",
    help="선택한 XAI에 따라 다른 분석 결과를 제공합니다.",
    key="xai_key",)


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




if selected_xai == "XAI_분류":
    if st.button("XAI 분류 실행"):  # 버튼 생성

        # 함수로 대시보드를 실행
        def run_dashboard(port):
            dashboard.run(port=port)


        # 분류 대시보드
        X_train, y_train, X_test, y_test = titanic_embarked()
        model = RandomForestClassifier(n_estimators=50, max_depth=10).fit(X_train, y_train)

        explainer = ClassifierExplainer(model, X_test, y_test, 
                                        cats=['Sex', 'Deck'], 
                                        descriptions=feature_descriptions,
                                        labels=['Queenstown', 'Southampton', 'Cherbourg'])


        # 대시보드 생성
        dashboard = ExplainerDashboard(explainer, title="XAI Classification Dashboard", bootstrap=dbc.themes.MORPH)

        # 스레드를 사용하여 대시보드 실행
        t = threading.Thread(target=lambda: run_dashboard(8055))
        t.start()

        st.components.v1.html(
            """
            <iframe src="http://localhost:8055" style="width:100%; height:600px;"></iframe>
            """,
            height=600,
        )


elif selected_xai == "XAI_회귀":
    if st.button("XAI 회귀 실행"):

        # 회귀 대시보드
        X_train, y_train, X_test, y_test = titanic_fare()
        model_2 = RandomForestRegressor(n_estimators=50, max_depth=10).fit(X_train, y_train)

        explainer_2 = RegressionExplainer(model_2, X_test, y_test, 
                                        cats=['Sex', 'Deck', 'Embarked'], 
                                        descriptions=feature_descriptions,
                                        units="$")

        # 대시보드 생성
        dashboard2 = ExplainerDashboard(explainer_2, title="Simplified Regression Dashboard",  bootstrap=dbc.themes.MORPH)

        # 함수로 대시보드를 실행
        def run_dashboard2(port):
            dashboard2.run(port=port)

        # 스레드를 사용하여 대시보드 실행
        t = threading.Thread(target=lambda: run_dashboard2(8060))
        t.start()

        st.components.v1.html(
            """
            <iframe src="http://localhost:8060" style="width:100%; height:600px;"></iframe>
            """,
            height=600,
        )

