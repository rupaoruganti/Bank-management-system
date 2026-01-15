# 🏦 Bank Management System

A **Bank Management System** developed as a **project** to demonstrate **database design**, **SQL programming**, and a **Streamlit-based web interface** for core banking operations.

---

## 📌 Overview

The system models essential banking entities such as **branches, customers, employees, accounts, transactions, loans, credit cards, fixed deposits, beneficiaries, and notifications**. It focuses on ensuring **data integrity**, **atomic transactions**, and **business rule enforcement** using database-level features.

---


## ⚙️ Key Features

* User registration and authentication
* Account creation and overview
* Deposit, withdrawal, and fund transfer
* Transaction history
* Loan and credit card applications
* Fixed deposit management
* Beneficiary management
* Notifications
* Basic administrative controls

---

## 📁 Project Structure

```
BANK-MANAGEMENT-SYSTEM/
├── main.py                  # Entry point
├── app.py                   # Streamlit app
├── bank.py                  # Business logic
├── database.py              # DB connection utilities
├── ddl_commands.sql         # Database schema
├── database_procedures.sql  # Stored procedures
├── database_triggers.sql    # Triggers
```

---

## 🛠️ Technologies Used

* **Language:** Python 3.x
* **Web UI:** Streamlit
* **Database:** MySQL
* **Libraries:** mysql-connector-python, pandas, streamlit

---

## ▶️ How to Run

### 1️⃣ Backend (FastAPI)

Make sure MySQL is running and the database schema is already created.

Install backend dependencies:
```bash
pip install fastapi "uvicorn[standard]" mysql-connector-python pandas
```

Start the backend API server:
```bash
uvicorn api:app --reload
```


### 2️⃣ Frontend (Streamlit)

Install frontend dependencies
```bash
pip install mysql-connector-python pandas streamlit
```

Run the Streamlit application
```bash
streamlit run app.py
```
The web interface will open automatically in your browser.
---
