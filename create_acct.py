import random
import time
import pymysql as sql
import string
import textformatting as txf
import datetime

from backs import back_to_options_menu

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


# function to generate user ID
def generate_user_id():
    """Method to generate user ID"""
    letters_list = string.ascii_letters.upper()
    numbers_list = string.digits
    user_id_first = ''.join(random.choices(letters_list, k=2))
    user_id_num = ''.join(random.choices(numbers_list, k=3))
    user_id_second = ''.join(random.choices(letters_list, k=2))
    user_id = user_id_first + user_id_num + user_id_second
    return user_id


# function to generate account number
def gen_acct_num():
    """Method to generate account number"""
    acct_nu = str(random.randint(10000, 99999))
    acct_numb = "00241" + acct_nu
    return acct_numb


# function to confirm account type
def conf_acct_type(acct_type):
    """Method to confirm account type"""
    if acct_type == 'Savings':
        print('\033[3m\tYou have opened a Savings account\033[0m')
        return 'Savings'
    elif acct_type == 'Business':
        print('\033[3m\tYou have opened a Business account\033[0m')
        return 'Business'
    elif acct_type == 'Student':
        print("\033[3m\tYou have opened a Student's account\033[0m")
        return "Student"
    else:
        return 'Invalid Input'
        # print()


# function to generate username
def gen_user_name(user_name_inp):
    """Method to generate username"""
    for num in range(2):
        user_name_inp += str(random.randint(0, 9))
    return user_name_inp


# function to confirm username
def conf_user_name(user_name_inp):
    select_user_names = 'SELECT user_name from bank_tbl'
    my_cur.execute(select_user_names)
    all_user_names = my_cur.fetchall()
    all_user_names_list = [row[0] for row in all_user_names]  # Extracting usernames from the fetched rows
    if user_name_inp in all_user_names_list:
        new_user_name = gen_user_name(user_name_inp)
        return new_user_name
    else:
        return user_name_inp


def get_user_input(prompt):
    """function that prompts user for input"""
    return input(prompt)


def display_error(message):
    """function that displays error message"""
    print(txf.red() + message + txf.end())
    time.sleep(1)


def handle_no_credentials():
    """function to handle error for user not inputting credentials"""
    time.sleep(2)
    display_error('Sorry, you cannot register in our bank without the necessary credentials')
    for i in range(1, 6):
        time.sleep(1)
        print(txf.red() + f'\rError{"." * i}', end='')
    time.sleep(3)
    print('\nAn unexpected error occurred...' + txf.end())
    time.sleep(2)
    exit()


def validate_input(input_value, length):
    """Function to validate users input"""
    if input_value.isdigit():
        if len(input_value) == length:
            return True
        else:
            display_error(f'Input should be {length} digits')
    else:
        display_error('Input is not a number')
    return False


def is_valid_phone_number(phone_num):
    """function to validate phone number input"""
    valid_prefixes = ['070', '071', '080', '081', '090', '091']
    if phone_num.isdigit() and len(phone_num) == 11 and phone_num[:3] in valid_prefixes:
        return True
    return False


def get_account_by_user_and_type(user_name, acct_type):
    """Function to check if user already exists before"""
    query = '''
        SELECT user_id, user_name, account_type, balance, created_at
        FROM accounts
        WHERE user_name = %s AND account_type = %s
        '''
    my_cur.execute(query, (user_name, acct_type))

    # Fetch the result
    account = my_cur.fetchone()

    # Return the result if found, otherwise return None
    if account:
        return account
    else:
        return None


def print_with_delay(text, delay=0.255):
    """function that simulates text by text typing"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)


def check_user_existence_phone_num(phone_num):
    """Check if a user already exists based on the phone_num"""
    query = "SELECT phone_num FROM bank_tbl"
    my_cur.execute(query)
    all_phone_nums = my_cur.fetchall()
    all_phone_nums_list = [row[0] for row in all_phone_nums]  # Extracting usernames from the fetched rows
    if phone_num in all_phone_nums_list:
        return True
    else:
        return False


def check_user_existence_bvn_num(bvn_input):
    """Check if a user already exists based on the bvn number"""
    if bvn_input != 'NONE':
        query = "SELECT bvn_num FROM bank_tbl"
        my_cur.execute(query)
        all_bvn_nums = my_cur.fetchall()
        all_bvn_nums_list = [row[0] for row in all_bvn_nums]  # Extracting usernames from the fetched rows
        if bvn_input in all_bvn_nums_list:
            return True
        else:
            return False
    else:
        return my_cur.fetchone() is None, False


def check_user_existence_nin_num(nin_input):
    """Check if a user already exists based on the nin number"""
    if nin_input != 'NONE':
        query = "SELECT nin_num FROM bank_tbl"
        my_cur.execute(query)
        all_nin_nums = my_cur.fetchall()
        all_nin_nums_list = [row[0] for row in all_nin_nums]  # Extracting usernames from the fetched rows
        if nin_input in all_nin_nums_list:
            return True
        else:
            return False
    else:
        return my_cur.fetchone() is None, False


def print_account_details(split_details):
    """function to print account details of user"""
    print(
        f'{txf.bold()}\n\t+------------------------------+\n\t'
        f'|      Account Details      '
        f'\n\t+------------------------------+\n'
        f'\t| First name: {split_details[0]}\n'
        f'\t| Last name: {split_details[1]}\n'
        f'\t| Phone number: {split_details[2]}\n'
        f'\t| User name: {split_details[3]}\n'
        f'\t| User ID: {split_details[4]}\n'
        f'\t| Account number: {split_details[5]}\n'
        f'\t| BVN: {split_details[6]}\n'
        f'\t| NIN: {split_details[7]}\n'
        f'\t| Account Balance: ${split_details[8]}\n'
        f'\t| PIN: {split_details[9]}\n'
        f'\t| Account Status: {split_details[10]}\n'
        f'\t| Account Type: {split_details[11]}\n'
        f'\t| Transaction PIN: {split_details[12]}\n'
        f'\t+------------------------------+\n{txf.end()}'
    )


def write_to_file(split_details, user_name_inp):
    """function to write accounts created to a file"""
    with open('accounts.txt', 'a') as accts:
        accts.write(
            f'{txf.bold()}\n\t+------------------------------+\n\t'
            f'|      Account Details   {user_name_inp}   '
            f'\n\t+------------------------------+\n'
            f'\t| First name: {split_details[0]}\n'
            f'\t| Last name: {split_details[1]}\n'
            f'\t| Phone number: {split_details[2]}\n'
            f'\t| User name: {split_details[3]}\n'
            f'\t| User ID: {split_details[4]}\n'
            f'\t| Account number: {split_details[5]}\n'
            f'\t| BVN: {split_details[6]}\n'
            f'\t| NIN: {split_details[7]}\n'
            f'\t| Account Balance: ${split_details[8]}\n'
            f'\t| PIN: {split_details[9]}\n'
            f'\t| Account Status: {split_details[10]}\n'
            f'\t| Account Type: {split_details[11]}\n'
            f'\t| Transaction PIN: {split_details[12]}\n'
            f'\t+------------------------------+\n\n{txf.end()}'
        )


# function to create account
nin_input = 'NONE'


def create_acct():
    """Function to create account"""
    global nin_input
    print(txf.bold() + '*Fill in your details below to open your account\n' + txf.end())
    time.sleep(1.5)
    # creating empty list that acts as temporary storage
    temp_list = []
    # collect first and last name inputs
    fname = input(txf.bold() + "Enter your first name: " + txf.end()).capitalize()
    time.sleep(0.5)
    lname = input(txf.bold() + "Enter your last name: " + txf.end()).capitalize()
    time.sleep(0.5)
    # generate username is username already exists in the db
    user_name_inp = fname.upper() + lname.upper()
    user_name_inp = conf_user_name(user_name_inp)
    while True:
        bvn_input = get_user_input(txf.bold() + "Enter your BVN [enter NONE if you don't have a BVN]: " + txf.end()).upper()
        if bvn_input.upper() == 'NONE':
            time.sleep(1)
            nin_input = get_user_input(txf.bold() + "Enter your NIN [enter NONE if you don't have an NIN]: " + txf.end()).upper()
            if nin_input.upper() == 'NONE' and bvn_input == 'NONE':
                time.sleep(1)
                handle_no_credentials()
            elif validate_input(nin_input, 11):
                break  # Valid NIN, exit the loop
        elif validate_input(bvn_input, 11):
            break  # Valid BVN, exit the loop
    while True:
        phone_num = get_user_input((txf.bold() + 'Enter your phone number: ' + txf.end()))
        if is_valid_phone_number(phone_num):
            break
        else:
            display_error("Invalid phone number. Please try again.")
            time.sleep(1)
            continue

    if check_user_existence_phone_num(phone_num) is True or check_user_existence_bvn_num(bvn_input) is True or (check_user_existence_nin_num(nin_input) is True):

        # If the user exists, ask for user ID and BVN or NIN
        time.sleep(1.5)
        user_id = input(txf.bold() + "Enter your User ID: " + txf.end())
        query = "SELECT * FROM bank_tbl WHERE user_id = %s"
        my_cur.execute(query, (user_id,))
        result = my_cur.fetchone()

        if result:
            name = result[4]  # Assuming the name is in the 5th column
            time.sleep(2.5)
            print(txf.bold() + f"Hey {name}, You can't create multiple accounts at the moment. We are still working on it. Sorry for the inconvenience." + txf.end())
            back_to_options_menu()
        else:
            txf.display_error("Invalid User ID")
    else:
        time.sleep(0.5)
        while True:
            pin_ = str(input(txf.bold() + 'Set your 5-digit PIN: ' + txf.end()))
            if pin_.isdigit() is True:
                if len(pin_) < 5 or len(pin_) > 5:
                    continue
                else:
                    break
            else:
                display_error('Input is not digits')
                continue
        while True:
            transaction_pin = str(input(txf.bold() + 'Set your 4-digit Transaction PIN: ' + txf.end()))
            if transaction_pin.isdigit() is True:
                if len(transaction_pin) < 4 or len(transaction_pin) > 4:
                    continue
                else:
                    break
            else:
                display_error('Input is not digits')
                continue

        acct_stat = 'Active'
        acct_bal = 0
        time.sleep(0.5)
        while True:
            acct_type_inp = input(txf.bold() + "Choose an account type [Savings,Business,Student]: " + txf.end()).capitalize()
            acct_type = conf_acct_type(acct_type_inp)
            existing_account = get_account_by_user_and_type(user_name_inp, acct_type)

            if existing_account:
                display_error(f"Error: User {txf.gray_bg() + {user_name_inp} + txf.end()} already has a {txf.gray_bg() + acct_type + txf.end()} account.")
            else:
                break

            if acct_type == 'Invalid Input':
                continue
            else:
                break

        if acct_type == 'Savings':
            acct_bal = 50
        elif acct_type == 'Business':
            acct_bal = 500
        elif acct_type == 'Student':
            acct_bal = 0
        time.sleep(0.5)
        generate_user_id()
        gen_acct_num()
        temp_list.append(fname)
        temp_list.append(lname)
        temp_list.append(phone_num)
        temp_list.append(user_name_inp)
        user_id = generate_user_id()
        temp_list.append(user_id)
        acct_numb = gen_acct_num()
        temp_list.append(acct_numb)

        if bvn_input:
            temp_list.append(bvn_input)
        else:
            temp_list.append('Empty')

        if nin_input:
            temp_list.append(nin_input)
        else:
            temp_list.append('Empty')
        temp_list.append(str(acct_bal))
        temp_list.append(pin_)
        temp_list.append(acct_stat)
        temp_list.append(acct_type)
        temp_list.append(transaction_pin)
        created_at = datetime.datetime.now()
        details = " ".join(temp_list)
        split_details = details.split(" ")
        # print(split_details)
        print_with_delay(txf.italic() + "\t\tCreating Account...")
        time.sleep(2)
        print("\n\t\tYour account has been created successfully" + txf.end())

        time.sleep(2)
        print_account_details(split_details)
        write_to_file(split_details, user_name_inp)

        # SQL Insert query
        inst_acct_dtls = "INSERT INTO bank_tbl (first_name,last_name,phone_num,user_name,user_id,acct_num,bvn_num,nin_num,acct_bal,PIN,acct_status,acct_type,transaction_pin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # Execute the query with user phone_num
        my_cur.execute(inst_acct_dtls,
                       (fname, lname, phone_num, user_name_inp, user_id, acct_numb, bvn_input, nin_input, acct_bal, pin_, acct_stat, acct_type, transaction_pin))

        inst_acct_db = "INSERT INTO accounts (user_id,user_name,account_type,balance,created_at) VALUES (%s, %s, %s, %s, %s)"
        my_cur.execute(inst_acct_db, (user_id, user_name_inp, acct_type, acct_bal, created_at))

        conn_obj.commit()
        # my_cur.close()
        # conn_obj.close()
        time.sleep(1)

        back_to_options_menu()
