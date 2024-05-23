import time
import pymysql as sql
import textformatting as txf
import adminoptions

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def admin_menu():
    time.sleep(3)
    print(txf.bold() + '\n\t+-----------------------------+-----------------------------+--------------------------------+')
    print('\t|                       ADMIN                           OPTIONS                              |')
    print('\t+-----------------------------+-----------------------------+--------------------------------+')
    print('\t|   1. Check   user  details  |   2. Delete user account    |  3.  Block  user  account      |')
    print('\t+-----------------------------+-----------------------------+--------------------------------+')
    print('\t|   4.  Suspend user account  |  5. Unblock  user  account  |   6.   Resume user account     |')
    print('\t+-----------------------------+-----------------------------+--------------------------------+')
    print(f'\t|  7. Generate user Statement |   8.     Log   out          |   9.      {txf.italic() + txf.yellow() + 'coming  soon' + txf.end() + txf.end()}         |')
    print('\t+-----------------------------+-----------------------------+--------------------------------+' + txf.end())

    while True:

        cntn = input(txf.bold() + '>>> ' + txf.end())

        if cntn != '1' and cntn != '2' and cntn != '3' and cntn != '4' and cntn != '5' and cntn != '6' and cntn != '7' and cntn != '8':
            time.sleep(2)
            txf.display_error('Invalid input. Please try again.')
            continue
        else:
            if cntn == '1':
                time.sleep(3)
                adminoptions.check_acct_details_for_user()
            elif cntn == '2':
                time.sleep(1)
                adminoptions.delete_acct_for_user()
            elif cntn == '3':
                time.sleep(1)
                adminoptions.block_user_acct()
            elif cntn == '4':
                time.sleep(1.5)
                adminoptions.suspend_user_acct()
            elif cntn == '5':
                time.sleep(3)
                adminoptions.unblock_user_acct()
            elif cntn == '6':
                time.sleep(3)
                adminoptions.resume_user_acct()
            elif cntn == '7':
                time.sleep(3)
                adminoptions.gen_user_acct_statement()
            elif cntn == '8':
                time.sleep(1)
                print(txf.italic() + "\n\tLogging out ....")
                time.sleep(3)
                print("\n\tLogged out successfully." + txf.end())
                import backs
                backs.back_to_options_menu()
            else:
                txf.display_error('Invalid option. Please choose again.')
                continue
        import backs
        backs.back_to_admin_menu()
    time.sleep(2)

admin_menu()