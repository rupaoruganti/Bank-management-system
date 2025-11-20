-- Triggers for Bank Management System

-- 1. After Transaction Trigger - Update Account Balance
DELIMITER //
CREATE TRIGGER after_transaction_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF NEW.type = 'deposit' THEN
        UPDATE accounts 
        SET balance = balance + NEW.amount 
        WHERE account_id = NEW.account_id;
    ELSEIF NEW.type = 'withdrawal' THEN
        UPDATE accounts 
        SET balance = balance - NEW.amount 
        WHERE account_id = NEW.account_id;
    END IF;
END //
DELIMITER ;

-- 2. Before Transaction Trigger - Validate Balance
DELIMITER //
CREATE TRIGGER before_transaction_insert
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
    DECLARE current_balance DECIMAL(15, 2);
    
    IF NEW.type = 'withdrawal' THEN
        SELECT balance INTO current_balance
        FROM accounts
        WHERE account_id = NEW.account_id;
        
        IF current_balance < NEW.amount THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Insufficient balance for withdrawal';
        END IF;
    END IF;
END //
DELIMITER ;

-- 3. After Loan Status Change Trigger - Create Notification
DELIMITER //
CREATE TRIGGER after_loan_status_update
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

-- 6. Before Credit Card Insert - Enforce Tier Limits
DELIMITER //
CREATE TRIGGER before_credit_card_insert
BEFORE INSERT ON credit_cards
FOR EACH ROW
BEGIN
    CASE NEW.card_type
        WHEN 'Silver' THEN
            IF NEW.credit_limit < 0.00 OR NEW.credit_limit > 50000.00 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Credit limit outside allowed range for Silver cards (0 - 50000)';
            END IF;
        WHEN 'Gold' THEN
            IF NEW.credit_limit < 50000.01 OR NEW.credit_limit > 200000.00 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Credit limit outside allowed range for Gold cards (50000.01 - 200000)';
            END IF;
        WHEN 'Platinum' THEN
            IF NEW.credit_limit < 200000.01 OR NEW.credit_limit > 1000000.00 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Credit limit outside allowed range for Platinum cards (200000.01 - 1000000)';
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Unknown card type';
    END CASE;
END //
DELIMITER ;

-- 7. Before Credit Card Update - Enforce Tier Limits on updates
DELIMITER //
CREATE TRIGGER before_credit_card_update
BEFORE UPDATE ON credit_cards
FOR EACH ROW
BEGIN
    CASE NEW.card_type
        WHEN 'Silver' THEN
            IF NEW.credit_limit < 0.00 OR NEW.credit_limit > 50000.00 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Credit limit outside allowed range for Silver cards (0 - 50000)';
            END IF;
        WHEN 'Gold' THEN
            IF NEW.credit_limit < 50000.01 OR NEW.credit_limit > 200000.00 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Credit limit outside allowed range for Gold cards (50000.01 - 200000)';
            END IF;
        WHEN 'Platinum' THEN
            IF NEW.credit_limit < 200000.01 OR NEW.credit_limit > 1000000.00 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Credit limit outside allowed range for Platinum cards (200000.01 - 1000000)';
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Unknown card type';
    END CASE;
END //
DELIMITER ;