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

if 'selected_survey' not in st.session_state:
    st.session_state.selected_survey = st.warning("문진표를 먼저 작성해주세요!")

DATA_PATH = "./"
SEED = 42

# 랜덤 시드 설정
np.random.seed(SEED)

# 데이터 불러오는 함수(캐싱)
@st.cache_data # 캐싱 데코레이터
def load_csv(path):
    return pd.read_csv(path)



from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

# 가상의 암 검진 데이터를 생성하는 함수
def generate_cancer_data(n=500):
    np.random.seed(0)
    data = {
        'age': np.random.randint(20, 80, n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'tumor_size': np.random.randint(1, 100, n),
        'cancer_stage': np.random.choice([1, 2, 3, 4], n),
        'cancer_type': np.random.choice(['Breast', 'Lung', 'Prostate'], n),
    }
    return pd.DataFrame(data)

# 가상의 건강검진 데이터를 생성하는 함수
def generate_health_data(n=500):
    np.random.seed(0)
    data = {
        'age': np.random.randint(20, 80, n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'blood_pressure': np.random.randint(80, 180, n),
        'cholesterol': np.random.randint(150, 300, n),
        'weight': np.random.randint(50, 100, n),
        'height': np.random.randint(150, 200, n),
        'smoker': np.random.choice([True, False], n),
    }
    return pd.DataFrame(data)


if st.session_state.selected_survey == "암검진 문진표":
    st.title("Cancer Screening Data Analysis")

    # Generate data and show on sidebar
    n = st.sidebar.slider("Select Number of Data Points", 100, 500, 200)
    df = generate_cancer_data(n)
    st.sidebar.write("### Preview of Data")
    st.sidebar.write(df.head())

    # ANOVA Analysis
    st.subheader("ANOVA Analysis: Tumor Size by Cancer Type")
    groups = df.groupby('cancer_type').apply(lambda x: x['tumor_size'].tolist())
    f_value, p_value = stats.f_oneway(*groups)
    st.write(f"F-value: {f_value}, P-value: {p_value}")

    # Machine Learning
    st.subheader("Machine Learning: Predicting Cancer Stage")
    df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})
    df['cancer_type'] = df['cancer_type'].map({'Breast': 0, 'Lung': 1, 'Prostate': 2})
    X = df[['age', 'gender', 'tumor_size', 'cancer_type']]
    y = df['cancer_stage']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=50)
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    st.write(f"Classification accuracy: {accuracy}")

    # Data Visualization
    st.subheader("Data Visualization")

    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Boxplot for tumor size by cancer type
    sns.boxplot(x='cancer_type', y='tumor_size', data=df, ax=ax[0])
    ax[0].set_title("Boxplot of Tumor Size by Cancer Type")

    # Distribution of cancer stages
    sns.histplot(df['cancer_stage'], kde=False, ax=ax[1])
    ax[1].set_title("Distribution of Cancer Stages")

    st.pyplot(fig)


if st.session_state.selected_survey == "일반건강검진 문진표":
    st.title("Health Screening Data Analysis")

    # Generate data and show on sidebar
    n = st.sidebar.slider("Select Number of Data Points", 100, 500, 200)
    df = generate_health_data(n)
    st.sidebar.write("### Preview of Data")
    st.sidebar.write(df.head())

    # ANOVA Analysis
    st.subheader("ANOVA Analysis: Blood Pressure by Gender")
    groups = df.groupby('gender').apply(lambda x: x['blood_pressure'].tolist())
    f_value, p_value = stats.f_oneway(*groups)
    st.write(f"F-value: {f_value}, P-value: {p_value}")

    # Machine Learning
    st.subheader("Machine Learning: Predicting Smoking Habit")
    df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})
    X = df[['age', 'gender', 'blood_pressure', 'cholesterol', 'weight', 'height']]
    y = df['smoker']
    clf = RandomForestClassifier(n_estimators=50)
    clf.fit(X, y)
    st.write(f"Feature Importances: {clf.feature_importances_}")

    # Data Visualization
    st.subheader("Data Visualization")

    fig, ax = plt.subplots(2, 2, figsize=(15, 12))

    # Blood Pressure by Gender
    sns.boxplot(x='gender', y='blood_pressure', data=df, ax=ax[0, 0])
    ax[0, 0].set_title("Blood Pressure by Gender")

    # Cholesterol levels
    sns.histplot(df['cholesterol'], kde=True, ax=ax[0, 1])
    ax[0, 1].set_title("Distribution of Cholesterol Levels")

    # Scatter plot between weight and height
    sns.scatterplot(x='weight', y='height', hue='smoker', data=df, ax=ax[1, 0])
    ax[1, 0].set_title("Scatter Plot of Weight vs Height")

    # Blood Pressure by Age
    sns.lineplot(x='age', y='blood_pressure', data=df, ax=ax[1, 1])
    ax[1, 1].set_title("Blood Pressure by Age")

    st.pyplot(fig)

