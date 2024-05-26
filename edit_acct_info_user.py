import time
import pymysql as sql
import loggedinmenu
import textformatting as txf
from create_acct import conf_user_name

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def edit_acct_info(user_name, pin):
    try:
        time.sleep(1)
        print(txf.bold() + '\n\t\t\t\t+------------------------------+---------------------------+-------------------------+')
        print('\t\t\t\t|    Please choose an option                                                       |')
        print('\t\t\t\t+------------------------------+---------------------------+-------------------------+')
        print('\t\t\t\t|   1.    Change First name    | 2.   Change Last name     | 3. Change Phone number  |')
        print('\t\t\t\t+------------------------------+---------------------------+-------------------------+')
        print('\t\t\t\t|   4.    Change Pin           | 5. Change Transaction PIN | 6.        Exit          |')
        print('\t\t\t\t+------------------------------+---------------------------+-------------------------+')

        time.sleep(0.5)
        inp = input('>>> ' + txf.end())
        time.sleep(1)
        if inp == '1':
            new_first_name = input('\n\033[1mEnter your new first name: \033[0m').capitalize()
            time.sleep(2)
            insert_new_first_name_query = "UPDATE bank_tbl SET first_name = %s WHERE user_name = %s AND PIN = %s"
            my_cur.execute(insert_new_first_name_query, (new_first_name, user_name, pin))
            txf.print_with_delay('changing...')
            time.sleep(2)
            print('\n\t\t\033[3m first name updated successfully\033[0m')
            time.sleep(1)
            print('\n\033[1mWould you also like to change your last name? {Y/N}: \033[0m')
            time.sleep(0.5)
            affirm = input('\t\033[1m>>> \033[0m').upper()
            if affirm == 'Y':
                time.sleep(1.5)
                new_last_name = input('\n\033[1mEnter your new last name: \033[0m').capitalize()
                time.sleep(1.5)
                insert_new_last_name_query = "UPDATE bank_tbl SET last_name = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(insert_new_last_name_query, (new_last_name, user_name, pin))
                txf.print_with_delay('changing...')
                time.sleep(2)
                print('\n\t\t\033[3m last name updated successfully\033[0m')
                user_name_ = new_first_name.upper() + new_last_name.upper()
                new_user_name = conf_user_name(user_name_)
                time.sleep(0.5)
                print(f'\n\t\t\033[3mNew user name: \033[1m{new_user_name}\033[0m\033[0m')
                update_user_name_query = "UPDATE bank_tbl SET user_name = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(update_user_name_query, (new_user_name, user_name, pin))
                conn_obj.commit()
            elif affirm == 'N':

                get_last_name_query = "SELECT last_name FROM bank_tbl WHERE user_name = %s AND PIN = %s"
                my_cur.execute(get_last_name_query, (user_name, pin))
                last_name = my_cur.fetchone()
                last_name = last_name[0]

                user_name_ = new_first_name.upper() + str(last_name).upper()
                new_user_name = conf_user_name(user_name_)
                time.sleep(2)
                print(f'\n\t\t\033[3mNew user name: \033[1m{new_user_name}\033[0m\033[0m')
                update_user_name_query = "UPDATE bank_tbl SET user_name = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(update_user_name_query, (new_user_name, user_name, pin))
                conn_obj.commit()
            else:
                time.sleep(1)
                print('\n\t\033[31mInvalid input. please try again.\033[0m')
        elif inp == '2':
            time.sleep(1.5)
            new_last_name = input('\n\t\033[1mEnter your new last name: \033[0m').capitalize()
            time.sleep(2)
            insert_new_last_name_query = "UPDATE bank_tbl SET last_name = %s WHERE user_name = %s AND PIN = %s"
            my_cur.execute(insert_new_last_name_query, (new_last_name, user_name, pin))
            txf.print_with_delay('changing...')
            time.sleep(2)
            print('\n\t\t\033[3mLast name updated successfully\033[0m')
            time.sleep(1.5)
            print('\n\t\033[1mWould you also like to change your first name? [Y/N]?: \033[0m')
            time.sleep(0.5)
            affirm = input('\t\033[1m : \033[0m').upper()
            time.sleep(2)
            if affirm == 'Y':
                new_first_name = input('\n\t\033[1mEnter your new first name: \033[0m').capitalize()
                time.sleep(2)
                insert_new_first_name_query = "UPDATE bank_tbl SET first_name = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(insert_new_first_name_query, (new_first_name, user_name, pin))
                txf.print_with_delay('changing...')
                time.sleep(2)
                print('\n\t\t\033[3mFirst name updated successfully\033[0m')
                time.sleep(1.5)
                user_name_ = new_first_name.upper() + new_last_name.upper()
                new_user_name = conf_user_name(user_name_)
                print(f'\t\t\033[3mNew user name: \033[1m{new_user_name}\033[0m\033[0m')
                update_user_name_query = "UPDATE bank_tbl SET user_name = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(update_user_name_query, (new_user_name, user_name, pin))
                conn_obj.commit()
            elif affirm == 'N':
                get_first_name_query = "SELECT first_name FROM bank_tbl WHERE user_name = %s AND PIN = %s"
                my_cur.execute(get_first_name_query, (user_name, pin))
                first_name = my_cur.fetchone()
                first_name = first_name[0]
                time.sleep(1)
                user_name_ = first_name.upper() + str(new_last_name).upper()
                new_user_name = conf_user_name(user_name_)
                print(f'\t\t\033[3mNew user name: \033[1m{new_user_name}\033[0m\033[0m')
                update_user_name_query = "UPDATE bank_tbl SET user_name = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(update_user_name_query, (new_user_name, user_name, pin))
                conn_obj.commit()
        elif inp == '3':
            time.sleep(2)
            print('\n\033[1mEnter your new Phone number\033[0m')
            time.sleep(0.5)
            new_phone_number = input('\033[1m>>> \033[0m')

            if new_phone_number.isdigit():
                if len(new_phone_number) == 11:
                    new_phone = str(new_phone_number)
                    update_pin_query = "UPDATE bank_tbl SET phone_num = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_pin_query, (new_phone, user_name, pin))
                    conn_obj.commit()
                    time.sleep(2)
                    txf.print_with_delay('changing...')
                    time.sleep(2)
                    print('\n\t\t\t\033[3mPhone number updated successfully\033[0m')
                else:
                    time.sleep(1)
                    print('\n\t\t\t\033[31mNew phone number has to be 11 digits\033[0m')
            else:
                time.sleep(1)
                print('\n\t\t\033[31mNew phone number is not digits\033[0m')
        elif inp == '4':
            time.sleep(2)
            print('\n\t\033[1mEnter your new PIN\033[0m')
            time.sleep(0.5)
            new_pin_digit = input('\t\t\033[1m : \033[0m')

            if new_pin_digit.isdigit():
                if len(new_pin_digit) == 5:
                    new_pin = str(new_pin_digit)
                    update_pin_query = "UPDATE bank_tbl SET PIN = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_pin_query, (new_pin, user_name, pin))
                    conn_obj.commit()
                    time.sleep(2)
                    txf.print_with_delay('changing...')
                    time.sleep(2)
                    print('\n\t\t\t\033[3mPIN updated successfully\033[0m')
                else:
                    time.sleep(1)
                    print('\n\t\t\t\033[31mNew PIN has to be 5 digits\033[0m')
            else:
                time.sleep(1)
                print('\n\t\t\033[31mNew PIN is not digits\033[0m')
        elif inp == '5':
            time.sleep(2)
            print('\n\t\033[1mEnter your new Transaction PIN\033[0m')
            time.sleep(0.5)
            new_pin_digit = input('\t\t\033[1m : \033[0m')

            if new_pin_digit.isdigit():
                if len(new_pin_digit) == 4:
                    new_pin = str(new_pin_digit)
                    update_pin_query = "UPDATE bank_tbl SET transaction_pin = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_pin_query, (new_pin, user_name, pin))
                    conn_obj.commit()
                    time.sleep(2)
                    txf.print_with_delay('changing...')
                    time.sleep(2)
                    print('\n\t\t\t\033[3mTransaction PIN updated successfully\033[0m')
                else:
                    time.sleep(1)
                    print('\n\t\t\t\033[31mNew PIN has to be 5 digits\033[0m')
            else:
                time.sleep(1)
                print('\n\t\t\033[31mNew PIN is not digits\033[0m')
        elif inp == '6':
            time.sleep(1.5)
            txf.print_with_delay(txf.italic() + '\n\tExiting...' + txf.end())
            time.sleep(1)
            loggedinmenu.logged_in_menu()
        else:
            time.sleep(1)
            print('\n\t\033[31mInvalid input. please try again\033[0m.')
    except Exception as e:
        print(f'Error: {e}')
