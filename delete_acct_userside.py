import time
import textformatting as txf
import retrieveuserdata as ret
import pymysql as sql

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def delete_account(user_name, pin):
    time.sleep(2)
    user_data = ret.retr_user_data(user_name, pin)
    affirm_del = input(
        f'\n\033[1m\033[91m{user_data[4]}\033[0m are you sure you want to delete your account [Y/N]: \033[0m').capitalize()
    time.sleep(2)
    if affirm_del == 'Y':
        del_acc_query = "DELETE FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(del_acc_query, (user_name, pin))
        conn_obj.commit()

        if my_cur.rowcount > 0:
            txf.print_with_delay(txf.italic() + '\t\tdeleting Account...' + txf.end())
            time.sleep(2)
            print(f"\n\t\033[1mAccount; {user_data[4]} deleted successfully.\033[0m")
        else:
            print("\n\033[31mAccount not found.\033[0m")

    elif affirm_del == 'N':
        print('\n\t\033[1mYou have cancelled the account delete\033[0m')

    else:
        print('\n\033[31mPlease input a valid option\033[0m')
