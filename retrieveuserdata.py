
def retr_user_data():
    global user_name
    global pin_
    time.sleep(2.5)

    if user_name and pin_:
        # Query the database to check if the provided BVN and PIN match any user records
        check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
        my_cur.execute(check_login_data, (user_name, pin_))
        user = my_cur.fetchone()
        if user:
            return user
    else:
        print("\n\033[31mYou have not logged in\033[0m")
        return None  # Return None if the user is not logged in


def retrieve_user_data():
    global user_name
    global pin_
    time.sleep(2.5)
    user_name = str(input('\n\033[1mInput yout User name: \033[0m')).upper()
    time.sleep(1)
    pin_ = str(input('\n\033[1mInput your 5-digit PIN: \033[0m'))

    if user_name and pin_:
        # Query the database to check if the provided BVN and PIN match any user records
        check_login_data = "SELECT * FROM bank_tbl WHERE user_name = %s AND PIN = %s "
        my_cur.execute(check_login_data, (user_name, pin_))
        user = my_cur.fetchone()

        if user:
            return user



    else:
        print("\n\033[31mYou have not logged in\033[0m")
        return None  # Return None if the user is not logged in
