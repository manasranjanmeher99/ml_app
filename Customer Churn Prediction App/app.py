import streamlit as st
import pickle
import pandas as pd

# Load model and scaler
model = pickle.load(open("churn_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Churn Prediction App")

st.write(
    "Predict whether a customer is likely to leave the company."
)

# Sidebar
st.sidebar.header("Customer Information")

credit_score = st.sidebar.slider(
    "Credit Score", 300, 900, 650
)

age = st.sidebar.slider(
    "Age", 18, 100, 35
)

tenure = st.sidebar.slider(
    "Tenure", 0, 10, 5
)

balance = st.sidebar.number_input(
    "Balance", value=50000.0
)

products = st.sidebar.slider(
    "Number of Products", 1, 4, 1
)

credit_card = st.sidebar.selectbox(
    "Has Credit Card",
    [0, 1]
)

active_member = st.sidebar.selectbox(
    "Is Active Member",
    [0, 1]
)

salary = st.sidebar.number_input(
    "Estimated Salary",
    value=50000.0
)

# Dataframe
data = pd.DataFrame({
    'CreditScore':[credit_score],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[products],
    'HasCrCard':[credit_card],
    'IsActiveMember':[active_member],
    'EstimatedSalary':[salary]
})

if st.button("Predict Churn"):

    scaled_data = scaler.transform(data)

    prediction = model.predict(scaled_data)

    probability = model.predict_proba(
        scaled_data
    )[0][1]

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error(
            f"⚠️ Customer likely to churn "
            f"({probability:.2%} probability)"
        )
    else:
        st.success(
            f"✅ Customer likely to stay "
            f"({1-probability:.2%} confidence)"
        )

    st.metric(
        "Churn Probability",
        f"{probability:.2%}"
    )

    # Risk Level
    if probability < 0.3:
        st.success("🟢 Low Risk")
    elif probability < 0.7:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")