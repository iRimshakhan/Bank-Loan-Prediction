import streamlit as st
import pandas as pd
import joblib
import mysql.connector

#Database connection function
def get_database_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )


#Function that saves predictions
def save_prediction(
    applicant_income,
    cibil_score,
    married,
    self_employed,
    previous_loan_taken,
    probability_bad,
    prediction
):

    connection = get_database_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO predictions (
            applicant_income,
            cibil_score,
            married,
            self_employed,
            previous_loan_taken,
            probability_bad,
            prediction
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        applicant_income,
        cibil_score,
        married,
        self_employed,
        previous_loan_taken,
        probability_bad,
        prediction
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

#Function for prediction history
def get_prediction_history():

    connection = get_database_connection()

    query = """
        SELECT
            id,
            applicant_income,
            cibil_score,
            married,
            self_employed,
            previous_loan_taken,
            probability_bad,
            prediction,
            created_at
        FROM predictions
        ORDER BY created_at DESC
    """

    history = pd.read_sql(query, connection)

    connection.close()

    return history


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

        prediction = "Loan Rejected"

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

        prediction = "Loan Approved"

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
    save_prediction(
        applicant_income,
        cibil_score,
        married_value,
        self_employed_value,
        previous_loan_value,
        probability_bad,
        prediction
    )
    st.success("Prediction saved successfully! 💾")



#Prediction History
st.divider()

st.subheader("📋 Prediction History")

history = get_prediction_history()

if history.empty:

    st.info("No prediction history available.")

else:

    history = history.rename(columns={
        "id": "ID",
        "applicant_income": "Applicant Income",
        "cibil_score": "CIBIL Score",
        "married": "Married",
        "self_employed": "Self Employed",
        "previous_loan_taken": "Previous Loan",
        "probability_bad": "Bad Customer Probability",
        "prediction": "Prediction",
        "created_at": "Date & Time"
    })

    history["Married"] = history["Married"].map({
        0: "No",
        1: "Yes"
    })

    history["Self Employed"] = history["Self Employed"].map({
        0: "No",
        1: "Yes"
    })

    history["Previous Loan"] = history["Previous Loan"].map({
        0: "No",
        1: "Yes"
    })

    history["Bad Customer Probability"] = (
        history["Bad Customer Probability"] * 100
    ).round(2).astype(str) + "%"

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Bank Customer Loan Prediction | "
    "Logistic Regression"
)
