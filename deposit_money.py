import time
import pymysql as sql
import textformatting as txf
import string
import random
from datetime import datetime
from create_acct import handle_transaction, check_restrictions

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def deposit_money(user_name, pin):
    # user_data = retr.retr_user_data(user_name, pin)
    time.sleep(2)
    # user_name = str(input('Enter your User name: ')).upper()
    # time.sleep(1.5)
    # pin = str(input('Enter your PIN: '))
    # time.sleep(1.5)
    amount = float(input('\n\033[1mEnter amount to deposit: \033[0m'))
    trans_pin_input = input('Enter your transaction PIN: ')

    check_pin_query = "SELECT transaction_pin, acct_type FROM bank_tbl WHERE user_name = %s and PIN = %s"
    my_cur.execute(check_pin_query, (user_name, pin))
    result = my_cur.fetchone()
    if result:
        trans_pin, acct_type = result
        if trans_pin_input == trans_pin:
            # Check the restrictions before proceeding
            status, message = check_restrictions(acct_type, 'deposit', amount)
            if not status:
                print(message)
                return
        charges = 0.015 * amount
        amount_dep = amount - charges

        acct_type = 'Admin'
        select_admin_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE acct_type = %s"
        my_cur.execute(select_admin_acc_bal, (acct_type,))
        current_balance = my_cur.fetchone()
        if current_balance:
            current_balance = current_balance[0]
            current_balance = current_balance - amount_dep
            new_balance = current_balance
            if new_balance >= 0:
                # Update the user's account balance in the database with the new balance
                update_admin_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE acct_type = %s"
                my_cur.execute(update_admin_acct_bal, (new_balance, acct_type))

        # Query the database to retrieve the current balance of the user's account
        select_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE user_name = %s AND PIN = %s "
        my_cur.execute(select_acc_bal, (user_name, pin))
        current_balance = my_cur.fetchone()
        time.sleep(4)
        if current_balance:
            current_balance = current_balance[0]
            new_balance = current_balance + amount_dep
            if new_balance >= 0:
                # Update the user's account balance in the database with the new balance
                update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                my_cur.execute(update_acct_bal, (new_balance, user_name, pin))
                txf.print_with_delay('..........')
                time.sleep(2)
                print(
                    f"\n\033[1mDeposit successful\033[0m.\n\t\033[1m Your new balance is: \033[32m${new_balance}\033[0m. (\033[31m-${charges}\033[0m for charges)\033[0m")

                select_deposit_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                my_cur.execute(select_deposit_acct_num, (user_name, pin))
                deposit_acct = my_cur.fetchone()
                deposit_acct = str(deposit_acct[0])

                def gen_transaction_id():
                    letters = string.ascii_letters.upper() + string.digits
                    letters_list = list(letters)
                    trr = []
                    for _ in letters_list:
                        scrambled = ''.join(random.choices(letters_list))
                        transaction_id_all = ''.join(scrambled)
                        transaction_ids = transaction_id_all[0:22]
                        trr.append(transaction_ids)
                    transaction_id = ''.join(trr[:23])
                    return transaction_id

                transaction_id = gen_transaction_id()
                with open('deposit_statements.txt', 'a') as deps:
                    deps.write(
                        f'Acct: ****{deposit_acct[-4:]}\nDEP:${amount_dep}\nTRANSACTION ID:{transaction_id}\nDesc:DEPOSIT OF {amount_dep}:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                trans_amount = amount_dep
                sender_acct_num = 'DEPOSIT'
                reciever_acct_num = deposit_acct

                sender_user_name = 'DEPOSIT'
                reciever_user_name = user_name

                trans_date = datetime.now()
                trans_desc = f'DEPOSIT OF ${amount_dep}'
                trans_status = 'Successful'

                # sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                # my_cur.execute(sender_acct_type_query, (sender_user_name,))
                # sender_acct_type = my_cur.fetchone()
                sender_acct_type = 'DEPOSIT'

                # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                # reciever_acct_type = my_cur.fetchone()
                reciever_acct_type = 'DEPOSIT'

                # Update sender acounts table
                update_accounts_query = "UPDATE accounts SET balance = balance + %s WHERE user_name = %s and account_type = %s"
                my_cur.execute(update_accounts_query, (amount_dep, reciever_user_name, reciever_acct_type))

                update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                my_cur.execute(update_trans_table, (
                    transaction_id, trans_amount, sender_acct_num, reciever_acct_num, sender_user_name,
                    reciever_user_name, trans_date, trans_desc, sender_acct_type, reciever_acct_type, trans_status))

                handle_transaction(acct_type, 'deposit', amount)

                conn_obj.commit()

            else:
                print('\n\033[31mYou cannot deposit a negative amount\033[0m')
        else:
            print("\033[31mAccount not found.\033[0m")
    else:
        txf.display_error('Invalid PIN')
    time.sleep(2)
