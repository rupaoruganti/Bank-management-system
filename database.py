import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        try:
            # First connect without database to create it if it doesn't exist
            self.connection = mysql.connector.connect(
                host=input("Enter MySQL host (default: localhost): ") or 'localhost',
                user=input("Enter MySQL username (default: root): ") or 'root',
                password=input("Enter MySQL password: ")
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                database_name = input("Enter database name (default: bank_management): ") or 'bank_management'
                
                # Create database if it doesn't exist
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                self.cursor.execute(f"USE {database_name}")
                print(f"Using database: {database_name}")
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connected to MySQL database")
                self.create_tables()  # Create tables when connection is established
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def create_procedures_and_triggers(self):
        try:
            # Read and execute procedures
            with open('database_procedures.sql', 'r') as file:
                procedures = file.read()
                for procedure in procedures.split('DELIMITER ;'):
                    if procedure.strip():
                        self.cursor.execute(procedure + 'DELIMITER ;')

            # Read and execute triggers
            with open('database_triggers.sql', 'r') as file:
                triggers = file.read()
                for trigger in triggers.split('DELIMITER ;'):
                    if trigger.strip():
                        self.cursor.execute(trigger + 'DELIMITER ;')

            # Also read and execute user creation SQL if present
            try:
                with open('database_users.sql', 'r') as uf:
                    users_sql = uf.read()
                    # split by semicolon to execute individual statements safely
                    for stmt in [s.strip() for s in users_sql.split(';') if s.strip()]:
                        self.cursor.execute(stmt)
            except FileNotFoundError:
                # Not critical; proceed if file not present
                pass

            # Optionally execute complex queries file if intended to create views or stored queries
            try:
                with open('complex_queries.sql', 'r') as cq:
                    cq_sql = cq.read()
                    # If the file contains SELECTs for analysis, do not execute them here.
                    # We execute statements that create views or stored queries only (CREATE VIEW/PROCEDURE/etc.)
                    for stmt in [s.strip() for s in cq_sql.split(';') if s.strip()]:
                        upper = stmt.strip().upper()
                        if upper.startswith('CREATE') or upper.startswith('INSERT') or upper.startswith('CREATE VIEW') or upper.startswith('CREATE PROCEDURE'):
                            try:
                                self.cursor.execute(stmt)
                            except Exception:
                                # ignore individual failures to avoid blocking setup
                                pass
            except FileNotFoundError:
                pass

            self.connection.commit()
            print("Procedures and triggers created successfully")
        except Exception as e:
            print(f"Error creating procedures and triggers: {e}")

    def create_tables(self):
        try:
            # Create branches table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS branches (
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
                )
            ''')

            # Create employees table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
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
                )
            ''')

            # Create customers table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
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
                )
            ''')

            # Create accounts table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
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
                )
            ''')

            # Create transactions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    account_id INT,
                    type VARCHAR(20) NOT NULL,
                    amount DECIMAL(15, 2) NOT NULL,
                    description TEXT,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed_by_employee INT,
                    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
                    FOREIGN KEY (processed_by_employee) REFERENCES employees(employee_id)
                )
            ''')

            # Create loans table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS loans (
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
                )
            ''')

            # Create credit_cards table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS credit_cards (
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
                )
            ''')

            # Create fixed_deposits table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS fixed_deposits (
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
                )
            ''')

            # Create beneficiaries table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS beneficiaries (
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
                )
            ''')

            # Create atm_transactions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS atm_transactions (
                    atm_transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    card_id INT,
                    transaction_type VARCHAR(20) NOT NULL,
                    amount DECIMAL(15, 2) NOT NULL,
                    atm_location VARCHAR(200),
                    status VARCHAR(20) DEFAULT 'completed',
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (card_id) REFERENCES credit_cards(card_id)
                )
            ''')

            # Create notifications table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id INT,
                    title VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )
            ''')

            self.connection.commit()
            print("Tables created successfully")
            
            # Create procedures and triggers
            self.create_procedures_and_triggers()
        except Error as e:
            print(f"Error creating tables: {e}")

    def close_connection(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")