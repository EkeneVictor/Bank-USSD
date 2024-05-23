import time
import pymysql as sql
import textformatting as txf
import string
import random
from datetime import datetime

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


def log_transaction(transaction_id, amount, sender_user_name, recipient_user_name, description):
    try:
        with open('transfer_statements.txt', 'a') as trans_statements:
            trans_statements.write(f'Transaction ID: {transaction_id}\n')
            trans_statements.write(f'Sender: {sender_user_name}\n')
            trans_statements.write(f'Recipient: {recipient_user_name}\n')
            trans_statements.write(f'Amount: ${amount}\n')
            trans_statements.write(f'Description: {description}\n')
            trans_statements.write(f'Date/Time: {datetime.now()}\n')
            trans_statements.write('--------------------------------------------\n')
    except Exception as e:
        print(f"An error occurred while logging transaction: {e}")


def log_transaction_failed(sender_user_name, recipient_account, amount, description, reason):
    try:
        with open('transfer_statements.txt', 'a') as trans_statements:
            trans_statements.write(f'Sender: {sender_user_name}\n')
            trans_statements.write(f'Recipient Account: {recipient_account}\n')
            trans_statements.write(f'Amount: ${amount}\n')
            trans_statements.write(f'Description: {description}\n')
            trans_statements.write(f'Reason for Failure: {reason}\n')
            trans_statements.write(f'Date/Time: {datetime.now()}\n')
            trans_statements.write('--------------------------------------------\n')
    except Exception as e:
        print(f"An error occurred while logging transaction failure: {e}")


def transfer_money(user_name, pin, recipient_account, amount, description):
    try:
        time.sleep(2)

        # Retrieve sender's account details
        sender_user_name = user_name

        # Check if recipient's account exists and is active
        bring_recipient_name = "SELECT * FROM bank_tbl WHERE acct_num = %s"
        my_cur.execute(bring_recipient_name, (recipient_account,))
        reciever = my_cur.fetchone()

        select_sender_acct = "SELECT acct_bal FROM bank_tbl WHERE user_name = %s AND PIN = %s"
        my_cur.execute(select_sender_acct, (sender_user_name, pin))
        sender_balance = my_cur.fetchone()[0]
        if sender_balance:
            if sender_balance >= amount:
                if reciever and reciever[9] == 'Active':
                    # Calculate charges
                    charges = 0.015 * amount
                    amount_tr = amount + charges
                    amount_rec = amount

                    # Update the Admin account balance directly in the database
                    update_admin_acct_bal = "UPDATE bank_tbl SET acct_bal = acct_bal + %s WHERE acct_type = 'Admin'"
                    my_cur.execute(update_admin_acct_bal, (charges,))
                    conn_obj.commit()

                    # Update sender's account balance
                    update_sender_acct = "UPDATE bank_tbl SET acct_bal = acct_bal - %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_sender_acct, (amount_tr, sender_user_name, pin))

                    # Update recipient's account balance
                    update_recipient_acct = "UPDATE bank_tbl SET acct_bal = acct_bal + %s WHERE acct_num = %s"
                    my_cur.execute(update_recipient_acct, (amount_rec, recipient_account))

                    confirm = input(
                        f"\n\033[1mYou are about to transfer ${amount} to {reciever[4]} (-${charges} for charges).\n Proceed with Transfer?[Y/N]: \033[0m").upper()
                    if confirm == 'Y':

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

                        # # Log transaction details

                        log_transaction(transaction_id, amount_tr, sender_user_name, reciever[4], description)
                        txf.print_with_delay('.......')
                        time.sleep(2)
                        print(
                            f"\n\033[1mTransfer successful.\033[0m\n \033[1m{sender_user_name}, You have transferred \033[32m${amount}\033[0m to {reciever[4]}\033[0m ")
                        # Get sender's account type
                        sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                        my_cur.execute(sender_acct_type_query, (sender_user_name,))
                        sender_acct_type = my_cur.fetchone()[0]

                        select_sender_acct = "SELECT acct_num FROM bank_tbl WHERE user_name = %s"
                        my_cur.execute(select_sender_acct, sender_user_name)
                        sender_acct = my_cur.fetchone()[0]

                        # Get recipient's account type
                        reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                        my_cur.execute(reciever_acct_type_query, (recipient_account,))
                        reciever_acct_type = my_cur.fetchone()[0]

                        # Insert transaction record directly into the database
                        update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                        my_cur.execute(update_trans_table, (
                            transaction_id, amount_tr, sender_acct, recipient_account, sender_user_name,
                            reciever[4], datetime.now(), description, sender_acct_type,
                            reciever_acct_type, 'Successful'))
                        conn_obj.commit()

                    else:
                        print('\n\033[31mYou have cancelled the transfer\033[0m')

                elif reciever and reciever[11] == 'Suspended':
                    charges = 0.015 * amount
                    amount_tr = amount - charges
                    description = description + ": [RECIPIENT ACCOUNT SUSPENDED]"

                    print(f"\n\t\033[33m{reciever[4]}'s account is Suspended.\n\t\tTransaction can not be made.\033[0m")
                    log_transaction_failed(user_name, recipient_account, amount_tr, description,
                                           "[RECIPIENT ACCOUNT SUSPENDED]")

                    # Get sender's account type
                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()[0]

                    select_sender_acct = "SELECT acct_num FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(select_sender_acct, sender_user_name)
                    sender_acct = my_cur.fetchone()[0]

                    # Get recipient's account type
                    reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    reciever_acct_type = my_cur.fetchone()[0]

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

                    # Insert transaction record directly into the database
                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, amount_tr, sender_acct, recipient_account, sender_user_name,
                        reciever[4], datetime.now(), description, sender_acct_type,
                        reciever_acct_type, 'Failed'))
                    conn_obj.commit()
                elif reciever and reciever[11] == 'Blocked':

                    charges = 0.015 * amount
                    amount_tr = amount - charges
                    description = description + ": [RECIPIENT ACCOUNT BLOCKED]"

                    print(f"\n\t\033[31m{reciever[4]}'s account is blocked.\n\t\tTransaction can not be made.\033[0m")
                    log_transaction_failed(user_name, recipient_account, amount, description, "[RECIPIENT ACCOUNT BLOCKED]")

                    # Get sender's account type
                    sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(sender_acct_type_query, (sender_user_name,))
                    sender_acct_type = my_cur.fetchone()[0]

                    select_sender_acct = "SELECT acct_num FROM bank_tbl WHERE user_name = %s"
                    my_cur.execute(select_sender_acct, sender_user_name)
                    sender_acct = my_cur.fetchone()[0]

                    # Get recipient's account type
                    reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                    my_cur.execute(reciever_acct_type_query, (recipient_account,))
                    reciever_acct_type = my_cur.fetchone()[0]

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

                    # Insert transaction record directly into the database
                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, amount_tr, sender_acct, recipient_account, sender_user_name,
                        reciever[4], datetime.now(), description, sender_acct_type,
                        reciever_acct_type, 'Failed'))
                    conn_obj.commit()

                else:
                    print("\n\033[31mRecipient account not found.\033[0m")
            else:
                print("\n\033[31mInsufficient balance.\033[0m")
        else:
            print("\n\033[31mSender account not found.\033[0m")

    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(2)
