import retrieveuserdata as retr
import time
import backs
import textformatting as txf
import pymysql as sql
import adminmenu
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


def logged_in():
    # Retrieve user data
    user_data = retr.retrieve_user_data()
    if user_data is None:
        time.sleep(2.5)
        txf.display_error('Invalid User name or PIN. Please try again')

        backs.back_to_options_menu()

    if user_data[12] == 'Admin':
        try:
            user_name = user_data[4]

            time.sleep(1.5)
            print(txf.italic() + f'\n\tLogged in as {user_name}.' + txf.end())
        except Exception as e:
            print(f'error :{e}')

        time.sleep(2)

        adminmenu.admin_menu()

    if user_data[12] != 'Admin' and user_data[11] == 'Active':
        if user_data:
            time.sleep(2.5)
            print(txf.bold() + f"\t\nLogin successful. Welcome, {user_data[4]}!" + txf.end())
            time.sleep(2.5)

            loggedinmenu.logged_in_menu()

            backs.back_to_options_menu()
        time.sleep(2)

    if user_data[11] == 'Blocked':
        time.sleep(3)
        customer_service = 'http://127.0.0.1:5500/cipherbank.html'
        txf.display_error(txf.bold() + txf.red() + f'\n\tAccount; {user_data[4]} has been blocked.\n\t\tAccess cannot be granted\n\t\t\tPlease contact the customer service;{txf.italic() + customer_service + txf.end() + txf.end() + txf.end()}')

        backs.back_to_options_menu()

    if user_data[11] == 'Suspended':
        time.sleep(2)
        customer_service = 'http://127.0.0.1:5500/cipherbank.html'
        txf.display_error(
            txf.bold() + txf.yellow() + f'\n\tAccount; {user_data[4]} has been suspended.\n\t\tAccess cannot be granted\n\t\t\tPlease contact the customer service;{txf.italic() + customer_service + txf.end() + txf.end() + txf.end()}')

        backs.back_to_options_menu()


logged_in()
