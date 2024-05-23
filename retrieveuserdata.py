import time
import pymysql as sql
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


def retr_user_data(user_name, pin_):
    """Retrieves user data for admin"""
    time.sleep(2.5)

    if user_name and pin_:
        # Query the database to check if the provided BVN and PIN match any user records
        check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
        my_cur.execute(check_login_data, (user_name, pin_))
        user = my_cur.fetchone()
        if user:
            return user
    else:
        txf.display_error('You have not logged in')
        return None  # Return None if the user is not logged in


def retrieve_user_data():
    """Retrieves user data for user"""
    time.sleep(2.5)
    user_name = txf.get_user_input(txf.bold() + 'Input your User name: ' + txf.end())
    time.sleep(1)
    pin_ = txf.get_user_input('Input your 5-digit PIN: ')

    if user_name and pin_:
        # Query the database to check if the provided BVN and PIN match any user records
        check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
        my_cur.execute(check_login_data, (user_name, pin_))
        user = my_cur.fetchone()

        if user:
            return user
    else:
        txf.display_error('You have not logged in')
        return None  # Return None if the user is not logged in
