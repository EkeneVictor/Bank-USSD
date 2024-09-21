import time
import pymysql as sql
import textformatting as txf
import string
import random
from datetime import datetime
from create_acct import check_restrictions
from create_acct import check_withdrawable_amount

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def withdraw_money(user_name, pin):
    try:
        time.sleep(2)
        amount = float(input('\n\033[1mEnter amount to withdraw: \033[0m'))
        trans_pin_input = input('Enter your transaction PIN: ')
        check_pin_query = "SELECT transaction_pin, acct_type FROM bank_tbl WHERE user_name = %s and PIN = %s"
        my_cur.execute(check_pin_query, (user_name, pin))
        result = my_cur.fetchone()
        if result:
            trans_pin, acct_type = result
            if trans_pin_input == trans_pin:
                # Check the restrictions before proceeding
                status, message = check_restrictions(acct_type, 'withdrawal', amount)
                if not status:
                    txf.display_error(message)
                    return

                # Check withdrawable amount
                can_withdraw, message = check_withdrawable_amount(user_name, pin, amount)
                if not can_withdraw:
                    return txf.display_error(message)

                charges = 0.015 * amount
                amount_bnk = amount + charges
                amount_wtd = amount + charges

                # Update the Admin account balance directly in the database
                update_admin_acct_bal = "UPDATE bank_tbl SET acct_bal = acct_bal + %s WHERE acct_type = 'Admin'"
                my_cur.execute(update_admin_acct_bal, (amount_bnk,))
                conn_obj.commit()

                # Query the database to retrieve the current balance of the user's account
                select_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE user_name = %s AND PIN = %s"
                my_cur.execute(select_acc_bal, (user_name, pin))
                current_balance = my_cur.fetchone()
                time.sleep(4)
                if current_balance:
                    current_balance = current_balance[0]
                    if current_balance >= amount:
                        # Update the user's account balance in the database with the new balance
                        new_balance = current_balance - amount_wtd
                        update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                        my_cur.execute(update_acct_bal, (new_balance, user_name, pin))
                        conn_obj.commit()
                        txf.print_with_delay('......')
                        time.sleep(2)

                        print(
                            f"\n\t\033[1mWithdraw successful. You have withdrawn \033[32m${amount:,}\033[0m (\033[31m-${charges}\033[0m for charges). Your new balance is \033[32m${new_balance}\033[0m\033[0m")

                        select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                        my_cur.execute(select_withdrawal_acct_num, (user_name, pin))
                        withdrawal_acct = my_cur.fetchone()
                        withdrawal_acct = str(withdrawal_acct[0])

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
                        with open('withdraw__statements.txt', 'a') as withdraw_statements:
                            withdraw_statements.write(
                                f'Acct: ****{withdrawal_acct[-4:]}\nWTH:${amount_wtd:,}\nTRANSACTION ID:{transaction_id}\nDesc:WITHDRAWAL OF {amount_wtd:,}:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                        trans_amount = amount_wtd
                        sender_acct_num = withdrawal_acct
                        reciever_acct_num = 'WITHDRAWAL'

                        sender_user_name = user_name
                        reciever_user_name = 'WITHDRAWAL'

                        trans_date = datetime.now()
                        trans_desc = f'WITHDRAWAL OF ${amount_wtd}'
                        trans_status = 'Successful'

                        sender_acct_type = 'WITHDRAWAL'
                        reciever_acct_type = 'WITHDRAWAL'

                        # Update sender accounts table
                        update_accounts_query = "UPDATE accounts SET balance = balance - %s WHERE user_name = %s and account_type = %s"
                        my_cur.execute(update_accounts_query, (amount, user_name, sender_acct_type))
                        conn_obj.commit()

                        # Insert transaction record directly into the database
                        update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                        my_cur.execute(update_trans_table, (
                            transaction_id, trans_amount, sender_acct_num, reciever_acct_num, sender_user_name,
                            reciever_user_name, trans_date, trans_desc, sender_acct_type, reciever_acct_type, trans_status))
                        conn_obj.commit()
                    else:
                        txf.display_error("Insufficient balance for withdrawal.")
                else:
                    txf.display_error('Account not found')
                time.sleep(2)
            else:
                txf.display_error('Invalid Transaction PIN')
        else:
            txf.display_error('Invalid Username or PIN')
    except Exception as e:
        print(f"An error occurred: {e}")
