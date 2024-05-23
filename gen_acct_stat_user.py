import time
import pymysql as sql
from prettytable import PrettyTable
from datetime import datetime
import textformatting as txf

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def generate_account_statement(user_name):
    try:
        start_date_str = input('\n\033[1mEnter start date to generate statement: \033[0m')
        stop_date_str = input('\n\033[1mEnter stop date for statement: \033[0m')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        stop_date = datetime.strptime(stop_date_str, '%Y-%m-%d')

        my_cur.execute(
            "SELECT * FROM transaction_tbl WHERE (sender_user_name = %s OR reciever_user_name = %s) AND transaction_date_time BETWEEN %s AND %s",
            (user_name, user_name, start_date, stop_date))
        all_transactions = my_cur.fetchall()

        table = PrettyTable()
        table.field_names = ['transaction_id', 'transaction_amount', 'sender_acct_num',
                             'reciever_acct_num', 'sender_user_name', 'reciever_user_name',
                             'transaction_date_time', 'description', 'sender_acct_type',
                             'reciever_acct_type', 'transaction_status']

        for transaction in all_transactions:
            table.add_row(transaction)

        with open('account_statement.txt', 'w') as acct_statements:
            acct_statements.write(str(table))
            acct_statements.flush()

        time.sleep(3)
        txf.print_with_delay('.......')
        time.sleep(2)
        print('\n\t\033[1mAccount statement generated. \n\tCheck your inbox for statement\033[0m')
    except Exception as e:
        print(f"An error occurred: {e}")
