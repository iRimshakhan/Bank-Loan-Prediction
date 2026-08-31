# 🏦 Bank Customer Loan Prediction

An end-to-end Machine Learning web application that predicts whether a bank customer is likely to have a **good or bad loan outcome** based on customer and loan-related information.

The application is built with **Python, Scikit-learn, Streamlit, and MySQL**, and is deployed using **Streamlit Community Cloud** with **Railway MySQL** for persistent prediction storage.

---

##  Live Demo

🔗 **Live Application:**  
https://bank-loan-prediction-deploy.streamlit.app

---

## 📌 Project Overview

Loan approval and risk assessment are important tasks in the banking and financial sector.

This project demonstrates how Machine Learning can be used to analyze customer information and predict the likelihood of a loan being classified as **Good** or **Bad**.

The project goes beyond simply training a Machine Learning model by integrating it into a web application with:

- Interactive user input
- Real-time prediction
- Prediction probability
- Persistent database storage
- Prediction history
- Cloud deployment

---

## Features

### Machine Learning Prediction

The application uses a trained Machine Learning model to generate loan predictions based on user-provided information.

### Prediction Probability

Along with the prediction, the application displays the probability associated with the prediction.

### User Input

Users can enter customer and loan-related information through an interactive Streamlit interface.

<img width="372" height="647" alt="image" src="https://github.com/user-attachments/assets/22747d11-3699-4cbc-827a-465924c7b3ce" />

### MySQL Database Integration

Every prediction submitted through the application is stored in a MySQL database.

The database is hosted on **Railway** for persistent cloud storage.

### Prediction History

The application retrieves previously stored predictions from the MySQL database and displays them in the application.

<img width="954" height="48" alt="image" src="https://github.com/user-attachments/assets/d5db4348-a4d7-4e67-9e8e-f13deee0956d" />
<img width="1320" height="96" alt="image" src="https://github.com/user-attachments/assets/3b6f652a-f15b-45db-ba5d-a59b2d9b9120" />

### ☁️ Cloud Deployment

The application is deployed using **Streamlit Community Cloud** and connected to a Railway-hosted MySQL database.

---

## Tech Stack

| Technology             | Usage                   |
| ---------------------- | ----------------------- |
| Python                 | Application development |
| Streamlit              | Web application         |
| Pandas                 | Data handling           |
| Scikit-learn           | Machine Learning        |
| Logistic Regression    | Prediction model        |
| Joblib                 | Model loading           |
| MySQL                  | Database                |
| Railway                | Cloud database hosting  |
| mysql-connector-python | MySQL integration       |
|GitHub | Version control |

---

## System Architecture

```text
                    USER
                      │
                      ▼
              Streamlit Web App
                      │
                      ▼
             User Input / Features
                      │
                      ▼
             Machine Learning Model
                      │
                      ▼
                  Prediction
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
       Display Result     Save Prediction
                               │
                               ▼
                        Railway MySQL
                               │
                               ▼
                     Prediction History
```

---

## Project Structure

```text
Bank-Loan-Prediction/
│
├── app.py                  # Streamlit application
├── loan_model.pkl          # Trained Machine Learning model
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
---

## Database Integration
The project uses:
```text
Railway MySQL Database
```
Railway provides a persistent cloud database.

This makes it more suitable for a deployed Streamlit application than relying only on a local database.

---

## Database Table

The application stores prediction records inside: predictions

The database stores:

| Column              | Description                                |
| ------------------- | ------------------------------------------ |
| id                  | Unique prediction ID                       |
| age                 | Customer age                               |
| gender              | Customer gender                            |
| applicant_income    | Customer income                            |
| loan_amount         | Requested loan amount                      |
| cibil_score         | Customer credit score                      |
| married             | Marital status                             |
| dependents          | Number of dependents                       |
| education           | Education information                      |
| self_employed       | Employment status                          |
| previous_loan_taken | Previous loan information                  |
| tenure              | Loan tenure                                |
| probability_bad     | Probability of bad customer classification |
| prediction          | Final loan prediction                      |
| created_at          | Prediction timestamp                       |

---

## Database Workflow

```text
User Enters Customer Information
            │
            ▼
Generate ML Prediction
            │
            ▼
Calculate Probability
            │
            ▼
Create Complete Database Record
            │
            ▼
Open Railway MySQL Connection
            │
            ▼
Execute INSERT Query
            │
            ▼
Commit Transaction
            │
            ▼
Close Database Connection
            │
            ▼
Display Success Message
```

---

## Key Learning Outcomes

Through this project, I learned how to:

Build a Machine Learning prediction application.

Integrate a trained Logistic Regression model with Streamlit.

Handle feature compatibility between a model and user input.

Separate complete user data from ML model data.

Prevent feature mismatch errors.

Load trained models using Joblib.

Calculate prediction probabilities.

Apply custom classification thresholds.

Integrate Python applications with MySQL.

Store prediction records in a cloud database.

Use Railway for persistent database storage.

Configure Streamlit Secrets securely.

Build prediction history functionality.

Handle SQL INSERT and SELECT operations.

Debug database schema mismatches.

Use ALTER TABLE to evolve an existing database schema.

Preserve historical data while adding new columns.

Build a growing dataset for future Machine Learning improvements.

---

# 👤 Author

Khan Rimsha Fatima Mohammed Naim

🎓 Master's in Information Technology (Artificial Intelligence)

🤖 Interested in Artificial Intelligence, Generative AI, AI Agents, Machine Learning, Data Science, AI Automation, and Building AI-powered applications

🔗 GitHub: https://github.com/iRimshakhan

💼 LinkedIn: https://linkedin.com/in/rimshafatimakhan

---

## Support
If you found this project interesting, consider giving the repository a ⭐ on GitHub!
