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
import socket


if "page" not in st.session_state:
    st.session_state.page = "Survey"

DATA_PATH = "./"
SEED = 42

# 데이터 불러오는 함수(캐싱)
# @st.cache_data # 캐싱 데코레이터 (ttl=900)
# def load_csv(path):
#     return pd.read_csv(path)


st.markdown(f"""
            <span style='font-size: 24px;'>
            <div style=" color: #000000;">
                <strong>Explainer_dashboard
            </strong>
            </div>
            """, unsafe_allow_html=True)

# 포트가 사용 가능한지 확인하는 함수
def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    return result == 0

# 사용 가능한 포트를 찾는 함수
def find_available_port(start_port, end_port):
    for port in range(start_port, end_port):
        if not check_port(port):
            return port
    return None

# 대시보드를 실행하는 함수
def run_dashboard(port, dashboard):
    if not check_port(port):
        dashboard.run(port=port, host='0.0.0.0')  # 모든 인터페이스에서 접근 가능하게 설정
    else:
        st.error(f"Port {port} is already in use!")

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
    if st.button("XAI 분류 실행"):
        port1 = find_available_port(8055, 8100)
        if port1 is not None:
            X_train, y_train, X_test, y_test = titanic_embarked()
            model = RandomForestClassifier(n_estimators=50, max_depth=10).fit(X_train, y_train)
            explainer = ClassifierExplainer(model, X_test, y_test, cats=['Sex', 'Deck'], descriptions=feature_descriptions, labels=['Queenstown', 'Southampton', 'Cherbourg'])
            dashboard = ExplainerDashboard(explainer, title="XAI Classification Dashboard", bootstrap=dbc.themes.MORPH)
            t = threading.Thread(target=lambda: run_dashboard(port1, dashboard))
            t.start()
            st.components.v1.html(
                f'<iframe src="http://localhost:{port1}" style="width:100%; height:600px;"></iframe>',
                height=600
            )
        else:
            st.error("No available ports found!")

elif selected_xai == "XAI_회귀":
    if st.button("XAI 회귀 실행"):
        port2 = find_available_port(8060, 8100)
        if port2 is not None:
            X_train, y_train, X_test, y_test = titanic_fare()
            model_2 = RandomForestRegressor(n_estimators=50, max_depth=10).fit(X_train, y_train)
            explainer_2 = RegressionExplainer(model_2, X_test, y_test, cats=['Sex', 'Deck', 'Embarked'], descriptions=feature_descriptions, units="$")
            dashboard2 = ExplainerDashboard(explainer_2, title="Simplified Regression Dashboard", bootstrap=dbc.themes.MORPH)
            t = threading.Thread(target=lambda: run_dashboard(port2, dashboard2))
            t.start()
            st.components.v1.html(
                f'<iframe src="http://localhost:{port2}" style="width:100%; height:600px;"></iframe>',
                height=600
            )
        else:
            st.error("No available ports found!")
