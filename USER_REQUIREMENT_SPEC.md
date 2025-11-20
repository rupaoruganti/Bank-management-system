# User Requirement Specification

## Project: Bank Management System

### Purpose
This Bank Management System automates core retail-banking operations for customers and internal staff. The application allows customers to register, create bank accounts, perform transactions (deposits, withdrawals, transfers), apply for loans and credit cards, create fixed deposits, manage beneficiaries, and view notifications. For staff/administrators, it supports loan processing, employee and branch management, and enforcement of business rules through database triggers and stored procedures.

The solution is intended for an educational project (coursework) and demonstrates database design principles (ER design and relational schema), SQL programming (DDL, DML, triggers, stored procedures/functions), and a simple Streamlit GUI for user-facing operations.

### Scope
This deliverable covers: requirements definition, database schema and creation scripts, stored procedures and triggers, complex SQL queries (nested, joins, aggregates), a lightweight Streamlit front-end implementing the primary workflows (customer registration, account management, transactions, loans, credit card applications, fixed deposits, beneficiaries), and documentation for building and testing the system. It does not provide production-level security (password hashing is minimal or illustrative), nor advanced banking compliance features (real KYC, two-factor authentication, encryption of credentials) unless explicitly added later.

The scope includes the artifacts listed in the project rubric: ER diagram, relational schema, DDL scripts, CRUD screenshots, GUI flows, triggers/procedures, complex queries, and a GitHub repo link.

### Detailed Description 
A mid-sized retail bank operates multiple branches. Each branch has employees (managers, tellers) and services a set of customers. Customers may hold multiple accounts (Savings, Checking, Fixed Deposits) at a branch. Each account can have many transactions (deposits, withdrawals, transfers). Customers may apply for loans and credit cards; loans are processed by bank staff and have a status lifecycle (pending → approved/denied). Credit cards carry credit limits and balances. Beneficiaries can be added by customers for transfers. Notifications inform customers of changes (e.g., loan status updates, credit card activation). The database enforces referential integrity, business rules via triggers, and transactional consistency via stored procedures (for money transfers and loan processing).

Core entities (for ER diagram):
- Branches
- Employees
- Customers
- Accounts
- Transactions
- Loans
- Credit_Cards
- Fixed_Deposits
- Beneficiaries
- Notifications

Key relationships and rules:
- A Branch may have many Employees and many Accounts.
- A Customer belongs to a Branch and can have many Accounts, Loans, Credit Cards, and Beneficiaries.
- An Account belongs to a Customer and a Branch; Transactions reference Accounts.
- Loans reference Customer and Branch; loans have status and processed_by (employee).
- Credit card issuance is governed by tier limits; triggers enforce business rules.
- Stored procedures handle multi-step operations (e.g., TransferMoney) to ensure atomicity.

### Functional Requirements
Each "System Functionality" below includes a one-line description.

1. User Registration and Authentication
   - Allow new customers to register and existing customers to log in to the GUI.

2. Account Creation
   - Customers can create new bank accounts with initial deposits.

3. Account Overview (Read)
   - Customers can view a list of their accounts, balances, and status.

4. Transactions (Deposit/Withdrawal/Transfer)
   - Customers can make deposits and withdrawals; transfers should be performed atomically via a stored procedure.

5. Transaction History
   - Customers can view chronological transaction history for a selected account.

6. Loan Application
   - Customers can apply for loans (provide type, amount, term); staff can process and update loan status.

7. Credit Card Application
   - Customers can apply for credit cards; card-tier limits are enforced by application logic and database triggers.

8. Fixed Deposit Management
   - Customers can create fixed deposits and view maturity amounts/periods.

9. Beneficiary Management
   - Customers can add/remove beneficiaries to support future fund transfers.

10. Notifications
    - System creates notifications (e.g., loan status change, card activation) and customers can mark notifications as read.

11. Administrative Tasks (DB/Staff)
    - Admin can create database users, manage privileges, and staff can process loans.

12. Data Integrity and Business Rules
    - Triggers validate balances (prevent over-withdrawal), update balances after transactions, and enforce card tier limits.

13. Reporting / Queries
    - Provide aggregate reports (branch transaction summaries), joins (transaction with customer/branch), and nested queries (above-average balances per account type).

### Non-functional requirements
- Usability: simple Streamlit UI for common workflows.
- Correctness: ACID semantics for money movement, referential integrity in DB.
- Maintainability: SQL scripts and procedures stored as `.sql` files; code in `app.py`, `bank.py`, `database.py`.
- Portability: designed for MySQL; connection parameters configurable.

### Acceptance Criteria
- Database schema created with provided DDL scripts and tables populated for basic test data.
- Stored procedures and triggers execute and enforce rules (transfer funds atomically; prevent invalid deletions).
- Streamlit GUI allows registration, login, account creation, transaction execution, loan application, credit card application, and related read operations.
- Complex queries (nested/join/aggregate) return expected results on sample data.
