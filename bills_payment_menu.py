import time
import pymysql as sql
import loggedinmenu
import textformatting as txf
import mobile_menu
import pay_electricity
import pay_water
import config
import backs

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def bills_payment_menu():
    print(txf.bold() + "\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+---------------+------------------+--------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| Bills Payment Menu                                                     |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+---------------+------------------+--------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1. Electricity Bill  | 2. Water Bill | 3. Mobile Top-up | 4.   Exit    |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+---------------+------------------+--------------+\n")

    option = input("Select an utility: " + txf.end())
    time.sleep(2)

    if option == '1':
        time.sleep(2)
        pay_electricity.pay_electricity_bill(config.user_name, config.pin_)
        backs.back_to_bill_payment_menu()
    elif option == '2':
        time.sleep(1)
        pay_water.pay_water_bill(config.user_name, config.pin_)
        backs.back_to_bill_payment_menu()
    elif option == '3':
        time.sleep(2)
        mobile_menu.mobile_top_up_menu()
    elif option == '4':
        time.sleep(1.5)
        txf.print_with_delay(txf.italic() + '\n\tExiting...' + txf.end())
        loggedinmenu.logged_in_menu()
    else:
        print('Invalid Input...')
