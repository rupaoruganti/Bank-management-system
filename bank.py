from database import DatabaseConnection
import hashlib
import datetime
import secrets

# Card limits by tier (application-level enforcement)
# Values are currency amounts. Adjust as needed.
CARD_LIMITS = {
    'Silver': (0.00, 50000.00),
    'Gold': (50000.01, 200000.00),
    'Platinum': (200000.01, 1000000.00)
}

class BankManagement:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.create_tables()

    def create_customer(self, name, address, phone, email, password):
        try:
            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            query = '''INSERT INTO customers (name, address, phone, email, password) 
                      VALUES (%s, %s, %s, %s, %s)'''
            values = (name, address, phone, email, hashed_password)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating customer: {e}")
            return False

    def create_account(self, customer_id, account_type, initial_balance=0):
        try:
            query = '''INSERT INTO accounts (customer_id, account_type, balance) 
                      VALUES (%s, %s, %s)'''
            values = (customer_id, account_type, initial_balance)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error creating account: {e}")
            return False

    def deposit(self, account_id, amount):
        try:
            # Update account balance
            update_query = '''UPDATE accounts 
                            SET balance = balance + %s 
                            WHERE account_id = %s'''
            self.db.cursor.execute(update_query, (amount, account_id))

            # Record transaction
            transaction_query = '''INSERT INTO transactions 
                                 (account_id, type, amount, description) 
                                 VALUES (%s, %s, %s, %s)'''
            self.db.cursor.execute(transaction_query, 
                                 (account_id, 'deposit', amount, 'Deposit transaction'))

            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error processing deposit: {e}")
            return False

    def withdraw(self, account_id, amount):
        try:
            # Check balance
            self.db.cursor.execute('''SELECT balance FROM accounts 
                                    WHERE account_id = %s''', (account_id,))
            current_balance = self.db.cursor.fetchone()[0]

            if current_balance >= amount:
                # Update account balance
                update_query = '''UPDATE accounts 
                                SET balance = balance - %s 
                                WHERE account_id = %s'''
                self.db.cursor.execute(update_query, (amount, account_id))

                # Record transaction
                transaction_query = '''INSERT INTO transactions 
                                     (account_id, type, amount, description) 
                                     VALUES (%s, %s, %s, %s)'''
                self.db.cursor.execute(transaction_query, 
                                     (account_id, 'withdrawal', amount, 'Withdrawal transaction'))

                self.db.connection.commit()
                return True
            else:
                print("Insufficient balance")
                return False
        except Exception as e:
            print(f"Error processing withdrawal: {e}")
            return False

    def check_balance(self, account_id):
        try:
            self.db.cursor.execute('''SELECT balance FROM accounts 
                                    WHERE account_id = %s''', (account_id,))
            return self.db.cursor.fetchone()[0]
        except Exception as e:
            print(f"Error checking balance: {e}")
            return None

    def get_transaction_history(self, account_id):
        try:
            query = '''SELECT * FROM transactions 
                      WHERE account_id = %s 
                      ORDER BY transaction_date DESC'''
            self.db.cursor.execute(query, (account_id,))
            return self.db.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving transaction history: {e}")
            return []

    def close_connection(self):
        self.db.close_connection()

    def issue_credit_card(self, customer_id, card_type, requested_limit, expiry_date=None):
        """Issue a new credit card for a customer with application-level tier checks.

        Raises ValueError on invalid tier or if requested_limit is outside allowed range.
        Returns True on success, False on DB error.
        """
        # Validate card tier
        if card_type not in CARD_LIMITS:
            raise ValueError(f"Invalid card tier: {card_type}. Valid tiers: {', '.join(CARD_LIMITS.keys())}")

        min_lim, max_lim = CARD_LIMITS[card_type]
        if not (min_lim <= requested_limit <= max_lim):
            raise ValueError(
                f"Requested limit {requested_limit} not allowed for tier {card_type} (allowed: {min_lim} - {max_lim})"
            )

        # Generate a simple random 16-digit card number (string)
        card_number = ''.join(str(secrets.randbelow(10)) for _ in range(16))

        # Default expiry: 4 years from today if not provided
        if expiry_date is None:
            expiry_date = (datetime.date.today() + datetime.timedelta(days=365 * 4)).isoformat()

        try:
            insert_query = '''INSERT INTO credit_cards
                              (customer_id, card_number, card_type, expiry_date, credit_limit, current_balance, status)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            values = (customer_id, card_number, card_type, expiry_date, requested_limit, 0.0, 'active')

            self.db.cursor.execute(insert_query, values)
            self.db.connection.commit()
            return True
        except Exception as e:
            print(f"Error issuing credit card: {e}")
            return False