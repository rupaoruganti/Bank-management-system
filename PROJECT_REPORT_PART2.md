## DDL Commands

```sql
-- Create Branches Table
CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_code VARCHAR(20) UNIQUE NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE,
    manager_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Employees Table
CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_id INT,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(200),
    hire_date DATE NOT NULL,
    salary DECIMAL(15, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

-- Create Customers Table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_id INT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    phone VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    occupation VARCHAR(100),
    annual_income DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

-- Create Accounts Table
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    branch_id INT,
    account_type VARCHAR(20) NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'active',
    interest_rate DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
);

-- Create Transactions Table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_by_employee INT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (processed_by_employee) REFERENCES employees(employee_id)
);

-- Create Loans Table
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    branch_id INT,
    loan_type VARCHAR(50) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    term_months INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    processed_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
    FOREIGN KEY (processed_by) REFERENCES employees(employee_id)
);

-- Create Credit Cards Table
CREATE TABLE credit_cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    card_number VARCHAR(16) UNIQUE NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    expiry_date DATE NOT NULL,
    credit_limit DECIMAL(15, 2) NOT NULL,
    current_balance DECIMAL(15, 2) DEFAULT 0.00,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create Fixed Deposits Table
CREATE TABLE fixed_deposits (
    fd_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    amount DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    term_months INT NOT NULL,
    start_date DATE NOT NULL,
    maturity_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Create Beneficiaries Table
CREATE TABLE beneficiaries (
    beneficiary_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    account_id INT,
    name VARCHAR(100) NOT NULL,
    account_number VARCHAR(20) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    ifsc_code VARCHAR(20) NOT NULL,
    relationship VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

-- Create Notifications Table
CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

## Stored Procedures

```sql
-- Procedure to transfer money between accounts
DELIMITER //
CREATE PROCEDURE TransferMoney(
    IN from_account_id INT,
    IN to_account_id INT,
    IN amount DECIMAL(15, 2),
    OUT status VARCHAR(50)
)
BEGIN
    DECLARE from_balance DECIMAL(15, 2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET status = 'Error occurred';
    END;
    
    START TRANSACTION;
    
    -- Check if sufficient balance
    SELECT balance INTO from_balance 
    FROM accounts 
    WHERE account_id = from_account_id;
    
    IF from_balance >= amount THEN
        -- Deduct from source account
        UPDATE accounts 
        SET balance = balance - amount 
        WHERE account_id = from_account_id;
        
        -- Add to destination account
        UPDATE accounts 
        SET balance = balance + amount 
        WHERE account_id = to_account_id;
        
        -- Record transactions
        INSERT INTO transactions (account_id, type, amount, description)
        VALUES (from_account_id, 'transfer_out', amount, 
                CONCAT('Transfer to account ', to_account_id));
                
        INSERT INTO transactions (account_id, type, amount, description)
        VALUES (to_account_id, 'transfer_in', amount, 
                CONCAT('Transfer from account ', from_account_id));
        
        COMMIT;
        SET status = 'Success';
    ELSE
        ROLLBACK;
        SET status = 'Insufficient balance';
    END IF;
END //
DELIMITER ;

-- Procedure to calculate loan EMI
DELIMITER //
CREATE PROCEDURE CalculateLoanEMI(
    IN loan_amount DECIMAL(15, 2),
    IN interest_rate DECIMAL(5, 2),
    IN term_months INT,
    OUT monthly_emi DECIMAL(15, 2)
)
BEGIN
    DECLARE monthly_rate DECIMAL(10, 6);
    SET monthly_rate = interest_rate / (12 * 100);
    SET monthly_emi = loan_amount * monthly_rate * POW(1 + monthly_rate, term_months) 
                     / (POW(1 + monthly_rate, term_months) - 1);
END //
DELIMITER ;
```

## Triggers

```sql
-- Trigger to update credit card balance after transaction
DELIMITER //
CREATE TRIGGER after_credit_card_transaction
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF NEW.type = 'credit_card_payment' THEN
        UPDATE credit_cards
        SET current_balance = current_balance + NEW.amount
        WHERE card_id = (SELECT card_id FROM credit_card_transactions 
                        WHERE transaction_id = NEW.transaction_id);
    END IF;
END //
DELIMITER ;

-- Trigger to create notification after loan approval
DELIMITER //
CREATE TRIGGER after_loan_status_change
AFTER UPDATE ON loans
FOR EACH ROW
BEGIN
    IF NEW.status != OLD.status THEN
        INSERT INTO notifications (customer_id, title, message, type)
        VALUES (
            NEW.customer_id,
            CONCAT('Loan Status Updated: ', NEW.status),
            CONCAT('Your loan application (ID: ', NEW.loan_id, ') status has been updated to ', NEW.status),
            'loan_update'
        );
    END IF;
END //
DELIMITER ;
```

## Complex Queries

```sql
-- Nested Query: Find customers with high-value accounts
SELECT c.name, c.email, a.account_type, a.balance
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
WHERE a.balance > (
    SELECT AVG(balance) * 2
    FROM accounts
    WHERE account_type = a.account_type
);

-- Join Query: Get detailed transaction report
SELECT 
    t.transaction_id,
    c.name AS customer_name,
    a.account_id,
    t.type,
    t.amount,
    b.branch_name,
    e.name AS processed_by
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN branches b ON a.branch_id = b.branch_id
LEFT JOIN employees e ON t.processed_by_employee = e.employee_id
WHERE t.transaction_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY);

-- Aggregate Query: Branch-wise transaction summary
SELECT 
    b.branch_name,
    COUNT(t.transaction_id) as total_transactions,
    SUM(CASE WHEN t.type = 'deposit' THEN t.amount ELSE 0 END) as total_deposits,
    SUM(CASE WHEN t.type = 'withdrawal' THEN t.amount ELSE 0 END) as total_withdrawals,
    AVG(t.amount) as avg_transaction_amount
FROM branches b
JOIN accounts a ON b.branch_id = a.branch_id
JOIN transactions t ON a.account_id = t.account_id
GROUP BY b.branch_id
HAVING total_transactions > 100;
```

## Screenshots

[Add screenshots of your application here showing different features and operations]

1. Login Screen
2. Account Creation
3. Transaction Processing
4. Loan Application
5. Credit Card Management
6. Fixed Deposit Creation
7. Beneficiary Management
8. Transaction History
9. Account Overview
10. Notifications

## Application Features

1. User Authentication and Authorization
   - Secure login/logout
   - Password encryption
   - Session management

2. Account Management
   - Multiple account types
   - Real-time balance updates
   - Account status tracking

3. Transaction Processing
   - Deposits and withdrawals
   - Fund transfers
   - Transaction history

4. Loan Management
   - Multiple loan types
   - Automated EMI calculation
   - Loan status tracking

5. Credit Card Services
   - Card application
   - Credit limit management
   - Transaction tracking

6. Fixed Deposits
   - FD creation with various terms
   - Interest calculation
   - Maturity tracking

7. Beneficiary Management
   - Add/remove beneficiaries
   - Secure beneficiary validation
   - Quick transfer to beneficiaries

8. Notification System
   - Transaction alerts
   - Loan status updates
   - Account activity notifications

## Future Enhancements

1. Mobile Banking Interface
2. Integration with Payment Gateways
3. Advanced Security Features
4. Automated Report Generation
5. Multi-language Support

## Conclusion

The Bank Management System successfully implements a comprehensive banking solution with robust database management, secure transactions, and user-friendly interface. The system demonstrates effective use of MySQL features including stored procedures, triggers, and complex queries to maintain data integrity and provide efficient banking services.