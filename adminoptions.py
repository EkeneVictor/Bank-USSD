import textformatting as txf
import pymysql as sql
import time
from datetime import datetime
from prettytable import PrettyTable

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def check_acct_details_for_user():
    """function that prints details of specified user"""
    try:
        user_name_input = txf.get_user_input('Enter user name: ')
        user_name_query = "SELECT * FROM bank_tbl WHERE user_name = %s"
        my_cur.execute(user_name_query, user_name_input)
        user_data = my_cur.fetchone()
        if user_data:
            time.sleep(4)
            print(
                f'{txf.bold()}\n\t+------------------------------+\n\t'
                f'|      Account Details      '
                f'\n\t+------------------------------+\n'
                f'\t| First name: {user_data[1]}\n'
                f'\t| Last name: {user_data[2]}\n'
                f'\t| Phone number: {user_data[3]}\n'
                f'\t| User name: {user_data[4]}\n'
                f'\t| User ID: {user_data[5]}\n'
                f'\t| Account number: {user_data[6]}\n'
                f'\t| BVN: {user_data[7]}\n'
                f'\t| NIN: {user_data[8]}\n'
                f'\t| Account Balance: ${user_data[9]}\n'
                f'\t| PIN: {user_data[10]}\n'
                f'\t| Account Status: {user_data[11]}\n'
                f'\t| Account Type: {user_data[12]}\n'
                f'\t| Transaction PIN: {user_data[13]}\n'
                f'\t+------------------------------+\n{txf.end()}'
            )
        else:
            time.sleep(4)
            txf.display_error('Account does not exist')
    except Exception as e:
        print(f'error occurred : {e}')


def delete_acct_for_user():
    """function to delete user account from db"""
    user_name = 'BANKADMIN'
    pin_ = '00000'

    check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
    my_cur.execute(check_login_data, (user_name, pin_))
    user = my_cur.fetchone()
    admin = user[4]
    try:
        user_name_input = txf.get_user_input(txf.bold() + 'Enter user name: ' + txf.end()).upper()

        affirm_del = txf.get_user_input(txf.bold() + f'Are you sure you want to permanently delete {user_name_input} from the database [Y/N]?: ' + txf.end()).upper()
        if affirm_del == 'Y':
            del_user_query = "DELETE FROM bank_tbl WHERE user_name = %s"
            if del_user_query:
                my_cur.execute(del_user_query, user_name_input)
                conn_obj.commit()
            else:
                txf.display_error('User does not exist')

            if my_cur.rowcount > 0:
                print(txf.bold() + f"{admin} has " + f"{txf.red() + 'deleted ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
            else:
                txf.display_error('Account not found.')

        elif affirm_del == 'N':
            print(txf.bold() + '\n\tYou have cancelled the account delete' + txf.end())

        else:
            txf.display_error('Please input a valid option')
    except Exception as e:
        print(f'error occurred : {e}')


def block_user_acct():
    """function to block user account"""
    user_name = 'BANKADMIN'
    pin_ = '00000'

    check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
    my_cur.execute(check_login_data, (user_name, pin_))
    user = my_cur.fetchone()
    admin = user[4]
    try:
        user_name_input = txf.get_user_input(txf.bold() + 'Enter user name: ' + txf.end()).upper()
        block_acct_query = "UPDATE `bank_tbl` SET `acct_status` = 'Blocked' WHERE user_name = %s"
        my_cur.execute(block_acct_query, (user_name_input,))
        conn_obj.commit()

        check_acct_for_block = "SELECT * FROM bank_tbl WHERE user_name = %s "
        my_cur.execute(check_acct_for_block, (user_name_input,))
        user_acct = my_cur.fetchone()

        if user_acct is not None:
            user_acct_status = str(user_acct[11])
            if user_acct_status == 'Blocked':
                time.sleep(2)
                print(txf.bold() + f"{admin} has " + f"{txf.red() + 'blocked ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
            else:
                time.sleep(3)
                txf.display_error('Error...')
        else:
            txf.display_error('Account does not exist')
    except Exception as e:
        print(f'error occurred : {e}')


def suspend_user_acct():
    """function to suspend user account"""
    user_name = 'BANKADMIN'
    pin_ = '00000'

    check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
    my_cur.execute(check_login_data, (user_name, pin_))
    user = my_cur.fetchone()
    admin = user[4]
    try:
        user_name_input = txf.get_user_input(txf.bold() + 'Enter user name: ' + txf.end()).upper()
        suspend_acct_query = "UPDATE `bank_tbl` SET `acct_status` = 'Suspended' WHERE user_name = %s"
        my_cur.execute(suspend_acct_query, user_name_input)
        conn_obj.commit()

        check_acct_for_sus = "SELECT * FROM bank_tbl WHERE user_name = %s "
        my_cur.execute(check_acct_for_sus, user_name_input)
        user_acct_status = my_cur.fetchone()
        user_acct_status = str(user_acct_status[11])

        if user_acct_status == 'Suspended':
            print(txf.bold() + f"{admin} has " + f"{txf.yellow() + 'suspended ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
        else:
            txf.display_error('Error...')
    except Exception as e:
        print(f'error occurred : {e}')


def gen_user_acct_statement():
    """function to generate all transactions for specified user within a date range"""
    try:
        user_name_input = txf.get_user_input(txf.bold() + 'Enter user name: ' + txf.end()).upper()
        start_date_str = txf.get_user_input(txf.bold() + 'Enter start date [YYYY-MM-DD]: ' + txf.end())
        stop_date_str = txf.get_user_input(txf.bold() + 'Enter stop date [YYYY-MM-DD]: ' + txf.end())
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        stop_date = datetime.strptime(stop_date_str, '%Y-%m-%d')

        my_cur.execute(
            "SELECT * FROM transaction_tbl WHERE (sender_user_name = %s OR reciever_user_name = %s) AND transaction_date_time BETWEEN %s AND %s",
            (user_name_input, user_name_input, start_date, stop_date))
        all_transactions = my_cur.fetchall()

        table = PrettyTable()
        table.field_names = ['transaction_id', 'transaction_amount', 'sender_acct_num',
                             'reciever_acct_num', 'sender_user_name', 'reciever_user_name',
                             'transaction_date_time', 'description', 'sender_acct_type',
                             'reciever_acct_type', 'transaction_status']

        for transaction in all_transactions:
            table.add_row(transaction)

        with open('admin_statements.txt', 'w') as acct_statements:
            acct_statements.write(f'\n\n\t\t\t\t\t\t\t\tStatement for {user_name_input}\n')
            acct_statements.write(str(table))
            acct_statements.flush()

        print(txf.bold() + 'Account statement generated. \n\tCheck user inbox for statement' + txf.end())
    except Exception as e:
        print(f"An error occurred: {e}")


def unblock_user_acct():
    """function to unblock a blocked account"""
    user_name = 'BANKADMIN'
    pin_ = '00000'

    check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
    my_cur.execute(check_login_data, (user_name, pin_))
    user = my_cur.fetchone()
    admin = user[4]
    try:
        user_name_input = txf.get_user_input(txf.bold() + 'Enter user name: ' + txf.end()).upper()
        block_acct_query = "UPDATE `bank_tbl` SET `acct_status` = 'Active' WHERE user_name = %s and acct_status = 'Blocked'"
        my_cur.execute(block_acct_query, user_name_input)
        conn_obj.commit()

        check_acct_for_block = "SELECT * FROM bank_tbl WHERE user_name = %s "
        my_cur.execute(check_acct_for_block, user_name_input)
        user_acct = my_cur.fetchone()

        if user_acct:
            user_acct_status = str(user_acct[11])
            if user_acct_status == 'Active':
                time.sleep(2)
                print(txf.bold() + f"{admin} has " + f"{txf.bright_green() + 'unblocked ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
            else:
                time.sleep(3)
                txf.display_error('Error...')
        else:
            txf.display_error('Account not found')
    except Exception as e:
        print(f'error occurred : {e}')


def resume_user_acct():
    """function to resume account suspended"""
    user_name = 'BANKADMIN'
    pin_ = '00000'

    check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
    my_cur.execute(check_login_data, (user_name, pin_))
    user = my_cur.fetchone()
    admin = user[4]
    try:
        user_name_input = txf.get_user_input(txf.bold() + 'Enter user name: ' + txf.end()).upper()
        block_acct_query = "UPDATE `bank_tbl` SET `acct_status` = 'Active' WHERE user_name = %s and acct_status = 'Suspended'"
        my_cur.execute(block_acct_query, (user_name_input,))
        conn_obj.commit()

        check_acct_for_block = "SELECT * FROM bank_tbl WHERE user_name = %s "
        my_cur.execute(check_acct_for_block, (user_name_input,))
        user_acct = my_cur.fetchone()

        if user_acct:
            user_acct_status = str(user_acct[11])
            if user_acct_status == 'Active':
                time.sleep(2)
                print(txf.bold() + f"{admin} has " + f"{txf.bright_green() + 'resumed ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
            else:
                time.sleep(3)
                txf.display_error('Error...')
        else:
            txf.display_error('Account not found')
    except Exception as e:
        print(f'error occurred : {e}')


def process_due_loans():
    try:
        # Fetch loans that are past due and still have outstanding balances
        due_loans_query = """
        SELECT transaction_id, user_name, outstanding_balance, monthly_installment, due_date 
        FROM loans_tbl 
        WHERE status = 'Approved' AND repayment_status = 'Pending' AND due_date < NOW()
        """
        my_cur.execute(due_loans_query)
        due_loans = my_cur.fetchall()

        if not due_loans:
            print("No due loans found.")
            return

        for loan in due_loans:
            transaction_id, user_name, outstanding_balance, monthly_installment, due_date = loan

            # Fetch user's account balance
            check_balance_query = "SELECT acct_bal FROM bank_tbl WHERE user_name = %s"
            my_cur.execute(check_balance_query, (user_name,))
            user_balance = my_cur.fetchone()[0]

            # Determine the repayment amount
            repayment_amount = min(monthly_installment, outstanding_balance)

            if user_balance >= repayment_amount:
                # Deduct the repayment amount from the user's account balance
                update_balance_query = "UPDATE bank_tbl SET acct_bal = acct_bal - %s WHERE user_name = %s"
                my_cur.execute(update_balance_query, (repayment_amount, user_name))

                # Update the outstanding balance of the loan
                new_balance = outstanding_balance - repayment_amount
                update_loan_query = "UPDATE loans_tbl SET outstanding_balance = %s, last_repayment_date = %s WHERE transaction_id = %s"
                my_cur.execute(update_loan_query, (new_balance, datetime.now(), transaction_id))

                # Update the balance of admin account
                update_admin_query = "UPDATE bank_tbl SET acct_bal = acct_bal + %s WHERE user_name = %s"
                my_cur.execute(update_admin_query, (repayment_amount, 'BANKADMIN'))

                select_recipient_acct = "SELECT acct_num FROM bank_tbl WHERE user_name = %s"
                my_cur.execute(select_recipient_acct, user_name)
                sender_acct = my_cur.fetchone()[0]

                # Get recipient's account type
                reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                my_cur.execute(reciever_acct_type_query, (sender_acct,))
                sender_acct_type = my_cur.fetchone()[0]

                # Update sender acounts table
                update_accounts_query = "UPDATE accounts SET balance = balance - %s WHERE user_name = %s and account_type = %s"
                my_cur.execute(update_accounts_query, (repayment_amount, user_name, sender_acct_type))
                conn_obj.commit()

                recipient_acct = 'LOAN REPAYMENT'
                rec_user_name = 'LOAN REPAYMENT'
                description = f'REPAYMENT OF ${repayment_amount} LOAN'
                rec_acct_type = 'LOAN REPAYMENT'

                # log the loan repayment into transaction table
                update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                my_cur.execute(update_trans_table, (
                    transaction_id, repayment_amount, sender_acct, recipient_acct, user_name,
                    rec_user_name, datetime.now(), description, sender_acct_type,
                    rec_acct_type, 'Successful'))
                conn_obj.commit()

                # Insert the repayment record into loan_repayments_tbl
                insert_repayment_query = """
                INSERT INTO loan_repayments_tbl (loan_id, user_name, amount, payment_date, status)
                VALUES (%s, %s, %s, %s, %s)
                """
                my_cur.execute(insert_repayment_query, (transaction_id, user_name, repayment_amount, datetime.now(), 'Paid'))

                # If the loan is fully repaid, update the loan status
                if new_balance == 0:
                    update_loan_status_query = "UPDATE loans_tbl SET repayment_status = 'Paid' WHERE transaction_id = %s"
                    my_cur.execute(update_loan_status_query, (transaction_id,))

                print(f"Processed repayment for user {user_name}, loan {transaction_id}. New balance: {new_balance}")

            else:
                print(f"Insufficient funds for user {user_name} to repay loan {transaction_id}.")

        # Commit all changes to the database
        conn_obj.commit()

    except Exception as e:
        print(f"An error occurred while processing due loans: {e}")