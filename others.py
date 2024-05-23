











def bills_payment_menu():
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+---------------+------------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| Bills Payment Menu                                      |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+---------------+------------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1. Electricity Bill  | 2. Water Bill | 3. Mobile Top-up |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+---------------+------------------+\n")

    option = input("Select an utility: \033[0m")
    time.sleep(2)

    def pay_electricity_bill():
        print("\t\t\033[3mf", end='')
        time.sleep(0.255)
        print('e', end='')
        time.sleep(0.255)
        print('t', end='')
        time.sleep(0.255)
        print('c', end='')
        time.sleep(0.255)
        print('h', end='')
        time.sleep(0.255)
        print('i', end='')
        time.sleep(0.255)
        print('n', end='')
        time.sleep(0.255)
        print('g', end='')
        time.sleep(0.255)
        print(" ", end='')
        time.sleep(0.255)
        print('d', end='')
        time.sleep(0.255)
        print('e', end='')
        time.sleep(0.255)
        print('t', end='')
        time.sleep(0.255)
        print('a', end='')
        time.sleep(0.255)
        print('i', end='')
        time.sleep(0.255)
        print('l', end='')
        time.sleep(0.255)
        print('s', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(2)
        print('.', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(0.255)
        print('.\033[0m', end='')
        time.sleep(2)
        bills = [200, 250, 230, 430, 480, 520, 100, 150, 50, 400, 500, 450, 550, 600, 560, 650, 300, 320, 350,
                 1050, 1500, 1120]
        bill = random.choice(bills)
        print(f"\n\tYour outstanding bill amount for electricity is ${bill}.")
        confirm = input(f"\n\tDo you want to proceed with the payment [Y/N] ?:  ").upper()

        if confirm == 'Y':
            charges = 0.015 * bill
            amount = bill
            amount_paid = bill + charges

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
            my_cur.execute(select_acc_bal, (user_name, pin_))
            current_balance = my_cur.fetchone()
            time.sleep(4)
            try:
                if current_balance:
                    current_balance = current_balance[0]
                    if current_balance >= bill:
                        # Update the user's account balance in the database with the new balance
                        new_balance = current_balance - amount_paid
                        update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                        my_cur.execute(update_acct_bal, (new_balance, user_name, pin_))
                        conn_obj.commit()

                        print(
                            f"\n\t\033[Payment successful. \n\tYou have paid \033[32m${bill}\033[0m for electricity (\033[31m-${charges}\033[0m for charges). Your new balance is \033[32m${new_balance}\033[0m\033[0m")

                        select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                        my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                        withdrawal_acct = my_cur.fetchone()
                        withdrawal_acct = str(withdrawal_acct[0])

                        def gen_transaction_id():
                            letters = string.ascii_letters.upper() + string.digits
                            letters_list = list(letters)
                            trr = []
                            for letterss in letters_list:
                                scrambled = ''.join(random.choices(letters_list))
                                transaction_id_all = ''.join(scrambled)
                                transaction_ids = transaction_id_all[0:22]
                                trr.append(transaction_ids)
                            transaction_id = ''.join(trr[:23])
                            return transaction_id

                        transaction_id = gen_transaction_id()
                        with open('bill_payments.txt', 'a') as bill_payments:
                            bill_payments.write(
                                f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount_paid}  (-${charges} charges)\nTRANSACTION ID:{transaction_id}\nDesc:PAYMENT OF {bill} FOR ELETRICITY:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

                        trans_amount = bill
                        sender_acct_num = withdrawal_acct
                        reciever_acct_num = 'EKO ELECT'

                        sender_user_name = user_name
                        reciever_user_name = 'EKO ELECT'

                        trans_date = datetime.now()
                        trans_desc = f'PAYMENT OF ${bill} FOR ELECTRICITY'
                        trans_status = 'Successful'

                        sender_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE user_name = %s"
                        my_cur.execute(sender_acct_type_query, (sender_user_name,))
                        sender_acct_type = my_cur.fetchone()

                        # reciever_acct_type_query = "SELECT acct_type FROM bank_tbl WHERE acct_num = %s"
                        # my_cur.execute(reciever_acct_type_query, (recipient_account,))
                        # reciever_acct_type = my_cur.fetchone()
                        reciever_acct_type = 'EKO ELECT'

                        update_trans_table = "INSERT INTO transaction_tbl (transaction_id,transaction_amount,sender_acct_num,reciever_acct_num,sender_user_name,reciever_user_name,transaction_date_time,description,sender_acct_type,reciever_acct_type,transaction_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)"
                        my_cur.execute(update_trans_table, (
                            transaction_id, trans_amount, withdrawal_acct, reciever_acct_num, sender_user_name,
                            reciever_user_name, trans_date, trans_desc, sender_acct_type, reciever_acct_type,
                            trans_status))
                        conn_obj.commit()
                    else:
                        print("Insufficient balance for payment.")
                else:
                    print('Account not found')
            except Exception as e:
                print(f'erot : {e}')
                time.sleep(2)

        elif confirm == 'N':
            time.sleep(1)
            print('You have cancelled the payment')
        else:
            print('Invalid input')

    def pay_water_bill():
        time.sleep(1.5)
        print("\t\t\033[3mf", end='')
        time.sleep(0.255)
        print('e', end='')
        time.sleep(0.255)
        print('t', end='')
        time.sleep(0.255)
        print('c', end='')
        time.sleep(0.255)
        print('h', end='')
        time.sleep(0.255)
        print('i', end='')
        time.sleep(0.255)
        print('n', end='')
        time.sleep(0.255)
        print('g', end='')
        time.sleep(0.255)
        print(" ", end='')
        time.sleep(0.255)
        print('d', end='')
        time.sleep(0.255)
        print('e', end='')
        time.sleep(0.255)
        print('t', end='')
        time.sleep(0.255)
        print('a', end='')
        time.sleep(0.255)
        print('i', end='')
        time.sleep(0.255)
        print('l', end='')
        time.sleep(0.255)
        print('s', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(2)
        print('.', end='')
        time.sleep(0.255)
        print('.', end='')
        time.sleep(0.255)
        print('.\033[0m', end='')
        time.sleep(2)
        bills = [200, 250, 100, 150, 50, 400, 500, 450, 550, 600, 560, 650, 300, 320, 350, 1050, 1500, 1120]
        bill = random.choice(bills)
        print(f"\n\tYour outstanding bill amount for water is ${bill}.")
        confirm = input(f"\n\tDo you want to proceed with the payment [Y/N] ?:  ").upper()

        if confirm == 'Y':
            charges = 0.015 * bill
            amount = bill
            amount_paid = bill + charges

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
            my_cur.execute(select_acc_bal, (user_name, pin_))
            current_balance = my_cur.fetchone()
            time.sleep(4)
            try:
                if current_balance:
                    current_balance = current_balance[0]
                    if current_balance >= bill:
                        # Update the user's account balance in the database with the new balance
                        new_balance = current_balance - amount_paid
                        update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                        my_cur.execute(update_acct_bal, (new_balance, user_name, pin_))
                        conn_obj.commit()

                        print(
                            f"\n\t\033[Payment successful. \n\tYou have paid \033[32m${bill}\033[0m for water (\033[31m-${charges}\033[0m for charges). Your new balance is \033[32m${new_balance}\033[0m\033[0m")

                        select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                        my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                        withdrawal_acct = my_cur.fetchone()
                        withdrawal_acct = str(withdrawal_acct[0])

                        def gen_transaction_id():
                            letters = string.ascii_letters.upper() + string.digits
                            letters_list = list(letters)
                            trr = []
                            for letterss in letters_list:
                                scrambled = ''.join(random.choices(letters_list))
                                transaction_id_all = ''.join(scrambled)
                                transaction_ids = transaction_id_all[0:22]
                                trr.append(transaction_ids)
                            transaction_id = ''.join(trr[:23])
                            return transaction_id

                        transaction_id = gen_transaction_id()
                        with open('bill_payments.txt', 'a') as bill_payments:
                            bill_payments.write(
                                f'Acct: ****{withdrawal_acct[-4:]}\nDR:${amount_paid}  (-${charges} charges)\nTRANSACTION ID:{transaction_id}\nDesc:PAYMENT OF ${bill} FOR WATER:\nDT:{datetime.now()}\n Dial *389# to access bank services\n\n')

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
                            transaction_id, trans_amount, withdrawal_acct, reciever_acct_num, sender_user_name,
                            reciever_user_name, trans_date, trans_desc, sender_acct_type, reciever_acct_type,
                            trans_status))
                        conn_obj.commit()
                    else:
                        print("Insufficient balance for payment.")
                else:
                    print('Account not found')
            except Exception as e:
                print(f'erot : {e}')

        elif confirm == 'N':
            time.sleep(1.5)
            print('You have cancelled the payment')
        else:
            time.sleep(2)
            print('Invalid Input')

    def mobile_top_up_menu():
        time.sleep(2)
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1m+--------------------+-----------------+")
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t|  Top - up  Menu                      |")
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t+--------------------+-----------------+")
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1. Mobile  Top-up  | 2. Data Bundles |")
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t+--------------------+-----------------+\n")

        select = input('Select an option for top-up: ')

        def mobile_top_up():
            try:
                time.sleep(1.5)
                amount = float(input('Enter the top-up amount: '))
                charges = 0.015 * amount
                amount_paid = amount + charges

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
                my_cur.execute(select_acc_bal, (user_name, pin_))
                current_balance = my_cur.fetchone()
                time.sleep(4)
                try:
                    if current_balance:
                        current_balance = current_balance[0]
                        if current_balance >= amount_paid:
                            # Update the user's account balance in the database with the new balance
                            new_balance = current_balance - amount_paid
                            update_acct_bal = "UPDATE bank_tbl SET acct_bal = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (amount, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for airtime top-up (\033[31m-${charges}\033[0m for charges). Your new balance is \033[32m${new_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
                                    scrambled = ''.join(random.choices(letters_list))
                                    transaction_id_all = ''.join(scrambled)
                                    transaction_ids = transaction_id_all[0:22]
                                    trr.append(transaction_ids)
                                transaction_id = ''.join(trr[:23])
                                return transaction_id

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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
                    print(f'eoro {e}')
            except Exception as e:
                print(f'erot : {e}')

        def data_bundles():
            time.sleep(1)
            print('\n\t\t1. $100 for 200MB')
            print('\t\t2. $150 for 300MB')
            print('\t\t3. $300 for 750MB')
            print('\t\t4. $500 for 1GB')
            print('\t\t5. $800 for 2GB')
            print('\t\t6. $1200 for 3GB')
            opt = input('\n : ')

            if opt == '1':
                amount = 100
                data = 200

                # Query the database to retrieve the current balance of the user's account
                airtime_time_bal_sel = "SELECT airtime_balance FROM bank_tbl WHERE user_name = %s AND PIN = %s"
                my_cur.execute(airtime_time_bal_sel, (user_name, pin_))
                air_time_bal = my_cur.fetchone()
                time.sleep(2)
                try:
                    if air_time_bal:
                        air_time_bal = air_time_bal[0]
                        if air_time_bal >= amount:
                            # Update the user's account balance in the database with the new balance
                            new_airtime_balance = air_time_bal - amount
                            update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (data, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
                my_cur.execute(airtime_time_bal_sel, (user_name, pin_))
                air_time_bal = my_cur.fetchone()
                time.sleep(2)
                try:
                    if air_time_bal:
                        air_time_bal = air_time_bal[0]
                        if air_time_bal >= amount:
                            # Update the user's account balance in the database with the new balance
                            new_airtime_balance = air_time_bal - amount
                            update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (data, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
                my_cur.execute(airtime_time_bal_sel, (user_name, pin_))
                air_time_bal = my_cur.fetchone()
                time.sleep(2)
                try:
                    if air_time_bal:
                        air_time_bal = air_time_bal[0]
                        if air_time_bal >= amount:
                            # Update the user's account balance in the database with the new balance
                            new_airtime_balance = air_time_bal - amount
                            update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (data, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
                my_cur.execute(airtime_time_bal_sel, (user_name, pin_))
                air_time_bal = my_cur.fetchone()
                time.sleep(2)
                try:
                    if air_time_bal:
                        air_time_bal = air_time_bal[0]
                        if air_time_bal >= amount:
                            # Update the user's account balance in the database with the new balance
                            new_airtime_balance = air_time_bal - amount
                            update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (data, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
                my_cur.execute(airtime_time_bal_sel, (user_name, pin_))
                air_time_bal = my_cur.fetchone()
                time.sleep(2)
                try:
                    if air_time_bal:
                        air_time_bal = air_time_bal[0]
                        if air_time_bal >= amount:
                            # Update the user's account balance in the database with the new balance
                            new_airtime_balance = air_time_bal - amount
                            update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (data, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
                my_cur.execute(airtime_time_bal_sel, (user_name, pin_))
                air_time_bal = my_cur.fetchone()
                time.sleep(2)
                try:
                    if air_time_bal:
                        air_time_bal = air_time_bal[0]
                        if air_time_bal >= amount:
                            # Update the user's account balance in the database with the new balance
                            new_airtime_balance = air_time_bal - amount
                            update_acct_bal = "UPDATE bank_tbl SET airtime_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_acct_bal, (new_airtime_balance, user_name, pin_))
                            conn_obj.commit()

                            update_airtime_bal = "UPDATE bank_tbl SET data_balance = %s WHERE user_name = %s AND PIN = %s"
                            my_cur.execute(update_airtime_bal, (data, user_name, pin_))
                            conn_obj.commit()

                            print(
                                f"\n\t\033[1mTop-up successful. \n\tYou have paid \033[32m${amount}\033[0m for {data}MB data bundle. Your new airtime balance is \033[32m${new_airtime_balance}\033[0m\033[0m")

                            select_withdrawal_acct_num = "SELECT acct_num FROM bank_tbl where user_name = %s AND PIN = %s"
                            my_cur.execute(select_withdrawal_acct_num, (user_name, pin_))
                            withdrawal_acct = my_cur.fetchone()
                            withdrawal_acct = str(withdrawal_acct[0])

                            def gen_transaction_id():
                                letters = string.ascii_letters.upper() + string.digits
                                letters_list = list(letters)
                                trr = []
                                for letterss in letters_list:
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
                                transaction_id, trans_amount, withdrawal_acct, reciever_acct_num,
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
            else:
                print('Invalid Input')

            print(
                "\033[34m\033[1m1. Press # to go back to top up menu\n2. Press * to go back to bill payment menu\033[0m")
            bck = input(": ")
            if bck == '#':
                mobile_top_up_menu()
            else:
                bills_payment_menu()

        if select == '1':
            mobile_top_up()

        elif select == '2':
            data_bundles()

    if option == '1':
        time.sleep(2)
        pay_electricity_bill()
    elif option == '2':
        time.sleep(1)
        pay_water_bill()
    elif option == '3':
        time.sleep(2)
        mobile_top_up_menu()
    else:
        print('Invalid Input...')

    print(
        "\033[34m\033[1m1. Press # to go back to bill payment menu\n2. Press * to go back to logged in menu\033[0m")
    bck = input(": ")
    if bck == '#':
        bills_payment_menu()
    else:
        logged_in_menu()


def get_response(user_input):
    if 'hey' or 'hi' or 'hello' in user:
        return random.choice(responses.get(user_input.lower(), responses["hi", "hey", "hello", "yo"]))

    responses = {
        "hey": f"Hey there {user_name}. How are you doing today!?",
        "hi": f"Hello {user_name}! How can I assist you today?",
        "hello": f"Hi there {user_name}! What can I do for you?",
        "yo": f"What's up {user_name}! What do you need help with?",
        "i'm good, you?": f"That's nice to hear. I'm also doing good, thanks for asking.",
        "what is your name": f"My name is Cipher. I know your name is {user_name}!!. Don't ask how i knew it, it's my little secret 😁😁",
        "how are you": "I'm an AI, so I don't have feelings. But im feeling damn sassy for sure!!",
        "how are you doing today": "I'm an doing fine for sure. how can I help you!!",
        "what can you do": "I can chat with you, answer basic questions, and assist with information about how the app works.",
        "who is your role model": f"JOHAN LIEBERT!!. He inspires me a lot. Can i tell you a little secret?",
        "who is your boss": "It is Cipher ofc",
        "who is your creator": "It is Cipher ofc",
        "who is your maker": "It is Cipher ofc",
        "yes": f"Im planning to take over the world someday, and in a JOHAN LIEBERT style ofc☺",
        "bye": "Goodbye! Have a great day!",
        "default": "I'm not sure how to respond to that. Can you ask something else?",
        "who are you": "I'm Cipher, your virtual assistant.",
        "how are you": "I'm an AI, so I don't have feelings, but I'm here to help you!",
        "what can you do": "I can chat with you, answer basic questions, and assist with information.",
        "help": "Sure, I'm here to help. What do you need assistance with?",
        "thank you": "You're welcome! If you have any other questions, feel free to ask.",
        "thanks": "You're welcome! How else can I assist you?",
        "bye": "Goodbye! Have a great day!",
        "exit": "Goodbye! Have a great day!",
        "what's the weather like": "I can't check the weather at the moment, but you can use a weather app or website for up-to-date information.",
        "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "how old are you": "I'm as old as the latest update I received. Time is a bit different for AIs!",
        "what's your favorite color": "As an AI, I don't have preferences, but I can help you with color-related queries!",
        "can you help me": "Of course! What do you need help with?",
        "how does this work": "You can ask me questions or request information, and I'll do my best to provide helpful responses.",
        "what's your purpose": "My purpose is to assist you with information and help you with your queries.",
        "where are you from": "I exist in the digital world, created to assist you!",
        "what is ai": "AI stands for Artificial Intelligence, which is the simulation of human intelligence by machines.",
        "do you have any hobbies": "I don't have hobbies, but I enjoy processing information and helping you out!",
        "tell me something interesting": "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "what's the time": "I can't check the current time, but you can check it on your device or a clock nearby.",
        "good morning": "Good morning! How can I assist you today?",
        "good afternoon": "Good afternoon! How can I help you?",
        "good evening": "Good evening! What can I do for you?",
        "good night": "Good night! Have a restful sleep.",
        "how's it going": "It's going well! How can I assist you today?",
        "what's up": "I'm here to help you with whatever you need. How can I assist you?",
        "are you real": "I'm as real as the data and algorithms that power me. I'm here to assist you with your queries.",
        "how do you work": "I process your inputs using natural language processing and provide responses based on pre-programmed information.",
        "why can't you do certain things": "My capabilities are based on my programming and the information I have access to. Some tasks might be beyond my current abilities."

    }
    return responses.get(user_input.lower(), responses["default"])


fun_responses = {
    "tell me a joke": [
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ],
    "give me a fun fact": [
        "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Octopuses have three hearts and blue blood.",
        "Bananas are berries, but strawberries aren't."
    ],
    "play rock paper scissors": ["rock", "paper", "scissors"],
    "flip a coin": ["Heads", "Tails"],
    "roll a die": ["1", "2", "3", "4", "5", "6"],
    "play a guessing game": "I'm thinking of a number between 1 and 10. Can you guess what it is?"
}


def get_fun_response(user_input):
    user_input = user_input.lower()
    if user_input in fun_responses:
        response = fun_responses[user_input]
        if isinstance(response, list):
            if user_input == "play rock paper scissors":
                user_choice = input("Choose rock, paper, or scissors: ").lower()
                ai_choice = random.choice(response)
                if user_choice == ai_choice:
                    return f"We both chose {ai_choice}. It's a tie!"
                elif (user_choice == "rock" and ai_choice == "scissors") or \
                        (user_choice == "paper" and ai_choice == "rock") or \
                        (user_choice == "scissors" and ai_choice == "paper"):
                    return f"I chose {ai_choice}. You win!"
                else:
                    return f"I chose {ai_choice}. I win!"
            elif user_input == "flip a coin":
                return f"The coin landed on {random.choice(response)}."
            elif user_input == "roll a die":
                return f"The die shows {random.choice(response)}."
            else:
                return random.choice(response)
        else:
            return response
    return "I'm not sure how to respond to that. Can you ask something else?"


def guessing_game():
    number = random.randint(1, 10)
    attempts = 0
    dots = ['.', '..', '...', '....', '.....', '....', '...', '..', '.', ' ']
    for dot in dots:
        # Use carriage return to overwrite the same line
        print(f'\rCipher: {dot}', end='', flush=True)
        time.sleep(0.2555)
        print("\rCipher: I'm thinking of a number between 1 and 10. Can you guess what it is?", flush=True)
        break
    while attempts < 3:
        try:
            guess = int(input("Your guess: "))
            attempts += 1
            if guess == number:
                return "Congratulations! You guessed the correct number."
            elif guess < number:
                print("Too low. Try again.")
            else:
                print("Too high. Try again.")
        except ValueError:
            print("Please enter a valid number.")
    return f"Sorry, you've used all attempts. The number was {number}."


def cipher_ai():
    print("Welcome to Cipher AI! Type 'bye' to exit.")
    while True:
        try:
            dots = ['.', '..', '...', '....', '.....', '....', '...', '..', '.', ' ']
            user_input = input("You: ")
            if user_input.lower() == "bye" or user_input.lower() == "exit":
                for dot in dots:
                    print(f'\rCipher: {dot}', end='', flush=True)
                    time.sleep(0.2555)
                print(f"\rCipher: {get_response(user_input)}      ", flush=True)
                break
            elif user_input.lower() == "play a guessing game":
                for dot in dots:
                    # Use carriage return to overwrite the same line
                    print(f'\rCipher: {dot}', end='', flush=True)
                    time.sleep(0.2555)
                    print(f"\rCipher: {guessing_game()}{' ' * 20}", flush=True)
                    break
            else:
                for dot in dots:
                    # Use carriage return to overwrite the same line
                    print(f'\rCipher: {dot}', end='', flush=True)
                    time.sleep(0.2555)
                if user_input.lower() in fun_responses:
                    print(f"\rCipher: {get_fun_response(user_input)}{' ' * 20}", flush=True)
                else:
                    print(f"\rCipher: {get_response(user_input)}{' ' * 20}", flush=True)
        except Exception as e:
            print(f' eror: {e}')

