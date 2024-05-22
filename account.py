

class Account:
    def __init__(self, user_id, account_type, balance):
        self.user_id = user_id
        self.account_type = account_type
        self.balance = balance


def get_account_by_user_and_type(user_id, account_type):
    # This function should query the database to check for an existing account
    # For demonstration, assume it returns None if no account is found
    pass


def save_account(account):
    # This function should save the account to the database
    pass


def create_account(user_id, account_type):
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

    # Create the new account
    new_account = Account(user_id=user_id, account_type=account_type, balance=initial_balance)
    save_account(new_account)
    return "Account created successfully."


# Example usage
user_id = 1
account_type = "savings"
message = create_account(user_id, account_type)
print(message)
