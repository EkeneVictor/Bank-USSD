import time
import pymysql as sql
import textformatting as txf
import string
import random
from datetime import datetime
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


def pay_water_bill(user_name, pin):
    txf.print_with_delay(txf.italic() + '\tfetching details...' + txf.end())
    time.sleep(2)
    bills = [200, 250, 100, 150, 50, 400, 500, 450, 550, 600, 560, 650, 300, 320, 350, 1050, 1500, 1120]
    bill = random.choice(bills)
    print(f"\n\tYour outstanding bill amount for water is ${bill:,}.")
    confirm = input(f"\n\tDo you want to proceed with the payment [Y/N] ?:  ").upper()

    if confirm == 'Y':

        charges = 0.015 * bill
        amount_paid = bill + charges

        # Check withdrawable amount
        can_withdraw, message = check_withdrawable_amount(user_name, pin, amount_paid)
        if not can_withdraw:
            txf.display_error(message)
            return

        acct_type = 'Admin'
        select_admin_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE acct_type = %s"
        my_cur.execute(select_admin_acc_bal, (acct_type,))
        current_balance = my_cur.fetchone()
        if current_balance:
            current_balance = current_balance[0]
            current_balance = current_balance
            new_balance = current_balance + charges
            if new_balance >= 0:
                # Update the user's account balance in the database with the new balance
                update_admin_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE acct_type = %s"
                my_cur.execute(update_admin_acct_bal, (new_balance, acct_type))
                conn_obj.commit()
            else:
                print('\n\033[31mError....\033[0m')

        # Query the database to retrieve the current balance of the user's account
        select_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(select_acc_bal, (user_name, pin))
        current_balance = my_cur.fetchone()
        time.sleep(4)
        try:
            if current_balance:
                current_balance = current_balance[0]
                if current_balance >= bill:
                    # Update the user's account balance in the database with the new balance
                    new_balance = current_balance - amount_paid
                    update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_balance, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[Payment successful. \n\tYou have paid \033[32m${bill:,}\033[0m for water (\033[31m-${charges}\033[0m for charges). Your new balance is \033[32m${new_balance:,}\033[0m\033[0m")

                    select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                    my_cur.execute(select_withdrawal_acct_num, (user_name, pin))
                    withdrawal_acct = my_cur.fetchone()
                    withdrawal_acct = str(withdrawal_acct[0])

                    transaction_id = gen_transaction_id()
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount_paid:,}  (-${charges} charges)\nTRANSACTION ID:{transaction_id}\nDesc:PAYMENT OF ${bill:,} FOR WATER:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = bill
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = 'STATE WATERS'

                    sender_user_name = user_name
                    reciever_user_name = 'STATE WATERS'

                    trans_date = datetime.now()
                    trans_desc = f'PAYMENT OF ${bill} FOR WATERS'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = 'STATE WATERS'

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num, sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type, reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient balance for payment.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'error : {e}')

    elif confirm == 'N':
        time.sleep(1.5)
        print('You have cancelled the payment')
    else:
        time.sleep(2)
        print('Invalid Input')
