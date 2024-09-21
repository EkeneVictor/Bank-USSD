import time
import pymysql as sql
import backs
import textformatting as txf
import string
import random
from datetime import datetime
import config
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


def mobile_top_up_menu():
    time.sleep(2)
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1m+--------------------+-----------------+-----------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t|  Top - up  Menu                                  |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+--------------------+-----------------+-----------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1. Mobile  Top-up  | 2. Data Bundles | 3.  Exit  |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+--------------------+-----------------+-----------+\n")

    select = input('Select an option for top-up: ')

    if select == '1':
        mobile_top_up(config.user_name, config.pin_)
        backs.back_to_top_up_menu()

    elif select == '2':
        data_bundles(config.user_name, config.pin_)

    elif select == '3':
        backs.back_to_bill_payment_menu()
    else:
        txf.display_error('Invalid input')


def mobile_top_up(user_name, pin):
    try:
        time.sleep(1.5)
        amount = float(input('Enter the top-up amount: '))
        charges = 0.015 * amount
        amount_paid = amount + charges

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
                if current_balance >= amount_paid:
                    # Update the user's account balance in the database with the new balance
                    new_balance = current_balance - amount_paid
                    update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (amount, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for airtime top-up (\033[31m-${charges}\033[0m for charges). Your new balance is \033[32m${new_balance}\033[0m\033[0m")

                    select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                    my_cur.execute(select_withdrawal_acct_num, (user_name, pin))
                    withdrawal_acct = my_cur.fetchone()
                    withdrawal_acct = str(withdrawal_acct[0])

                    transaction_id = gen_transaction_id()
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount_paid}  (-${format(charges, ".2f")} charges)\nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF {amount} FOR AIRTIME:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR AIRTIME'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient balance for payment.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'error: {e}')
    except Exception as e:
        print(f'error: {e}')

        backs.back_to_top_up_menu()


def data_bundles(user_name, pin):
    time.sleep(1)
    print('\n\t\t1. $100 for 200MB')
    print('\t\t2. $150 for 300MB')
    print('\t\t3. $300 for 750MB')
    print('\t\t4. $500 for 1GB')
    print('\t\t5. $800 for 2GB')
    print('\t\t6. $1200 for 3GB')
    print('\t\t7.  Exit')
    opt = input('\n : ')

    if opt == '1':
        amount = 100
        data = 200

        # Query the database to retrieve the current balance of the user's account
        airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(airtime_time_bal_sel, (user_name, pin))
        air_time_bal = my_cur.fetchone()
        time.sleep(2)
        try:
            if air_time_bal:
                air_time_bal = air_time_bal[0]
                if air_time_bal >= amount:
                    # Update the user's account balance in the database with the new balance
                    new_airtime_balance = air_time_bal - amount
                    update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (data, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

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
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount} \nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient airtime balance.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'erRor: {e}')
    elif opt == '2':

        amount = 150
        data = 300

        # Query the database to retrieve the current balance of the user's account
        airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(airtime_time_bal_sel, (user_name, pin))
        air_time_bal = my_cur.fetchone()
        time.sleep(2)
        try:
            if air_time_bal:
                air_time_bal = air_time_bal[0]
                if air_time_bal >= amount:
                    # Update the user's account balance in the database with the new balance
                    new_airtime_balance = air_time_bal - amount
                    update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (data, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

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
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount} \nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient airtime balance.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'erRor: {e}')
    elif opt == '3':

        amount = 300
        data = 750

        # Query the database to retrieve the current balance of the user's account
        airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(airtime_time_bal_sel, (user_name, pin))
        air_time_bal = my_cur.fetchone()
        time.sleep(2)
        try:
            if air_time_bal:
                air_time_bal = air_time_bal[0]
                if air_time_bal >= amount:
                    # Update the user's account balance in the database with the new balance
                    new_airtime_balance = air_time_bal - amount
                    update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (data, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

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
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount} \nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient airtime balance.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'erRor: {e}')
    elif opt == '4':

        amount = 500
        data = 1024

        # Query the database to retrieve the current balance of the user's account
        airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(airtime_time_bal_sel, (user_name, pin))
        air_time_bal = my_cur.fetchone()
        time.sleep(2)
        try:
            if air_time_bal:
                air_time_bal = air_time_bal[0]
                if air_time_bal >= amount:
                    # Update the user's account balance in the database with the new balance
                    new_airtime_balance = air_time_bal - amount
                    update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (data, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

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
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount} \nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient airtime balance.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'erRor: {e}')
    elif opt == '5':

        amount = 800
        data = 2048

        # Query the database to retrieve the current balance of the user's account
        airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(airtime_time_bal_sel, (user_name, pin))
        air_time_bal = my_cur.fetchone()
        time.sleep(2)
        try:
            if air_time_bal:
                air_time_bal = air_time_bal[0]
                if air_time_bal >= amount:
                    # Update the user's account balance in the database with the new balance
                    new_airtime_balance = air_time_bal - amount
                    update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (data, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

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
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount} \nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient airtime balance.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'erRor: {e}')
    elif opt == '6':

        amount = 1200
        data = 5042

        # Query the database to retrieve the current balance of the user's account
        airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(airtime_time_bal_sel, (user_name, pin))
        air_time_bal = my_cur.fetchone()
        time.sleep(2)
        try:
            if air_time_bal:
                air_time_bal = air_time_bal[0]
                if air_time_bal >= amount:
                    # Update the user's account balance in the database with the new balance
                    new_airtime_balance = air_time_bal - amount
                    update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin))
                    conn_obj.commit()

                    update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_airtime_bal, (data, user_name, pin))
                    conn_obj.commit()

                    print(
                        f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

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
                    with open('bill_payments.txt', 'a') as bill_payments:
                        bill_payments.write(
                            f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount} \nTRANSACTION ID:{transaction_id}\nDesc:TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount
                    sender_acct_num = withdrawal_acct
                    reciever_acct_num = random.choice(('MTN', 'GLO', 'AIRTEL', '9MOBILE', 'NTEL'))

                    sender_user_name = user_name
                    reciever_user_name = reciever_acct_num

                    trans_date = datetime.now()
                    trans_desc = f'TOP-UP OF ${amount} FOR {data}MB DATA BUNDLE'
                    trans_status = 'Successful'

                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()

                    # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    # reciever_acct_type = my_cur.fetchone()
                    reciever_acct_type = reciever_user_name

                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num,
                        sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type,
                        reciever_acct_type,
                        trans_status))
                    conn_obj.commit()
                else:
                    print("Insufficient airtime balance.")
            else:
                print('Account not found')
        except Exception as e:
            print(f'erRor: {e}')
    elif opt == '7':
        time.sleep(2)
        mobile_top_up_menu()
    else:
        print('Invalid Input')

    backs.back_to_top_up_menu()
