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

        with open('admin_statements.txt', 'a') as acct_statements:
            acct_statements.write(f'\n\n\t\t\t\t\t\t\t\tStatement for {user_name_input}\n')
            acct_statements.write(str(table))
            acct_statements.flush()

        print('\n\t\033[1mAccount statement generated. \n\tCheck user inbox for statement\033[0m')
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
        user_acct_status = my_cur.fetchone()
        user_acct_status = str(user_acct_status[11])

        if user_acct_status == 'Active':
            time.sleep(2)
            print(txf.bold() + f"{admin} has " + f"{txf.bright_green() + 'unblocked ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
        else:
            time.sleep(3)
            txf.display_error('Error...')
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
        user_acct_status = my_cur.fetchone()
        user_acct_status = str(user_acct_status[11])

        if user_acct_status == 'Active':
            time.sleep(2)
            print(txf.bold() + f"{admin} has " + f"{txf.bright_green() + 'resumed ' + txf.end()}" + f"{user_name_input}'s account successfully" + txf.end())
        else:
            time.sleep(3)
            txf.display_error('Error...')
    except Exception as e:
        print(f'error occurred : {e}')
