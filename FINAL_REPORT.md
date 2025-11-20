# Final Project Report — Bank Management System

> NOTE: This report contains the required sections and placeholders only. As requested, it does NOT include code snippets, SQL dumps, or screenshots — please add those artifacts into the indicated sections later.

## 1. Title and Team Details (Cover Page)
Project Title: Bank Management System

Team:
- Team Name: ______________________
- Member 1: Name, Roll/ID, Email
- Member 2: Name, Roll/ID, Email
- Member 3: Name, Roll/ID, Email
- Supervisor/Instructor: ______________________

Date: ______________________


## 2. Description (Short Abstract)
This project implements a simplified Bank Management System that demonstrates core database design, SQL programming, and a lightweight web GUI for bank operations. The system models branches, customers, employees, accounts, transactions, loans, credit cards, fixed deposits, beneficiaries, and notifications. It includes DDL scripts, stored procedures for atomic operations (e.g., fund transfers), triggers to enforce business rules (e.g., balance checks), and sample complex SQL queries (nested, joins, aggregates) to support reporting and analytics.


## 3. User Requirement Specification (Prepared for Review-1)
(See `USER_REQUIREMENT_SPEC.md` for the full, detailed specification. Below is a concise summary to include in the report.)

Purpose: Automate retail banking workflows for customers and staff, safely manage transactions, and demonstrate database features for an academic project.

Scope: Includes schema design, DDL, procedures, triggers, complex queries, and a Streamlit GUI implementing registration, account management, transactions, loans, credit cards, fixed deposits, beneficiaries, and notifications.

Major functional requirements (high-level):
- User registration and authentication
- Account creation and overview
- Deposit, withdrawal, and transfer (atomic via stored procedure)
- Transaction history view
- Loan application and processing
- Credit card application and tier enforcement
- Fixed deposit creation and view
- Beneficiary management
- Notifications
- Administrative facilities for users/privileges


## 4. Software / Tools / Programming Languages Used
- Language: Python 3.x
- Web UI: Streamlit
- Database: MySQL (compatible with mysql-connector-python)
- Python libraries: mysql-connector-python, pandas, streamlit
- Development environment: Any (project prepared for Windows development and execution)


## 5. ER Diagram
Placeholder for ER diagram image. Insert the ER diagram graphic (PNG/SVG) here when ready.

Suggested filename/path to add: `screenshots/ER_DIAGRAM.png` or `ER_DIAGRAM.mmd` (Mermaid source).


## 6. Relational Schema
The core relational schema (table list and key attributes) is:
- branches(branch_id PK, branch_name, branch_code, address, city, state, phone, email, manager_id, created_at)
- employees(employee_id PK, branch_id FK, name, position, email, phone, address, hire_date, salary, status, created_at)
- customers(customer_id PK, branch_id FK, name, address, phone, email, password, date_of_birth, occupation, annual_income, created_at)
- accounts(account_id PK, customer_id FK, branch_id FK, account_type, balance, status, interest_rate, created_at)
- transactions(transaction_id PK, account_id FK, type, amount, description, transaction_date, processed_by_employee FK)
- loans(loan_id PK, customer_id FK, branch_id FK, loan_type, amount, interest_rate, term_months, start_date, end_date, status, processed_by FK, created_at)
- credit_cards(card_id PK, customer_id FK, card_number, card_type, expiry_date, credit_limit, current_balance, status, created_at)
- fixed_deposits(fd_id PK, account_id FK, amount, interest_rate, term_months, start_date, maturity_date, status, created_at)
- beneficiaries(beneficiary_id PK, customer_id FK, account_id FK, name, account_number, bank_name, ifsc_code, relationship, created_at)
- notifications(notification_id PK, customer_id FK, title, message, type, is_read, created_at)


## 8. CRUD Operation Screenshots




## 9. List of Functionalities / Features and Associated Front-End Screenshots
Provide a numbered list of implemented features with a short description and the corresponding screenshot reference. Example entries (fill with screenshots later):
1. Registration and Login — `screenshots/login_page.png`
2. Account Creation — `screenshots/create_account.png`
3. Account Overview — `screenshots/account_overview.png`
4. Transactions (Deposit/Withdrawal) — `screenshots/transaction_form.png`
5. Transaction History — `screenshots/transaction_history.png`
6. Loan Application — `screenshots/loan_application.png`
7. Credit Card Application — `screenshots/credit_card_application.png`
8. Fixed Deposit Management — `screenshots/fixed_deposit.png`
9. Beneficiary Management — `screenshots/beneficiaries.png`
10. Notifications Panel — `screenshots/notifications.png`


## 10. Triggers, Procedures/Functions, Nested Query, Join, Aggregate Queries
All SQL artifacts are supplied as separate .sql files in the repository. Do not include full SQL here (per request); instead, reference the files below and add brief descriptions.

Files and brief descriptions:
- `database_triggers.sql` — Contains triggers for:
  - Updating account balances after transactions
  - Validating withdrawals before insertion
  - Creating notifications on loan status change
  - Preventing deletion of accounts with non-zero balance or recent transactions
  - Enforcing credit card tier limits during insert/update
- `database_procedures.sql` — Contains stored procedures and functions including:
  - `TransferMoney` (atomic transfer with transaction handling)
  - `CalculateLoanEMI` (EMI calculator function)
  - `CreateAccountWithDeposit` (account creation + initial deposit transaction)
  - `GetAccountBalance` (get balance function)
  - `ProcessLoanApplication` (status update and notification)
- `complex_queries.sql` — Contains example queries for:
  - Nested queries (e.g., customers with above-average deposits)
  - Join queries (transactions joined with accounts, customers, branches)
  - Aggregate queries (branch-level summaries: totals, averages, counts)
- `database_users.sql` — Contains SQL to create DB users and grant privileges (admin, employee, customer roles)


## 11. Code Snippets for Invoking Procedures/Functions/Triggers
As requested, code snippets are omitted from this report. Add the invocation snippets in this section later (examples include: CALL TransferMoney(...), SELECT CalculateLoanEMI(...), and sample Python callproc use). If you want, use `CODE_SNIPPETS.md` in the repository as a ready template to copy from.

Reference: `CODE_SNIPPETS.md` (present in repo) — copy entries into this section when ready.


## 12. SQL Files (Create, Insert, Triggers, Procedures/Functions, Nested, Join, Aggregate)
All SQL files for the project are in the repository. Add their contents to the appendix or attach the .sql files directly with the submission. The repository includes (but is not limited to):

- `ddl_commands.sql` — CREATE TABLE statements
- `database_users.sql` — CREATE USER and GRANT statements
- `database_procedures.sql` — Procedures and functions
- `database_triggers.sql` — Triggers
- `complex_queries.sql` — Sample nested/join/aggregate queries


---

### Appendix: Repository Map (where to find artifacts)
- Python app / GUI: `app.py` (Streamlit)
- Business logic helpers: `bank.py`
- Database connection and schema creation: `database.py` (calls `create_tables()` and loads SQL files)
- SQL files: `database_procedures.sql`, `database_triggers.sql`, `database_users.sql`, `complex_queries.sql`, `ddl_commands.sql`
- Report files: `USER_REQUIREMENT_SPEC.md`, `DELIVERABLES.md`, `FINAL_REPORT.md` (this file)
- Code invocation examples: `CODE_SNIPPETS.md`
- Placeholder folder for images/screenshots: `screenshots/`


If you'd like, I can also produce a ready-to-download single markdown or PDF combining these sections (without code or screenshots) so you can insert final artifacts and submit. Would you like that?