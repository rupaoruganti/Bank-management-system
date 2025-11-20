# Code Snippets: invoking Procedures / Functions / Triggers

This file contains runnable SQL examples you can use when connected to the `bank_management` database. Run these in your MySQL client (mysql CLI, MySQL Workbench, or any GUI).

1) Call the TransferMoney stored procedure

-- Example: transfer 100 from account 1 to account 2
CALL TransferMoney(1, 2, 100.00, @status);
SELECT @status;


2) Use CalculateLoanEMI function

-- Example: calculate EMI for a loan of 100000, 8.5% annual, 12 months
SELECT CalculateLoanEMI(100000.00, 8.5, 12) AS monthly_emi;


3) Process a loan application (procedure)

-- Example:
CALL ProcessLoanApplication(1, 2, 'approved', 'Verified documents');


4) Trigger behavior (no direct CALL)

-- Triggers run automatically on DML. To test `after_transaction_insert`:
INSERT INTO transactions (account_id, type, amount, description) VALUES (1, 'deposit', 500.00, 'Test deposit');
-- This will update the related account balance via the `after_transaction_insert` trigger.


5) Creating users via SQL file

-- If you want to (re)create DB users, run the `database_users.sql` file in the MySQL client:
SOURCE database_users.sql;


Notes:
- Some procedures use `DELIMITER //` blocks; when running in the mysql CLI you can paste the .sql file directly, or load it with `SOURCE` so delimiter blocks are respected.
- When using Python code to call stored procedures via `mysql-connector-python`, use `cursor.callproc('TransferMoney', [from_id, to_id, amount, status_out])` and then fetch the OUT parameter as described in your connector docs.
