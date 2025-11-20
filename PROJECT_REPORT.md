# Bank Management System
## DBMS Project Report

### Team Details
- Team Member 1 [Your Name]
- Team Member 2 [Your Name]
- Team Member 3 [Your Name]
- Team Member 4 [Your Name]

## Abstract
The Bank Management System is a comprehensive web-based application designed to automate and streamline banking operations. The system provides a user-friendly interface for both customers and bank employees to manage various banking activities including account management, transactions, loans, credit cards, and fixed deposits. The application ensures secure authentication, real-time transaction processing, and efficient data management using MySQL database.

## User Requirement Specification

### 1. User Types
- Customers
- Bank Employees
- System Administrators

### 2. Functional Requirements

#### 2.1 Customer Features
- Account Management
  - Create new accounts (Savings/Current/Fixed Deposit)
  - View account details and balance
  - Update personal information
  
- Transaction Management
  - Deposit funds
  - Withdraw funds
  - Transfer money between accounts
  - View transaction history
  
- Loan Management
  - Apply for different types of loans
  - Track loan status
  - View loan details
  
- Credit Card Services
  - Apply for credit cards
  - View credit card details
  - Check credit limit and balance
  
- Fixed Deposits
  - Create new fixed deposits
  - View FD details and maturity dates
  
- Beneficiary Management
  - Add beneficiaries
  - Manage beneficiary details
  
#### 2.2 Employee Features
- Customer Account Management
- Transaction Processing
- Loan Processing
- Credit Card Approval
- Branch Management

#### 2.3 Administrator Features
- User Management
- System Configuration
- Branch Management
- Report Generation

### 3. Non-Functional Requirements
- Security
- Performance
- Scalability
- Reliability
- Data Integrity
- User Interface

## Software and Tools Used

### 1. Development Tools
- **Programming Language:** Python 3.x
- **Database:** MySQL 8.0
- **Frontend Framework:** Streamlit
- **Version Control:** Git

### 2. Libraries and Packages
- streamlit
- mysql-connector-python
- pandas
- datetime

### 3. Development Environment
- Visual Studio Code
- MySQL Workbench
- Git/GitHub

## ER Diagram
[Insert ER Diagram Image Here]

## Relational Schema

```sql
Branches (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100),
    branch_code VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    manager_id INT
)

Employees (
    employee_id INT PRIMARY KEY,
    branch_id INT,
    name VARCHAR(100),
    position VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(200),
    hire_date DATE,
    salary DECIMAL(15,2),
    status VARCHAR(20),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
)

Customers (
    customer_id INT PRIMARY KEY,
    branch_id INT,
    name VARCHAR(100),
    address VARCHAR(200),
    phone VARCHAR(15),
    email VARCHAR(100),
    password VARCHAR(255),
    date_of_birth DATE,
    occupation VARCHAR(100),
    annual_income DECIMAL(15,2),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
)

Accounts (
    account_id INT PRIMARY KEY,
    customer_id INT,
    branch_id INT,
    account_type VARCHAR(20),
    balance DECIMAL(15,2),
    status VARCHAR(20),
    interest_rate DECIMAL(5,2),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id)
)

Transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT,
    type VARCHAR(20),
    amount DECIMAL(15,2),
    description TEXT,
    processed_by_employee INT,
    transaction_date TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id),
    FOREIGN KEY (processed_by_employee) REFERENCES Employees(employee_id)
)

Loans (
    loan_id INT PRIMARY KEY,
    customer_id INT,
    branch_id INT,
    loan_type VARCHAR(50),
    amount DECIMAL(15,2),
    interest_rate DECIMAL(5,2),
    term_months INT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    processed_by INT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES Branches(branch_id),
    FOREIGN KEY (processed_by) REFERENCES Employees(employee_id)
)

CreditCards (
    card_id INT PRIMARY KEY,
    customer_id INT,
    card_number VARCHAR(16),
    card_type VARCHAR(50),
    expiry_date DATE,
    credit_limit DECIMAL(15,2),
    current_balance DECIMAL(15,2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
)

FixedDeposits (
    fd_id INT PRIMARY KEY,
    account_id INT,
    amount DECIMAL(15,2),
    interest_rate DECIMAL(5,2),
    term_months INT,
    start_date DATE,
    maturity_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
)

Beneficiaries (
    beneficiary_id INT PRIMARY KEY,
    customer_id INT,
    account_id INT,
    name VARCHAR(100),
    account_number VARCHAR(20),
    bank_name VARCHAR(100),
    ifsc_code VARCHAR(20),
    relationship VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
)
```

## DDL Commands
[Will be continued in Part 2...]