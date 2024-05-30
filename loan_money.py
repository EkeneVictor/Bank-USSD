import time
import pymysql as sql
from create_acct import check_restrictions
import config
import textformatting as txf
import string
import random
from datetime import datetime, timedelta
import loggedinmenu

# connecting to the mysql server

conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server

my_cur = conn_obj.cursor()


def log_loan(transaction_id, amount, user_name, description):
    try:
        with open('loan_statements.txt', 'a') as loan_statements:
            loan_statements.write(f'Transaction ID: {transaction_id}\n')
            loan_statements.write(f'User: {user_name}\n')
            loan_statements.write(f'Amount: ${amount}\n')
            loan_statements.write(f'Description: {description}\n')
            loan_statements.write(f'Date/Time: {datetime.now()}\n')
            loan_statements.write('--------------------------------------------\n')
    except Exception as e:
        print(f"An error occurred while logging loan transaction: {e}")


def is_eligible(user_name):
    check_user_query = "SELECT acct_bal, acct_status, creation_date FROM bank_tbl WHERE user_name = %s"
    my_cur.execute(check_user_query, (user_name,))
    user = my_cur.fetchone()

    if not user:
        return False, "User not found"

    acct_bal, acct_status, acct_creation_date = user
    if acct_status != 'Active':
        return False, "Account not active"

    # Check if the user has an active loan
    check_loan_query = "SELECT transaction_id FROM loans_tbl WHERE user_name = %s AND repayment_status = 'Pending'"
    my_cur.execute(check_loan_query, (user_name,))
    loan = my_cur.fetchone()

    if loan:
        return False, f"User already has an active loan {loan}"

    account_age = (datetime.now() - acct_creation_date).days
    if account_age < 90:
        return False, "Account must be at least 3 months old"

    if acct_bal < 500:
        return False, "Minimum balance requirement not met"

    return True, "Eligible"


def process_loan_application(user_name, amount, repayment_period, trans_pin_input, pin):
    eligibility, message = is_eligible(user_name)
    if not eligibility:
        return f"Loan application denied: {message}"

    check_pin_query = "SELECT transaction_pin, acct_type FROM bank_tbl WHERE user_name = %s and PIN = %s"
    my_cur.execute(check_pin_query, (user_name, pin))
    result = my_cur.fetchone()
    if result:
        trans_pin, acct_type = result
        if trans_pin_input == trans_pin:
            # Check the restrictions before proceeding
            status, message = check_restrictions(acct_type, 'loan', amount)
            if not status:
                print(message)
                return

    interest_rate = 0.15
    total_repayment = amount + (amount * interest_rate * (repayment_period / 12))
    monthly_installment = total_repayment / repayment_period
    outstanding_balance = total_repayment
    present_date = datetime.now()
    due_date = present_date + timedelta(days=repayment_period * 30)
    # Generate a transaction ID
    transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=22))

    # Log the loan in the database
    insert_loan_query = """INSERT INTO loans_tbl (transaction_id, user_name, amount, interest_rate, total_repayment, 
                        monthly_installment, repayment_period, status, application_date, outstanding_balance, due_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    my_cur.execute(insert_loan_query, (
        transaction_id, user_name, amount, interest_rate, total_repayment, monthly_installment, repayment_period,
        'Approved', present_date, outstanding_balance, due_date))
    conn_obj.commit()

    sender_acct = 'LOAN'
    sender_user_name = 'LOAN'
    sender_acct_type = 'LOAN'

    select_recipient_acct = "SELECT acct_num FROM bank_tbl WHERE user_name = %s"
    my_cur.execute(select_recipient_acct, user_name)
    recipient_account = my_cur.fetchone()[0]

    # Get recipient's account type
    reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
    my_cur.execute(reciever_acct_type_query, (recipient_account,))
    reciever_acct_type = my_cur.fetchone()[0]

    description = f'LOAN OF {amount}'

    # log the loan into transaction table
    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
    my_cur.execute(update_trans_table, (
        transaction_id, amount, sender_acct, recipient_account, sender_user_name,
        user_name, datetime.now(), description, sender_acct_type,
        reciever_acct_type, 'Successful'))
    conn_obj.commit()

    # Update user's account balance
    update_balance_query = "UPDATE bank_tbl SET acct_bal = acct_bal + %s WHERE user_name = %s"
    my_cur.execute(update_balance_query, (amount, user_name))
    conn_obj.commit()

    # Update accounts table
    update_accounts_query = "UPDATE accounts SET balance = balance + %s WHERE user_name = %s and account_type = %s"
    my_cur.execute(update_accounts_query, (amount, user_name, reciever_acct_type))
    conn_obj.commit()

    # Update admins account balance
    update_admin_query = "UPDATE bank_tbl SET acct_bal = acct_bal - %s WHERE user_name = %s"
    my_cur.execute(update_admin_query, (amount, 'BANKADMIN'))
    conn_obj.commit()

    # Log the loan transaction
    log_loan(transaction_id, amount, user_name, "Loan Disbursement")

    return f"Loan approved: ${amount} disbursed. Monthly installment: ${monthly_installment:.2f}"


def check_loan_status(user_name):
    try:
        check_loan_query = "SELECT amount, total_repayment, monthly_installment, repayment_period, outstanding_balance, status FROM loans_tbl WHERE user_name = %s AND status = 'Approved'"
        my_cur.execute(check_loan_query, (user_name,))
        loans = my_cur.fetchall()

        if not loans:
            return "No active loans"

        loan_details = ""
        for loan in loans:
            amount, total_repayment, monthly_installment, repayment_period, outstanding_balance, status = loan
            loan_details += f"Loan Amount: ${amount}\n"
            loan_details += f"Total Repayment: ${total_repayment}\n"
            loan_details += f"Monthly Installment: ${monthly_installment}\n"
            loan_details += f"Repayment Period: {repayment_period} months\n"
            loan_details += f"Outstanding Balance: ${outstanding_balance}\n"
            loan_details += f"Status: {status}\n\n"

        return loan_details.strip()

    except Exception as e:
        return f"An error occurred while fetching loan details: {e}"


def log_loan_repayment(repayment_id, loan_id, user_name, amount, description):
    try:
        with open('loan_repayment_statements.txt', 'a') as repayment_statements:
            repayment_statements.write(f'Repayment ID: {repayment_id}\n')
            repayment_statements.write(f'Loan ID: {loan_id}\n')
            repayment_statements.write(f'User: {user_name}\n')
            repayment_statements.write(f'Amount: ${amount}\n')
            repayment_statements.write(f'Description: {description}\n')
            repayment_statements.write(f'Date/Time: {datetime.now()}\n')
            repayment_statements.write('--------------------------------------------\n')
    except Exception as e:
        print(f"An error occurred while logging loan repayment: {e}")


# def process_loan_repayment(user_name, loan_id, amount):
#     try:
#         # Retrieve the loan details
#         get_loan_query = "SELECT total_repayment, outstanding_balance FROM loans_tbl WHERE transaction_id = %s AND user_name = %s"
#         my_cur.execute(get_loan_query, (loan_id, user_name))
#         loan = my_cur.fetchone()
#
#         if loan[11] == 'Paid':
#             return "Loan not found"
#
#         total_repayment, outstanding_balance = loan
#
#         # Calculate the new outstanding balance
#         new_outstanding_balance = outstanding_balance - amount
#         if new_outstanding_balance < 0:
#             return "Amount exceeds outstanding balance"
#
#         # Update the outstanding balance in the loan table
#         update_loan_query = "UPDATE loans_tbl SET outstanding_balance = %s WHERE transaction_id = %s"
#         my_cur.execute(update_loan_query, (new_outstanding_balance, loan_id))
#         conn_obj.commit()
#
#         # Insert the repayment record into the loan_repayments_tbl
#         insert_repayment_query = """INSERT INTO loan_repayments_tbl (loan_id, user_name, amount, payment_date, status)
#                                     VALUES (%s, %s, %s, %s, %s)"""
#         my_cur.execute(insert_repayment_query, (loan_id, user_name, amount, datetime.now(), 'Completed'))
#         conn_obj.commit()
#
#         repayment_id = my_cur.lastrowid
#         log_loan_repayment(repayment_id, loan_id, user_name, amount, "Loan Repayment")
#
#         return f"Repayment of ${amount} processed. New outstanding balance: ${new_outstanding_balance:.2f}"
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return "Repayment processing failed"


# def check_loan_status(user_name):
#     check_loan_query = "SELECT amount, total_repayment, outstanding_balance, monthly_installment, repayment_period, status FROM loans_tbl WHERE user_name = %s AND status = 'Approved'"
#     my_cur.execute(check_loan_query, (user_name,))
#     loan = my_cur.fetchone()
#
#     if not loan:
#         return "No active loans"
#
#     amount, total_repayment, outstanding_balance, monthly_installment, repayment_period, status = loan


def make_loan_repayment(user_name):
    try:
        # Check if the user has an active loan
        check_loan_query = "SELECT transaction_id, outstanding_balance FROM loans_tbl WHERE user_name = %s AND repayment_status = 'Pending'"
        my_cur.execute(check_loan_query, (user_name,))
        loan = my_cur.fetchone()

        if not loan:
            return "You do not have an active loan."

        transaction_id, outstanding_balance = loan

        if loan:
            print(f'You have an outstanding balance of ${outstanding_balance}')
            time.sleep(2)
            amount = float(input('Enter amount you would like to pay off: '))

            if amount > outstanding_balance:
                return "Repayment amount exceeds outstanding balance."

            # Deduct the repayment amount from the user's account balance
            update_balance_query = "UPDATE bank_tbl SET acct_bal = acct_bal - %s WHERE user_name = %s"
            my_cur.execute(update_balance_query, (amount, user_name))

            # Update the outstanding balance of the loan
            new_balance = outstanding_balance - amount
            update_loan_query = "UPDATE loans_tbl SET outstanding_balance = %s WHERE transaction_id = %s"
            my_cur.execute(update_loan_query, (new_balance, transaction_id))

            select_recipient_acct = "SELECT acct_num FROM bank_tbl WHERE user_name = %s"
            my_cur.execute(select_recipient_acct, user_name)
            sender_acct = my_cur.fetchone()[0]

            # Get recipient's account type
            reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
            my_cur.execute(reciever_acct_type_query, (sender_acct,))
            sender_acct_type = my_cur.fetchone()[0]

            # Update sender accounts table
            update_accounts_query = "UPDATE accounts SET balance = balance - %s WHERE user_name = %s and account_type = %s"
            my_cur.execute(update_accounts_query, (amount, user_name, sender_acct_type))
            conn_obj.commit()

            # Update the Admin account balance directly in the database
            update_admin_acct_bal = "UPDATE bank_tbl SET acct_bal = acct_bal + %s WHERE acct_type = 'Admin'"
            my_cur.execute(update_admin_acct_bal, (amount,))
            conn_obj.commit()

            recipient_acct = 'LOAN REPAYMENT'
            rec_user_name = 'LOAN REPAYMENT'
            description = f'REPAYMENT OF ${amount} LOAN'
            rec_acct_type = 'LOAN REPAYMENT'

            # log the loan repayment into transaction table
            update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
            my_cur.execute(update_trans_table, (
                transaction_id, amount, sender_acct, recipient_acct, user_name,
                rec_user_name, datetime.now(), description, sender_acct_type,
                rec_acct_type, 'Successful'))
            conn_obj.commit()

            # Insert the repayment record into loan_repayments_tbl
            insert_repayment_query = """
            INSERT INTO loan_repayments_tbl (loan_id, user_name, amount, payment_date, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            my_cur.execute(insert_repayment_query, (transaction_id, user_name, amount, datetime.now(), 'Paid'))

            # Commit the changes to the database
            conn_obj.commit()

            # Check if the loan is fully repaid
            if new_balance == 0:
                update_loan_status_query = "UPDATE loans_tbl SET repayment_status = 'Paid' WHERE transaction_id = %s"
                my_cur.execute(update_loan_status_query, (transaction_id,))
                conn_obj.commit()
                return f"Loan repayment successful.\nYour new outstanding balance is ${new_balance}.\nYou have cleared your loan."
            else:
                return f"Loan repayment successful.\nYour new outstanding balance is ${new_balance}."

    except Exception as e:
        return f"An error occurred while processing loan repayment: {e}"


def loan_menu(user_name):
    print(
        txf.bold() + "\t\t\t\t\t\t\t\t\t\t\t\t\t+-----------------------+---------------+------------------+--------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| Loan  Menu                                                             |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+----------------+------------------+--------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1.  Apply for Loan   | 2. Loan Status | 3. Repay Loan    | 4.   Exit    |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+----------------+------------------+--------------+\n")

    user_input = input(">>>: ")
    if user_input == "1":
        time.sleep(3)
        amount = float(input("Enter loan amount: "))
        repayment_period = int(input("Enter repayment period in months: "))
        trans_pin_input = input("Enter your transaction pin: ")
        response = process_loan_application(user_name, amount, repayment_period, trans_pin_input, config.pin_)
        print(response)
    elif user_input == "2":
        time.sleep(2)
        response = check_loan_status(user_name)
        print(response)
    elif user_input == '3':
        time.sleep(1)
        response = make_loan_repayment(user_name)
        print(response)
    elif user_input == '4':
        time.sleep(1.5)
        txf.print_with_delay(txf.italic() + '\n\tExiting...' + txf.end())
        loggedinmenu.logged_in_menu()
    else:
        print("Invalid input. Please try again.")
