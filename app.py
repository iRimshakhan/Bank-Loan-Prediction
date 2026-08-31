import streamlit as st
import pandas as pd
import joblib
import mysql.connector


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_database_connection():
    """
    Creates and returns a connection to the MySQL database.

    Database credentials are loaded securely from:
    .streamlit/secrets.toml
    """

    connection = mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

    return connection



# ==================================================
# SAVE PREDICTION
# ==================================================

def save_prediction(
    age,
    gender,
    applicant_income,
    loan_amount,
    cibil_score,
    married,
    dependents,
    education,
    self_employed,
    previous_loan_taken,
    tenure,
    probability_bad,
    prediction
):
    """
    Saves all 11 user-entered fields along with
    prediction probability and prediction result.
    """

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        cursor = connection.cursor()

        query = """
            INSERT INTO predictions (
                age,
                gender,
                applicant_income,
                loan_amount,
                cibil_score,
                married,
                dependents,
                education,
                self_employed,
                previous_loan_taken,
                tenure,
                probability_bad,
                prediction
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s
            )
        """

        values = (
            age,
            gender,
            applicant_income,
            loan_amount,
            cibil_score,
            married,
            dependents,
            education,
            self_employed,
            previous_loan_taken,
            tenure,
            probability_bad,
            prediction
        )

        cursor.execute(query, values)

        # Save changes permanently
        connection.commit()


    except mysql.connector.Error as error:

        return False, f"MySQL INSERT error: {error}"


    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


# ==================================================
# GET PREDICTION HISTORY
# ==================================================

def get_prediction_history():
    """
    Retrieves all prediction records from MySQL.
    """

    connection = None

    try:

        connection = get_database_connection()

        query = """
            SELECT
                id,
                age,
                gender,
                applicant_income,
                loan_amount,
                cibil_score,
                married,
                dependents,
                education,
                self_employed,
                previous_loan_taken,
                tenure,
                probability_bad,
                prediction,
                created_at
            FROM predictions
            ORDER BY created_at DESC
        """

        history = pd.read_sql(
            query,
            connection
        )

        return history


    except mysql.connector.Error as error:

        return None, f"MySQL SELECT error: {error}"

    finally:

        if connection is not None and connection.is_connected():
            connection.close()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Bank Loan Prediction",
    page_icon="🏦",
    layout="centered"
)


# ==================================================
# LOAD TRAINED MODEL
# ==================================================

@st.cache_resource
def load_model():

    return joblib.load(
        "loan_model.pkl"
    )


model = load_model()


# ==================================================
# APPLICATION TITLE
# ==================================================

st.title("🏦 Bank Customer Loan Prediction")

st.write(
    "Enter the customer's information below to predict "
    "whether the loan should be approved or rejected."
)

st.info(
    "📊 All customer information is securely stored as "
    "historical data for future analysis and model improvement."
)

st.divider()


# ==================================================
# PERSONAL INFORMATION
# ==================================================

st.subheader("👤 Personal Information")


col1, col2 = st.columns(2)


with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1
    )


with col2:

    gender = st.selectbox(
        "Gender",
        options=[
            "Female",
            "Male"
        ]
    )


col1, col2 = st.columns(2)


with col1:

    married = st.selectbox(
        "Married",
        options=[
            "No",
            "Yes"
        ]
    )


with col2:

    dependents = st.number_input(
        "Dependents",
        min_value=0,
        value=0,
        step=1
    )


education = st.selectbox(
    "Education",
    options=[
        "Graduate",
        "Not Graduate"
    ]
)


# ==================================================
# EMPLOYMENT INFORMATION
# ==================================================

st.divider()

st.subheader("💼 Employment Information")


self_employed = st.selectbox(
    "Self Employed",
    options=[
        "No",
        "Yes"
    ]
)


# ==================================================
# FINANCIAL INFORMATION
# ==================================================

st.divider()

st.subheader("💰 Financial Information")


col1, col2 = st.columns(2)


with col1:

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )


with col2:

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=100000.0,
        step=1000.0
    )


cibil_score = st.number_input(
    "CIBIL Score",
    min_value=0,
    max_value=900,
    value=700,
    step=1
)


# ==================================================
# LOAN INFORMATION
# ==================================================

st.divider()

st.subheader("🏦 Loan Information")


col1, col2 = st.columns(2)


with col1:

    previous_loan_taken = st.selectbox(
        "Previous Loan Taken",
        options=[
            "No",
            "Yes"
        ]
    )


with col2:

    tenure = st.number_input(
        "Tenure",
        min_value=0,
        value=12,
        step=1
    )


# ==================================================
# COMPLETE USER RECORD
# ==================================================

complete_user_record = pd.DataFrame({

    "Age": [age],

    "Gender": [gender],

    "ApplicantIncome": [applicant_income],

    "LoanAmount": [loan_amount],

    "Cibil_Score": [cibil_score],

    "Married": [married],

    "Dependents": [dependents],

    "Education": [education],

    "Self_Employed": [self_employed],

    "Previous_Loan_Taken": [
        previous_loan_taken
    ],

    "Tenure": [tenure]

})


# ==================================================
# PREPARE ML INPUT
# ==================================================

# Convert Yes / No values to the same
# 0 / 1 format used during model training.

married_value = (
    1 if married == "Yes" else 0
)


self_employed_value = (
    1 if self_employed == "Yes" else 0
)


previous_loan_value = (
    1 if previous_loan_taken == "Yes" else 0
)


# IMPORTANT:
# This DataFrame is used internally.
# Only these 5 features are sent to the model.

ml_input_data = pd.DataFrame({

    "ApplicantIncome": [
        applicant_income
    ],

    "Cibil_Score": [
        cibil_score
    ],

    "Married": [
        married_value
    ],

    "Self_Employed": [
        self_employed_value
    ],

    "Previous_Loan_Taken": [
        previous_loan_value
    ]

})


# ==================================================
# DISPLAY COMPLETE CUSTOMER DATA
# ==================================================

with st.expander(
    "📋 View Complete Customer Data"
):

    st.dataframe(
        complete_user_record,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# PREDICTION
# ==================================================

st.divider()


if st.button(
    "🔍 Predict Loan Status",
    use_container_width=True
):

    try:

        # ------------------------------------------
        # MODEL PREDICTION
        # ------------------------------------------

        probability_bad = (
            model.predict_proba(
                ml_input_data
            )[0][1]
        )


        threshold = 0.7


        # ------------------------------------------
        # PREDICTION RESULT
        # ------------------------------------------

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
                "The probability of the customer being "
                "classified as bad is 70% or higher."
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
                "The probability of the customer being "
                "classified as bad is below 70%."
            )


        # ------------------------------------------
        # SAVE COMPLETE RECORD TO MYSQL
        # ------------------------------------------

        save_prediction(

            age=age,

            gender=gender,

            applicant_income=applicant_income,

            loan_amount=loan_amount,

            cibil_score=cibil_score,

            married=married_value,

            dependents=dependents,

            education=education,

            self_employed=self_employed_value,

            previous_loan_taken=previous_loan_value,

            tenure=tenure,

            probability_bad=probability_bad,

            prediction=prediction
        )


        st.success(
            "💾 Complete customer record saved successfully!"
        )


    except Exception as error:

        st.error(
            f"Error: {error}"
        )


# ==================================================
# PREDICTION HISTORY
# ==================================================

st.divider()

st.subheader("📋 Prediction History")


try:

    history = get_prediction_history()


    if history.empty:

        st.info(
            "No prediction history available."
        )


    else:

        # Rename columns only AFTER
        # the SQL query succeeds.

        history = history.rename(
            columns={

                "id": "ID",

                "age": "Age",

                "gender": "Gender",

                "applicant_income":
                    "Applicant Income",

                "loan_amount":
                    "Loan Amount",

                "cibil_score":
                    "CIBIL Score",

                "married":
                    "Married",

                "dependents":
                    "Dependents",

                "education":
                    "Education",

                "self_employed":
                    "Self Employed",

                "previous_loan_taken":
                    "Previous Loan",

                "tenure":
                    "Tenure",

                "probability_bad":
                    "Bad Customer Probability",

                "prediction":
                    "Prediction",

                "created_at":
                    "Date & Time"
            }
        )


        # Convert 0 / 1 values back
        # into user-friendly text.

        history["Married"] = (
            history["Married"].map({
                0: "No",
                1: "Yes"
            })
        )


        history["Self Employed"] = (
            history["Self Employed"].map({
                0: "No",
                1: "Yes"
            })
        )


        history["Previous Loan"] = (
            history["Previous Loan"].map({
                0: "No",
                1: "Yes"
            })
        )


        # Format probability as percentage.

        history["Bad Customer Probability"] = (

            history["Bad Customer Probability"]
            * 100

        ).round(2).astype(str) + "%"


        st.dataframe(

            history,

            use_container_width=True,

            hide_index=True

        )


except Exception as error:

    st.error(
        f"Prediction history is currently unavailable: "
        f"{error}"
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Bank Customer Loan Prediction | "
    "Logistic Regression | Historical Data Collection"
)
