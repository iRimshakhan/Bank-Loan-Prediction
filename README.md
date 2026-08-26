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

### MySQL Database Integration

Every prediction submitted through the application is stored in a MySQL database.

The database is hosted on **Railway** for persistent cloud storage.

### Prediction History

The application retrieves previously stored predictions from the MySQL database and displays them in the application.

<img width="381" height="479" alt="image" src="https://github.com/user-attachments/assets/e5759dd8-b38c-4abe-b839-abf16701ecf3" />

### ☁️ Cloud Deployment

The application is deployed using **Streamlit Community Cloud** and connected to a Railway-hosted MySQL database.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming language |
| Pandas | Data processing |
| Scikit-learn | Machine Learning |
| Streamlit | Web application |
| MySQL | Database |
| Railway | Cloud MySQL hosting |
| Streamlit Community Cloud | Application deployment |
| GitHub | Version control |

---

## 🏗️ System Architecture

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

## 📂 Project Structure

```text
Bank-Loan-Prediction/
│
├── app.py                  # Streamlit application
├── loan_model.pkl          # Trained Machine Learning model
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

