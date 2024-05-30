import random
import time
import pymysql as sql
import string
import textformatting as txf
from datetime import datetime

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


class AccountRestrictions:
    def __init__(self, min_balance, max_balance, max_withdrawal, max_deposit, interest_rate, transfer_limit, max_loan):
        self.min_balance = min_balance
        self.max_balance = max_balance
        self.max_withdrawal = max_withdrawal
        self.max_deposit = max_deposit
        self.interest_rate = interest_rate
        self.transfer_limit = transfer_limit
        self.max_loan = max_loan


# Defining restrictions for each account type
savings_restrictions = AccountRestrictions(
    min_balance=50, max_balance=100000, max_withdrawal=2000, max_deposit=10000,
    interest_rate=1.5, transfer_limit=1000, max_loan=0)

business_restrictions = AccountRestrictions(
    min_balance=500, max_balance=float('inf'), max_withdrawal=10000, max_deposit=50000,
    interest_rate=1.0, transfer_limit=20000, max_loan=500000)

student_restrictions = AccountRestrictions(
    min_balance=0, max_balance=10000, max_withdrawal=500, max_deposit=5000,
    interest_rate=2.0, transfer_limit=500, max_loan=50000)

current_restrictions = AccountRestrictions(
    min_balance=100, max_balance=float('inf'), max_withdrawal=5000, max_deposit=20000,
    interest_rate=0, transfer_limit=5000, max_loan=100000)


def handle_transaction(account_type, action, amount):
    status, message = check_restrictions(account_type, action, amount)
    if not status:
        print(message)
        return


def check_restrictions(account_type, action, amount):
    if account_type == 'Savings':
        restrictions = savings_restrictions
    elif account_type == 'Business':
        restrictions = business_restrictions
    elif account_type == 'Student':
        restrictions = student_restrictions
    elif account_type == 'Current':
        restrictions = current_restrictions
    else:
        return False, "Invalid account type"

    if action == 'withdrawal' and amount > restrictions.max_withdrawal:
        return False, f"Exceeds maximum withdrawal limit of ${restrictions.max_withdrawal}"
    elif action == 'deposit' and amount > restrictions.max_deposit:
        return False, f"Exceeds maximum deposit limit of ${restrictions.max_deposit}"
    elif action == 'transfer' and amount > restrictions.transfer_limit:
        return False, f"Exceeds maximum transfer limit of ${restrictions.transfer_limit}"
    elif action == 'loan' and amount > restrictions.max_loan:
        return False, f"Exceeds maximum loan limit of ${restrictions.max_loan}"

    return True, "Transaction approved"


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
        time.sleep(1)
        initial_deposit = float(input("Enter your initial deposit amount (minimum $50): "))

        if initial_deposit < 50:
            time.sleep(1)
            print("Invalid deposit. Minimum deposit is $50.")
            return 'Invalid Savings Deposit'

        return 'Savings'
    elif acct_type == 'Current':
        time.sleep(1)
        government_id = input("Enter your government ID number: ")
        valid_government_ids = [
            "G10001", "G10002", "G10003", "G10004", "G10005", "G10006", "G10007", "G10008", "G10009", "G10010",
            "G10011", "G10012", "G10013", "G10014", "G10015", "G10016", "G10017", "G10018", "G10019", "G10020"]

        if government_id not in valid_government_ids:
            print('Invalid Government ID')
            return 'Invalid Government ID'

        return 'Current'
    elif acct_type == 'Business':
        time.sleep(1)
        business_reg_number = input("Enter your business registration number: ")
        valid_registration_numbers = [
            "B10001", "B10002", "B10003", "B10004", "B10005", "B10006", "B10007", "B10008", "B10009", "B10010",
            "B10011", "B10012", "B10013", "B10014", "B10015", "B10016", "B10017", "B10018", "B10019", "B10020"]

        if business_reg_number not in valid_registration_numbers:
            print('Invalid Registration Number')
            return 'Invalid Registration'

        return 'Business'
    elif acct_type == 'Student':
        time.sleep(1)
        age = int(input("Enter your age: "))

        if age < 18 or age > 25:
            time.sleep(1)
            print("Invalid age. Must be between 18 and 25 years.")
            return 'Invalid age'

        student_id = input(txf.bold() + "Enter your student ID number: " + txf.end())
        valid_ids = [
            "S10001", "S10002", "S10003", "S10004", "S10005", "S10006", "S10007", "S10008", "S10009", "S10010",
            "S10011", "S10012", "S10013", "S10014", "S10015", "S10016", "S10017", "S10018", "S10019", "S10020",
            "S10021", "S10022", "S10023", "S10024", "S10025", "S10026", "S10027", "S10028", "S10029", "S10030",
            "S10031", "S10032", "S10033", "S10034", "S10035", "S10036", "S10037", "S10038", "S10039", "S10040",
            "S10041", "S10042", "S10043", "S10044", "S10045", "S10046", "S10047", "S10048", "S10049", "S10050",
            "S10051", "S10052", "S10053", "S10054", "S10055", "S10056", "S10057", "S10058", "S10059", "S10060",
            "S10061", "S10062", "S10063", "S10064", "S10065", "S10066", "S10067", "S10068", "S10069", "S10070",
            "S10071", "S10072", "S10073", "S10074", "S10075", "S10076", "S10077", "S10078", "S10079", "S10080",
            "S10081", "S10082", "S10083", "S10084", "S10085", "S10086", "S10087", "S10088", "S10089", "S10090",
            "S10091", "S10092", "S10093", "S10094", "S10095", "S10096", "S10097", "S10098", "S10099", "S10100",
            "S10101", "S10102", "S10103", "S10104", "S10105", "S10106", "S10107", "S10108", "S10109", "S10110",
            "S10111", "S10112", "S10113", "S10114", "S10115", "S10116", "S10117", "S10118", "S10119", "S10120",
            "S10121", "S10122", "S10123", "S10124", "S10125", "S10126", "S10127", "S10128", "S10129", "S10130",
            "S10131", "S10132", "S10133", "S10134", "S10135", "S10136", "S10137", "S10138", "S10139", "S10140",
            "S10141", "S10142", "S10143", "S10144", "S10145", "S10146", "S10147", "S10148", "S10149", "S10150",
            "S10151", "S10152", "S10153", "S10154", "S10155", "S10156", "S10157", "S10158", "S10159", "S10160",
            "S10161", "S10162", "S10163", "S10164", "S10165", "S10166", "S10167", "S10168", "S10169", "S10170",
            "S10171", "S10172", "S10173", "S10174", "S10175", "S10176", "S10177", "S10178", "S10179", "S10180",
            "S10181", "S10182", "S10183", "S10184", "S10185", "S10186", "S10187", "S10188", "S10189", "S10190",
            "S10191", "S10192", "S10193", "S10194", "S10195", "S10196", "S10197", "S10198", "S10199", "S10200"]

        if student_id not in valid_ids:
            print('Invalid Student ID')
            return 'Invalid ID'

        return "Student"
    else:
        return 'Invalid Input'


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
            f'\n\t+------------------------------+\n\t'
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
            f'\t+------------------------------+\n\n'
        )


# function to create account
nin_input = 'NONE'


def create_acct_v2(user_id):
    """Function to create account"""
    global nin_input
    print(txf.bold() + '*Fill in your details below to open another account\n' + txf.end())
    time.sleep(1.5)
    # creating empty list that acts as temporary storage
    temp_list = []
    # collect first and last name inputs
    select_fname = "SELECT first_name FROM bank_tbl WHERE user_id = %s"
    my_cur.execute(select_fname, user_id)
    fname = str(my_cur.fetchone()[0])
    # fname = input(txf.bold() + "Enter your first name: " + txf.end()).capitalize()
    time.sleep(0.5)
    select_lname = "SELECT last_name FROM bank_tbl WHERE user_id = %s"
    my_cur.execute(select_lname, user_id)
    lname = str(my_cur.fetchone()[0])
    # lname = input(txf.bold() + "Enter your last name: " + txf.end()).capitalize()
    time.sleep(0.5)
    # generate username is username already exists in the db
    user_name_inp = fname.upper() + lname.upper()
    bvn_input_sel = "SELECT bvn_num FROM bank_tbl WHERE user_id = %s"
    my_cur.execute(bvn_input_sel, user_id)
    bvn_input = my_cur.fetchone()[0]
    nin_input_sel = "SELECT nin_num FROM bank_tbl WHERE user_id = %s"
    my_cur.execute(nin_input_sel, user_id)
    nin_input = my_cur.fetchone()[0]
    phone_input_sel = "SELECT phone_num FROM bank_tbl WHERE user_id = %s"
    my_cur.execute(phone_input_sel, user_id)
    phone_num = my_cur.fetchone()[0]
    # user_name_inp = conf_user_name(user_name_inp)
    # while True:
    #     bvn_input = get_user_input(
    #         txf.bold() + "Enter your BVN [enter NONE if you don't have a BVN]: " + txf.end()).upper()
    #     if bvn_input.upper() == 'NONE':
    #         time.sleep(1)
    #         nin_input = get_user_input(
    #             txf.bold() + "Enter your NIN [enter NONE if you don't have an NIN]: " + txf.end()).upper()
    #         if nin_input.upper() == 'NONE' and bvn_input == 'NONE':
    #             time.sleep(1)
    #             handle_no_credentials()
    #         elif validate_input(nin_input, 11):
    #             break  # Valid NIN, exit the loop
    #     elif validate_input(bvn_input, 11):
    #         break  # Valid BVN, exit the loop
    # while True:
    #     phone_num = get_user_input((txf.bold() + 'Enter your phone number: ' + txf.end()))
    #     if is_valid_phone_number(phone_num):
    #         break
    #     else:
    #         display_error("Invalid phone number. Please try again.")
    #         time.sleep(1)
    #         continue
    # time.sleep(0.5)
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
        acct_type_inp = input(
            txf.bold() + "Choose an account type [Savings,Business,Student]: " + txf.end()).capitalize()
        acct_type = conf_acct_type(acct_type_inp)
        if acct_type == 'Invalid Input':
            continue

        existing_account = get_account_by_user_and_type(user_name_inp, acct_type)

        if existing_account:
            print(f"\033[31mError\033[0m: User {user_name_inp} already has a {acct_type} account.\n\tPlease choose another account type.")
            time.sleep(2)
            back_to_options_menu()
        else:
            break
    if acct_type == 'Savings':
        acct_bal = 50
    elif acct_type == 'Business':
        acct_bal = 500
    elif acct_type == 'Student':
        acct_bal = 0
    time.sleep(0.5)
    gen_acct_num()
    temp_list.append(fname)
    temp_list.append(lname)
    temp_list.append(phone_num)
    temp_list.append(user_name_inp)
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
    created_at = datetime.now()
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
    inst_acct_dtls = "INSERT INTO bank_tbl (first_name,last_name,phone_num,user_name,user_id,acct_num,bvn_num,nin_num,acct_bal,PIN,acct_status,acct_type,transaction_pin,creation_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # Execute the query with user phone_num
    my_cur.execute(inst_acct_dtls,
                   (fname, lname, phone_num, user_name_inp, user_id, acct_numb, bvn_input, nin_input, acct_bal, pin_,
                    acct_stat, acct_type, transaction_pin, created_at))

    inst_acct_db = "INSERT INTO accounts (user_id,user_name,account_type,balance,created_at) VALUES (%s, %s, %s, %s, %s)"
    my_cur.execute(inst_acct_db, (user_id, user_name_inp, acct_type, acct_bal, created_at))

    conn_obj.commit()
    # my_cur.close()
    # conn_obj.close()
    time.sleep(1)

    back_to_options_menu()
# except Exception as e:
#     print(f'error: {e}')


def create_acct():
    """Function to create account"""
    global nin_input
    print(txf.bold() + '*Fill in your details below to open an oaccount\n' + txf.end())
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
            name = result[4]
            time.sleep(2.5)
            print(txf.bold() + f"Hey {name}, Welcome Back!" + txf.end())
            time.sleep(2)
            # select_accts = "SELECT * FROM accounts WHERE user_id = %s"
            # my_cur.execute(select_accts, user_id)
            # accts = my_cur.fetchall()
            # first_acct = accts[0]
            # second_acct = accts[1]
            # third_acct = accts[2]
            # print(first_acct[2])
            # print(second_acct[2])
            # print(third_acct[2])

            create_acct_v2(user_id)

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
            acct_type_inp = input(
                txf.bold() + "Choose an account type [Savings, Business, Student, Current]: " + txf.end()).capitalize()
            acct_type = conf_acct_type(acct_type_inp)
            if acct_type == 'Invalid age':
                time.sleep(2)
                print("Cannot create account. Age requirement not met.")
                time.sleep(2)
                return
            elif acct_type == 'Invalid ID':
                time.sleep(2)
                print("Cannot create account. Invalid student ID.")
                time.sleep(2)
                return
            elif acct_type == 'Invalid Registration':
                print("Cannot create account. Invalid business registration number.")
                return
            elif acct_type == 'Invalid Savings Deposit':
                print("Cannot create account. Minimum deposit for savings account not met.")
                return
            elif acct_type == 'Invalid Government ID':
                print("Cannot create account. Invalid government ID number.")
                return
            elif acct_type == 'Invalid Input':
                time.sleep(2)
                print("Invalid account type. Please choose from Savings, Business, or Student.")
                time.sleep(2)
                continue

            existing_account = get_account_by_user_and_type(user_name_inp, acct_type)

            if existing_account:
                display_error(
                    f"Error: User {txf.gray_bg() + user_name_inp + txf.end()} already has a {txf.gray_bg() + acct_type + txf.end()} account.")
            else:
                break

        if acct_type == 'Savings':
            acct_bal = 50
        elif acct_type == 'Business':
            acct_bal = 500
        elif acct_type == 'Student':
            acct_bal = 0
        elif acct_type == 'Current':
            acct_bal = 100
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
        created_at = datetime.now()
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
        inst_acct_dtls = "INSERT INTO bank_tbl (first_name,last_name,phone_num,user_name,user_id,acct_num,bvn_num,nin_num,acct_bal,PIN,acct_status,acct_type,transaction_pin,creation_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # Execute the query with user phone_num
        my_cur.execute(inst_acct_dtls,
                       (fname, lname, phone_num, user_name_inp, user_id, acct_numb, bvn_input, nin_input, acct_bal, pin_, acct_stat, acct_type, transaction_pin, created_at))

        inst_acct_db = "INSERT INTO accounts (user_id,user_name,account_type,balance,created_at) VALUES (%s, %s, %s, %s, %s)"
        my_cur.execute(inst_acct_db, (user_id, user_name_inp, acct_type, acct_bal, created_at))

        conn_obj.commit()
        # my_cur.close()
        # conn_obj.close()
        time.sleep(1)

        back_to_options_menu()
