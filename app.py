import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Bank Loan Prediction",
    page_icon="🏦",
    layout="centered"
)


# --------------------------------------------------
# Load Trained Model
# --------------------------------------------------

@st.cache_resource
def load_model():
    return joblib.load("loan_model.pkl")


model = load_model()


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🏦 Bank Customer Loan Prediction")

st.write(
    "Enter the customer's information below to predict "
    "whether the loan should be approved or rejected."
)

st.divider()


# --------------------------------------------------
# Customer Inputs
# --------------------------------------------------

st.subheader("Customer Information")


applicant_income = st.number_input(
    "Applicant Income",
    min_value=0,
    value=50000,
    step=1000
)


cibil_score = st.number_input(
    "CIBIL Score",
    min_value=0,
    max_value=900,
    value=700,
    step=1
)


married = st.selectbox(
    "Married",
    options=["No", "Yes"]
)


self_employed = st.selectbox(
    "Self Employed",
    options=["No", "Yes"]
)


previous_loan = st.selectbox(
    "Previous Loan Taken",
    options=["No", "Yes"]
)


# Convert Yes/No to the same 0/1 representation
# used in the notebook.

married_value = 1 if married == "Yes" else 0
self_employed_value = 1 if self_employed == "Yes" else 0
previous_loan_value = 1 if previous_loan == "Yes" else 0


# --------------------------------------------------
# Create Input DataFrame
# --------------------------------------------------

input_data = pd.DataFrame({
    "ApplicantIncome": [applicant_income],
    "Cibil_Score": [cibil_score],
    "Married": [married_value],
    "Self_Employed": [self_employed_value],
    "Previous_Loan_Taken": [previous_loan_value]
})


# --------------------------------------------------
# Display Input Data
# --------------------------------------------------

with st.expander("View Input Data"):
    st.dataframe(input_data, use_container_width=True)


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button(
    "🔍 Predict Loan Status",
    use_container_width=True
):

    # Probability of class 1 = Probability_Bad
    probability_bad = model.predict_proba(input_data)[0][1]

    # Same threshold used in the notebook
    threshold = 0.7

    if probability_bad >= threshold:

        prediction = 1

        st.error(
            "❌ Loan Rejected"
        )

        st.write(
            f"Probability of Bad Customer: "
            f"**{probability_bad:.2%}**"
        )

        st.warning(
            "The probability of the customer being classified "
            "as bad is 70% or higher."
        )

    else:

        prediction = 0

        st.success(
            "✅ Loan Approved"
        )

        st.write(
            f"Probability of Bad Customer: "
            f"**{probability_bad:.2%}**"
        )

        st.info(
            "The probability of the customer being classified "
            "as bad is below 70%."
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Bank Customer Loan Prediction | "
    "Logistic Regression"
)
