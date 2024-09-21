import pymysql as sql

# connecting to the mysql server
conn_obj = sql.connect(
    user='Bank_Admin',
    password='0000',
    host='localhost',
    database='bank_project_db',
)

# connecting to the mysql server
my_cur = conn_obj.cursor()


class Account:
    def __init__(self, user_id, account_type, balance):
        self.user_id = user_id
        self.account_type = account_type
        self.balance = balance


def get_account_by_user_and_type(user_name, account_type):
    """Function to check if user already exists before"""
    query = '''
            SELECT user_id, user_name, account_type, balance, created_at
            FROM accounts
            WHERE user_name = %s AND account_type = %s
            '''
    my_cur.execute(query, (user_name, account_type))

    # Fetch the result
    account = my_cur.fetchone()

    # Return the result if found, otherwise return None
    if account:
        return account
    else:
        return None


def save_account(account):
    # This function should save the account to the database
    pass


def create_account(fname, lname, user_name, bvn, nin, phone_num, pin, transaction_pin, account_status, user_id, account_type):
    # Check if the user already has this type of account
    existing_account = get_account_by_user_and_type(user_id, account_type)
    if existing_account:
        return "You already have a {} account.".format(account_type)
    # Determine initial balance
    initial_balance = 0
    if account_type == "savings":
        initial_balance = 50
    elif account_type == "business":
        initial_balance = 500
    elif account_type == 'student':
        initial_balance = 0
    elif account_type == 'current':
        initial_balance = 100
    # Create the new account
    new_account = Account(user_id=user_id, account_type=account_type, balance=initial_balance)
    save_account(new_account)
    return "Account created successfully."


# Example usage
user_id = 1
account_type = "savings"
message = create_account(user_id, account_type)
print(message)
