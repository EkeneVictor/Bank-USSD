import time
import pymysql as sql
import textformatting as txf
import string
import random
from datetime import datetime
from create_acct import check_restrictions, check_withdrawable_amount

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
    # Simulate some delay to enhance user experience
    time.sleep(2)

    # Prompt user to enter the amount to deposit and convert it to float
    amount = float(input('\n\033[1mEnter amount to deposit: \033[0m'))

    # Prompt user to enter the transaction PIN
    trans_pin_input = input('Enter your transaction PIN: ')

    # Query to check if the user exists and get the transaction pin and account type
    check_pin_query = "SELECT transaction_pin, acct_type FROM bank_tbl WHERE user_name = %s and PIN = %s"
    my_cur.execute(check_pin_query, (user_name, pin))
    result = my_cur.fetchone()

    if result:
        trans_pin, acct_type = result

        # Check if the entered transaction pin matches the stored one
        if trans_pin_input == trans_pin:

            # Check any restrictions before proceeding with the deposit
            status, message = check_restrictions(acct_type, 'deposit', amount)
            if not status:
                time.sleep(2)
                txf.display_error(message)
                return

            # Calculate the charges and the actual deposit amount
            charges = 0.015 * amount
            amount_dep = amount - charges

            # Retrieve the admin account balance
            acct_type = 'Admin'
            select_admin_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE acct_type = %s"
            my_cur.execute(select_admin_acc_bal, (acct_type,))
            current_balance = my_cur.fetchone()

            if current_balance:
                current_balance = current_balance[0]
                current_balance = current_balance - amount_dep
                new_balance = current_balance

                # Ensure the admin account has enough balance to cover the deposit
                if new_balance >= 0:
                    # Update the admin's account balance
                    update_admin_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE acct_type = %s"
                    my_cur.execute(update_admin_acct_bal, (new_balance, acct_type))

            # Retrieve the current balance of the user's account
            select_acc_bal = "SELECT acct_bal FROM bank_tbl WHERE user_name = %s AND PIN = %s"
            my_cur.execute(select_acc_bal, (user_name, pin))
            current_balance = my_cur.fetchone()
            time.sleep(4)

            if current_balance:
                current_balance = current_balance[0]
                new_balance = current_balance + amount_dep

                # Ensure the new balance is non-negative
                if new_balance >= 0:
                    # Update the user's account balance
                    update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                    my_cur.execute(update_acct_bal, (new_balance, user_name, pin))

                    txf.print_with_delay('..........')
                    time.sleep(2)

                    print(
                        f"\n\033[1mDeposit successful\033[0m.\n\t\033[1m Your new balance is: \033[32m${new_balance:,}\033[0m. (\033[31m-${charges}\033[0m for charges)\033[0m")

                    # Retrieve the user's account number
                    select_deposit_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                    my_cur.execute(select_deposit_acct_num, (user_name, pin))
                    deposit_acct = my_cur.fetchone()
                    deposit_acct = str(deposit_acct[0])

                    # Generate a unique transaction ID
                    def gen_transaction_id():
                        letters = string.ascii_letters.upper() + string.digits
                        return ''.join(random.choices(letters, k=22))

                    transaction_id = gen_transaction_id()

                    # Log the deposit statement to a file
                    with open('deposit_statements.txt', 'a') as deps:
                        deps.write(
                            f'Acct: ****{deposit_acct[-4:]}\nDEP:${amount_dep:,}\nTRANSACTION ID:{transaction_id}\nDesc:DEPOSIT OF {amount_dep}:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                    trans_amount = amount_dep
                    sender_acct_num = 'DEPOSIT'
                    reciever_acct_num = deposit_acct

                    sender_user_name = 'DEPOSIT'
                    reciever_user_name = user_name

                    trans_date = datetime.now()
                    trans_desc = f'DEPOSIT OF ${amount_dep}'
                    trans_status = 'Successful'

                    sender_acct_type = 'DEPOSIT'
                    reciever_acct_type = 'DEPOSIT'

                    # Update the recipient's balance in the accounts table
                    update_accounts_query = "UPDATE accounts SET balance = balance + %s WHERE user_name = %s and account_type = %s"
                    my_cur.execute(update_accounts_query, (amount_dep, reciever_user_name, reciever_acct_type))

                    # Log the transaction in the transactions table
                    update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                    my_cur.execute(update_trans_table, (
                        transaction_id, trans_amount, sender_acct_num, reciever_acct_num, sender_user_name,
                        reciever_user_name, trans_date, trans_desc, sender_acct_type, reciever_acct_type, trans_status))

                    # Commit the transaction to the database
                    conn_obj.commit()
                else:
                    print('\n\033[31mYou cannot deposit a negative amount\033[0m')
            else:
                print("\033[31mAccount not found.\033[0m")
        else:
            time.sleep(2)
            txf.display_error('Invalid transaction PIN')
    else:
        txf.display_error('Invalid PIN')
    time.sleep(2)
