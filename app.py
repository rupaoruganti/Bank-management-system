import streamlit as st
import mysql.connector
from database import DatabaseConnection
from bank import CARD_LIMITS
import pandas as pd
from datetime import datetime, date, timedelta


# ---------------------------------------------------------
# Initialize Database Connection
# ---------------------------------------------------------
@st.cache_resource
def init_connection():
    db = DatabaseConnection()
    ensure_default_branch(db)
    return db


def ensure_default_branch(db):
    """Ensure at least one branch exists."""
    try:
        db.cursor.execute("SELECT COUNT(*) FROM branches")
        count = db.cursor.fetchone()[0]

        if count == 0:
            db.cursor.execute("""
                INSERT INTO branches (branch_name, location, city, contact_number, email)
                VALUES (%s, %s, %s, %s, %s)
            """, ("Main Branch", "123 Main St", "City", "1234567890", "main.branch@bank.com"))
            db.connection.commit()
    except Exception as e:
        st.error(f"Error creating default branch: {e}")


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)


# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'account_id' not in st.session_state:
    st.session_state.account_id = None


# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------
db = init_connection()


# ---------------------------------------------------------
# User Authentication
# ---------------------------------------------------------
def login_user():
    st.title("🏦 Bank Management System")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            try:
                db.cursor.execute("SELECT customer_id, password FROM customers WHERE email = %s", (email,))
                result = db.cursor.fetchone()

                if result and result[1] == password:  # In production: use hashed passwords!
                    st.session_state.authenticated = True
                    st.session_state.user_id = result[0]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            except Exception as e:
                st.error(f"Error during login: {e}")


def register_user():
    st.title("Register New Account")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Register")

        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return

            try:
                db.cursor.execute("""
                    INSERT INTO customers (name, email, phone, address, password)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, email, phone, address, password))
                db.connection.commit()
                st.success("Registration successful! Please login.")
            except mysql.connector.Error as e:
                if e.errno == 1062:
                    st.error("Email already registered!")
                else:
                    st.error(f"Error during registration: {e}")


# ---------------------------------------------------------
# Account Management
# ---------------------------------------------------------
def create_account():
    st.subheader("Create New Bank Account")

    with st.form("create_account_form"):
        account_type = st.selectbox("Account Type", ["Savings", "Checking", "Fixed Deposit"])
        initial_deposit = st.number_input("Initial Deposit Amount", min_value=0.0, value=0.0)
        submitted = st.form_submit_button("Create Account")

        if submitted:
            try:
                db.cursor.execute("""
                    INSERT INTO accounts (customer_id, account_type, balance)
                    VALUES (%s, %s, %s)
                """, (st.session_state.user_id, account_type, initial_deposit))

                account_id = db.cursor.lastrowid

                if initial_deposit > 0:
                    db.cursor.execute("""
                        INSERT INTO transactions (account_id, type, amount, description)
                        VALUES (%s, %s, %s, %s)
                    """, (account_id, "deposit", initial_deposit, "Initial deposit"))

                db.connection.commit()
                st.success("Account created successfully!")
            except Exception as e:
                st.error(f"Error creating account: {e}")


def view_accounts():
    st.subheader("Your Accounts")

    db.cursor.execute("""
        SELECT account_id, account_type, balance, status, created_at
        FROM accounts
        WHERE customer_id = %s
    """, (st.session_state.user_id,))

    accounts = db.cursor.fetchall()

    if accounts:
        df = pd.DataFrame(accounts, columns=["Account ID", "Account Type", "Balance", "Status", "Created At"])
        st.dataframe(df)
        # Filter only Savings accounts for transaction selection
        savings_accounts = [
            (acc[0], f"Account {acc[0]} - Balance: ${acc[2]:,.2f}")
            for acc in accounts if acc[1] == 'Savings'
        ]

        if savings_accounts:
            account_options = {desc: id for id, desc in savings_accounts}
            selected_desc = st.selectbox(
                "Select Savings Account for Transactions",
                list(account_options.keys())
            )
            st.session_state.account_id = account_options[selected_desc]
        else:
            st.warning("No Savings accounts available for transactions. Please create a Savings account first.")
            st.session_state.account_id = None
    else:
        st.info("You don't have any accounts yet. Create one!")


# ---------------------------------------------------------
# Transactions
# ---------------------------------------------------------
def make_transaction():
    if not st.session_state.account_id:
        st.warning("Please select a Savings account first!")
        return
        
    # Verify that selected account is a Savings account
    db.cursor.execute("""
        SELECT account_type 
        FROM accounts 
        WHERE account_id = %s AND customer_id = %s
    """, (st.session_state.account_id, st.session_state.user_id))
    
    account = db.cursor.fetchone()
    if not account or account[0] != 'Savings':
        st.error("Transactions can only be performed with Savings accounts.")
        return

    st.subheader("Make Transaction")

    with st.form("transaction_form"):
        transaction_type = st.selectbox("Transaction Type", ["deposit", "withdrawal"])
        amount = st.number_input("Amount", min_value=0.01)
        description = st.text_input("Description")
        submitted = st.form_submit_button("Submit Transaction")

        if submitted:
            try:
                from decimal import Decimal
                amount_decimal = Decimal(str(amount))

                db.cursor.execute("SELECT balance FROM accounts WHERE account_id = %s",
                                (st.session_state.account_id,))
                current_balance = db.cursor.fetchone()[0]

                if transaction_type == "withdrawal" and amount_decimal > current_balance:
                    st.error("Insufficient funds!")
                    return

                new_balance = current_balance + amount_decimal if transaction_type == "deposit" else current_balance - amount_decimal

                db.cursor.execute("""
                    UPDATE accounts SET balance = %s WHERE account_id = %s
                """, (new_balance, st.session_state.account_id))

                db.cursor.execute("""
                    INSERT INTO transactions (account_id, type, amount, description)
                    VALUES (%s, %s, %s, %s)
                """, (st.session_state.account_id, transaction_type, amount, description))

                db.connection.commit()
                st.success(f"Transaction successful! New balance: ${new_balance:,.2f}")

            except Exception as e:
                st.error(f"Error processing transaction: {e}")


def view_transactions():
    st.subheader("Transaction History")
    
    if not st.session_state.account_id:
        st.warning("Please select an account first!")
        return

    db.cursor.execute("""
        SELECT transaction_id, type, amount, description, transaction_date
        FROM transactions
        WHERE account_id = %s
        ORDER BY transaction_date DESC
    """, (st.session_state.account_id,))

    transactions = db.cursor.fetchall()

    if transactions:
        df = pd.DataFrame(transactions, columns=["Transaction ID", "Type", "Amount", "Description", "Date"])
        st.dataframe(df)
    else:
        st.info("No transactions found for this account.")


# ---------------------------------------------------------
# Loans Management
# ---------------------------------------------------------
def apply_loan():
    st.subheader("Apply for a Loan")
    
    with st.form("loan_application"):
        loan_type = st.selectbox("Loan Type", ["Personal", "Home", "Vehicle", "Education", "Business"])
        amount = st.number_input("Loan Amount", min_value=1000.0, step=1000.0)
        term_months = st.number_input("Loan Term (months)", min_value=6, max_value=360, step=6)
        purpose = st.text_area("Loan Purpose")
        
        # Get branches for selection
        db.cursor.execute("SELECT branch_id, branch_name, city FROM branches")
        branches = db.cursor.fetchall()
        branch_options = {f"{b[1]} ({b[2]})": b[0] for b in branches}
        selected_branch = st.selectbox("Select Branch", list(branch_options.keys()))
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            try:
                branch_id = branch_options[selected_branch]
                start_date = date.today()
                end_date = start_date + timedelta(days=30*term_months)
                interest_rate = 8.5  # Base interest rate, could be made dynamic
                
                db.cursor.execute("""
                    INSERT INTO loans (customer_id, branch_id, loan_type, amount, 
                                     interest_rate, term_months, start_date, end_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (st.session_state.user_id, branch_id, loan_type, amount,
                      interest_rate, term_months, start_date, end_date, 'pending'))
                
                db.connection.commit()
                st.success("Loan application submitted successfully!")
            except Exception as e:
                st.error(f"Error submitting loan application: {e}")


def view_loans():
    st.subheader("Your Loans")
    
    db.cursor.execute("""
        SELECT l.loan_id, l.loan_type, l.amount, l.interest_rate, 
               l.term_months, l.start_date, l.end_date, l.status,
               b.branch_name
        FROM loans l
        JOIN branches b ON l.branch_id = b.branch_id
        WHERE l.customer_id = %s
        ORDER BY l.created_at DESC
    """, (st.session_state.user_id,))
    
    loans = db.cursor.fetchall()
    
    if loans:
        df = pd.DataFrame(loans, columns=[
            "Loan ID", "Type", "Amount", "Interest Rate",
            "Term (months)", "Start Date", "End Date", "Status", "Branch"
        ])
        # Format currency and percentages
        df["Amount"] = df["Amount"].apply(lambda x: f"${x:,.2f}")
        df["Interest Rate"] = df["Interest Rate"].apply(lambda x: f"{x}%")
        st.dataframe(df)
    else:
        st.info("You don't have any loans yet.")


# ---------------------------------------------------------
# Credit Cards Management
# ---------------------------------------------------------
def apply_credit_card():
    st.subheader("Apply for a Credit Card")
    
    with st.form("credit_card_application"):
        card_type = st.selectbox("Card Type", ["Silver", "Gold", "Platinum"])
        income = st.number_input("Annual Income", min_value=0.0, step=1000.0)
        occupation = st.text_input("Occupation")
        
        submitted = st.form_submit_button("Apply")
        
        if submitted:
            try:
                import random
                card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
                expiry_date = date.today() + timedelta(days=365*5)  # 5 years validity
                credit_limit = min(income * 0.4, 1000000)  # 40% of income or max 1M
                
                # Enforce tier limits
                if card_type in CARD_LIMITS:
                    min_lim, max_lim = CARD_LIMITS[card_type]
                    if credit_limit < min_lim:
                        st.error(f"Income too low for {card_type} card (minimum limit ${min_lim:,.2f})")
                        return
                    if credit_limit > max_lim:
                        credit_limit = max_lim
                
                db.cursor.execute("""
                    INSERT INTO credit_cards (customer_id, card_number, card_type, 
                                            expiry_date, credit_limit, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (st.session_state.user_id, card_number, card_type,
                      expiry_date, credit_limit, 'pending'))
                
                db.connection.commit()
                st.success("Credit card application submitted successfully!")
            except Exception as e:
                st.error(f"Error applying for credit card: {e}")


def view_credit_cards():
    st.subheader("Your Credit Cards")
    
    db.cursor.execute("""
        SELECT card_number, card_type, expiry_date, credit_limit,
               current_balance, status, created_at
        FROM credit_cards
        WHERE customer_id = %s
        ORDER BY created_at DESC
    """, (st.session_state.user_id,))
    
    cards = db.cursor.fetchall()
    
    if cards:
        # Process data for display
        display_cards = []
        for card in cards:
            # Mask card number
            masked_number = 'xxxx-xxxx-xxxx-' + card[0][-4:]
            # Calculate available credit
            credit_limit = float(card[3])
            current_balance = float(card[4]) if card[4] is not None else 0.0
            available_credit = credit_limit - current_balance
            
            display_cards.append((
                masked_number, card[1], card[2],
                f"${credit_limit:,.2f}",
                f"${current_balance:,.2f}",
                f"${available_credit:,.2f}",
                card[5]
            ))
        
        df = pd.DataFrame(display_cards, columns=[
            "Card Number", "Type", "Expiry Date", "Credit Limit",
            "Current Balance", "Available Credit", "Status"
        ])
        st.dataframe(df)
    else:
        st.info("You don't have any credit cards yet.")


# ---------------------------------------------------------
# Fixed Deposits Management
# ---------------------------------------------------------
def create_fixed_deposit():
    st.subheader("Create Fixed Deposit")
    
    with st.form("fixed_deposit_form"):
        amount = st.number_input("Deposit Amount", min_value=1000.0, step=1000.0)
        term_months = st.selectbox("Term Period (months)", [12, 24, 36, 60])
        
        # Simple interest rate calculation
        interest_rate = 5.0 + (term_months/12)  # Base rate + term bonus
        st.write(f"Interest Rate: {interest_rate}% per annum")
        
        # Show maturity amount
        maturity_amount = amount * (1 + (interest_rate/100) * (term_months/12))
        st.write(f"Maturity Amount: ${maturity_amount:,.2f}")
        
        submitted = st.form_submit_button("Create Fixed Deposit")
        
        if submitted:
            try:
                start_date = date.today()
                maturity_date = start_date + timedelta(days=30*term_months)
                
                # Get user's primary account
                db.cursor.execute("""
                    SELECT account_id, balance 
                    FROM accounts 
                    WHERE customer_id = %s AND status = 'active'
                    LIMIT 1
                """, (st.session_state.user_id,))
                
                account = db.cursor.fetchone()
                
                if not account:
                    st.error("Please create a bank account first!")
                    return
                
                account_id, balance = account
                
                if balance < amount:
                    st.error("Insufficient balance in your account!")
                    return
                
                # Create FD and deduct amount from account
                db.cursor.execute("""
                    INSERT INTO fixed_deposits (
                        account_id, amount, interest_rate,
                        term_months, start_date, maturity_date
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (account_id, amount, interest_rate, term_months,
                      start_date, maturity_date))
                
                # Update account balance
                db.cursor.execute("""
                    UPDATE accounts 
                    SET balance = balance - %s 
                    WHERE account_id = %s
                """, (amount, account_id))
                
                db.connection.commit()
                st.success("Fixed deposit created successfully!")
            except Exception as e:
                st.error(f"Error creating fixed deposit: {e}")


def view_fixed_deposits():
    st.subheader("Your Fixed Deposits")
    
    db.cursor.execute("""
        SELECT fd.fd_id, 
               CAST(fd.amount AS DECIMAL(15,2)) as amount,
               CAST(fd.interest_rate AS DECIMAL(5,2)) as interest_rate,
               fd.term_months,
               fd.start_date, fd.maturity_date, fd.status,
               a.account_id, a.account_type
        FROM fixed_deposits fd
        JOIN accounts a ON fd.account_id = a.account_id
        WHERE a.customer_id = %s
        ORDER BY fd.created_at DESC
    """, (st.session_state.user_id,))
    
    fds = db.cursor.fetchall()
    
    if fds:
        # Process data for display
        display_fds = []
        from decimal import Decimal
        
        for fd in fds:
            # Convert numeric values to Decimal for precise calculations
            principal = Decimal(str(fd[1]))
            rate = Decimal(str(fd[2]))
            term = int(fd[3])
            
            # Calculate maturity amount
            interest_fraction = rate / Decimal('100')
            term_years = Decimal(str(term)) / Decimal('12')
            interest_multiplier = Decimal('1') + (interest_fraction * term_years)
            maturity_amount = principal * interest_multiplier
            
            days_remaining = (fd[5] - date.today()).days
            status = fd[6]
            if days_remaining < 0:
                status = 'matured'
            
            display_fds.append((
                fd[0],  # FD ID
                f"${float(principal):,.2f}",  # Principal formatted
                f"{float(rate)}%",  # Interest Rate formatted
                term,  # Term (months)
                fd[4],  # Start Date
                fd[5],  # Maturity Date
                f"${float(maturity_amount):,.2f}",  # Maturity Amount formatted
                max(days_remaining, 0),  # Days Remaining
                status,  # Status
                fd[8]   # Linked Account
            ))
        
        df = pd.DataFrame(display_fds, columns=[
            "FD ID", "Principal", "Interest Rate", "Term (months)",
            "Start Date", "Maturity Date", "Maturity Amount",
            "Days Remaining", "Status", "Linked Account"
        ])
        st.dataframe(df)
        
        # Calculate summary metrics using Decimal for precision
        total_invested = Decimal('0')
        total_maturity = Decimal('0')
        
        for fd in fds:
            principal = Decimal(str(fd[1]))
            rate = Decimal(str(fd[2]))
            term = int(fd[3])
            
            total_invested += principal
            maturity = principal * (Decimal('1') + (rate / Decimal('100') * (Decimal(str(term)) / Decimal('12'))))
            total_maturity += maturity
        
        total_earnings = total_maturity - total_invested
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Investment", f"${float(total_invested):,.2f}")
        with col2:
            st.metric("Total Maturity Value", f"${float(total_maturity):,.2f}")
        with col3:
            st.metric("Expected Earnings", f"${float(total_earnings):,.2f}")
    else:
        st.info("You don't have any fixed deposits yet.")


# ---------------------------------------------------------
# Beneficiaries Management
# ---------------------------------------------------------
def manage_beneficiaries():
    st.subheader("Manage Beneficiaries")
    
    tab1, tab2 = st.tabs(["Add Beneficiary", "View Beneficiaries"])
    
    with tab1:
        with st.form("add_beneficiary_form"):
            name = st.text_input("Beneficiary Name")
            account_number = st.text_input("Account Number")
            bank_name = st.text_input("Bank Name")
            ifsc_code = st.text_input("IFSC Code")
            relationship = st.selectbox("Relationship", [
                "Parent", "Spouse", "Child", "Sibling", "Friend", "Other"
            ])
            
            submitted = st.form_submit_button("Add Beneficiary")
            
            if submitted:
                if not all([name, account_number, bank_name, ifsc_code]):
                    st.error("All fields are required!")
                    return
                
                try:
                    # Get user's primary account
                    db.cursor.execute("""
                        SELECT account_id 
                        FROM accounts 
                        WHERE customer_id = %s AND status = 'active'
                        LIMIT 1
                    """, (st.session_state.user_id,))
                    
                    account = db.cursor.fetchone()
                    
                    if account:
                        db.cursor.execute("""
                            INSERT INTO beneficiaries (
                                customer_id, account_id, name,
                                account_number, bank_name, ifsc_code,
                                relationship
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (st.session_state.user_id, account[0], name,
                              account_number, bank_name, ifsc_code, relationship))
                        
                        db.connection.commit()
                        st.success("Beneficiary added successfully!")
                    else:
                        st.error("Please create a bank account first!")
                except Exception as e:
                    st.error(f"Error adding beneficiary: {e}")
    
    with tab2:
        db.cursor.execute("""
            SELECT name, account_number, bank_name, ifsc_code, 
                   relationship, created_at
            FROM beneficiaries
            WHERE customer_id = %s
            ORDER BY created_at DESC
        """, (st.session_state.user_id,))
        
        beneficiaries = db.cursor.fetchall()
        
        if beneficiaries:
            df = pd.DataFrame(beneficiaries, columns=[
                "Name", "Account Number", "Bank Name",
                "IFSC Code", "Relationship", "Added On"
            ])
            st.dataframe(df)
            
            # Add beneficiary deletion option
            st.write("Remove Beneficiary")
            selected_beneficiary = st.selectbox(
                "Select beneficiary to remove",
                [b[0] for b in beneficiaries]  # List of beneficiary names
            )
            
            if st.button("Remove Selected Beneficiary"):
                try:
                    db.cursor.execute("""
                        DELETE FROM beneficiaries
                        WHERE customer_id = %s AND name = %s
                    """, (st.session_state.user_id, selected_beneficiary))
                    
                    db.connection.commit()
                    st.success(f"Beneficiary {selected_beneficiary} removed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error removing beneficiary: {e}")
        else:
            st.info("You haven't added any beneficiaries yet.")


# ---------------------------------------------------------
# Notifications Management
# ---------------------------------------------------------
def view_notifications():
    st.subheader("Notifications")
    
    db.cursor.execute("""
        SELECT notification_id, title, message, type,
               created_at, is_read
        FROM notifications
        WHERE customer_id = %s
        ORDER BY created_at DESC
    """, (st.session_state.user_id,))
    
    notifications = db.cursor.fetchall()
    
    if notifications:
        unread = sum(1 for n in notifications if not n[5])
        if unread > 0:
            st.info(f"You have {unread} unread notification{'s' if unread != 1 else ''}.")
        
        for notif_id, title, message, type_, created_at, is_read in notifications:
            with st.container():
                col1, col2 = st.columns([5,1])
                with col1:
                    if not is_read:
                        title = f"🔵 {title}"
                    st.markdown(f"**{title}**")
                    st.write(message)
                    st.caption(f"{created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                with col2:
                    if not is_read:
                        if st.button("Mark as Read", key=f"mark_read_{notif_id}"):
                            db.cursor.execute("""
                                UPDATE notifications
                                SET is_read = TRUE
                                WHERE notification_id = %s
                            """, (notif_id,))
                            db.connection.commit()
                            st.rerun()
                st.divider()
    else:
        st.info("No notifications to display.")


# ---------------------------------------------------------
# Main Function
# ---------------------------------------------------------


def main():
    if not st.session_state.authenticated:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login_user()
        with tab2:
            register_user()
    else:
        st.sidebar.title("Navigation")

        menu_groups = {
            "Account Management": ["Account Overview", "Create Account"],
            "Transactions": ["Make Transaction", "Transaction History"],
            "Loans": ["Apply for Loan", "View Loans"],
            "Credit Cards": ["Apply for Credit Card", "View Credit Cards"],
            "Investments": ["Create Fixed Deposit", "View Fixed Deposits"],
            "Other Services": ["Manage Beneficiaries", "Notifications"]
        }

        selected_group = st.sidebar.selectbox("Menu", menu_groups.keys())
        page = st.sidebar.radio("Select Option", menu_groups[selected_group])

        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

        # Page Routing
        if page == "Account Overview":
            st.title("Account Overview")
            view_accounts()
        elif page == "Create Account":
            create_account()
        elif page == "Make Transaction":
            view_accounts()
            make_transaction()
        elif page == "Transaction History":
            view_accounts()
            view_transactions()
        elif page == "Apply for Loan":
            apply_loan()
        elif page == "View Loans":
            view_loans()
        elif page == "Apply for Credit Card":
            apply_credit_card()
        elif page == "View Credit Cards":
            view_credit_cards()
        elif page == "Create Fixed Deposit":
            create_fixed_deposit()
        elif page == "View Fixed Deposits":
            view_fixed_deposits()
        elif page == "Manage Beneficiaries":
            manage_beneficiaries()
        elif page == "Notifications":
            view_notifications()

if __name__ == "__main__":
    main()
