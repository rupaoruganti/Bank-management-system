-- Stored Procedures

-- 1. Transfer Money Procedure
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

-- 2. Calculate Loan EMI Function
DELIMITER //
CREATE FUNCTION CalculateLoanEMI(
    loan_amount DECIMAL(15, 2),
    interest_rate DECIMAL(5, 2),
    term_months INT
) 
RETURNS DECIMAL(15, 2)
DETERMINISTIC
BEGIN
    DECLARE monthly_rate DECIMAL(10, 6);
    DECLARE emi DECIMAL(15, 2);
    
    SET monthly_rate = interest_rate / (12 * 100);
    SET emi = loan_amount * monthly_rate * POW(1 + monthly_rate, term_months) 
              / (POW(1 + monthly_rate, term_months) - 1);
    
    RETURN emi;
END //
DELIMITER ;

-- 3. Create Account with Initial Deposit Procedure
DELIMITER //
CREATE PROCEDURE CreateAccountWithDeposit(
    IN p_customer_id INT,
    IN p_account_type VARCHAR(20),
    IN p_initial_deposit DECIMAL(15, 2),
    IN p_branch_id INT,
    OUT p_account_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_account_id = -1;
    END;
    
    START TRANSACTION;
    
    -- Create the account
    INSERT INTO accounts (customer_id, account_type, balance, branch_id, status)
    VALUES (p_customer_id, p_account_type, p_initial_deposit, p_branch_id, 'active');
    
    SET p_account_id = LAST_INSERT_ID();
    
    -- Record the initial deposit transaction
    IF p_initial_deposit > 0 THEN
        INSERT INTO transactions (account_id, type, amount, description)
        VALUES (p_account_id, 'deposit', p_initial_deposit, 'Initial deposit');
    END IF;
    
    COMMIT;
END //
DELIMITER ;

-- 4. Get Account Balance Function
DELIMITER //
CREATE FUNCTION GetAccountBalance(p_account_id INT) 
RETURNS DECIMAL(15, 2)
READS SQL DATA
BEGIN
    DECLARE v_balance DECIMAL(15, 2);
    
    SELECT balance INTO v_balance
    FROM accounts
    WHERE account_id = p_account_id;
    
    RETURN COALESCE(v_balance, 0.00);
END //
DELIMITER ;

-- 5. Process Loan Application Procedure
DELIMITER //
CREATE PROCEDURE ProcessLoanApplication(
    IN p_loan_id INT,
    IN p_processed_by INT,
    IN p_status VARCHAR(20),
    IN p_remarks TEXT
)
BEGIN
    DECLARE v_customer_id INT;
    
    -- Update loan status
    UPDATE loans 
    SET status = p_status,
        processed_by = p_processed_by
    WHERE loan_id = p_loan_id;
    
    -- Get customer_id for notification
    SELECT customer_id INTO v_customer_id
    FROM loans
    WHERE loan_id = p_loan_id;
    
    -- Create notification
    INSERT INTO notifications (customer_id, title, message, type)
    VALUES (
        v_customer_id,
        CONCAT('Loan Application ', p_status),
        CONCAT('Your loan application (ID: ', p_loan_id, ') has been ', LOWER(p_status), '. ', p_remarks),
        'loan_update'
    );
END //
DELIMITER ;