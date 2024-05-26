import textformatting as txf
import time
import retrieveuserdata as ret


def check_acct_details(user_name, pin):
    user_data = ret.retr_user_data(user_name, pin)
    txf.print_with_delay(txf.italic() + '\t\tfetching details' + txf.end(),)
    time.sleep(2)
    try:
        print(
            f'{txf.bold()}\n\t+------------------------------+\n\t'
            f'|      Account Details      '
            f'\n\t+------------------------------+\n'
            f'\t| First name: {user_data[1]}\n'
            f'\t| Last name: {user_data[2]}\n'
            f'\t| Phone number: {user_data[3]}\n'
            f'\t| User name: {user_data[4]}\n'
            f'\t| User ID: {user_data[5]}\n'
            f'\t| Account number: {user_data[6]}\n'
            f'\t| BVN: {user_data[7]}\n'
            f'\t| NIN: {user_data[8]}\n'
            f'\t| Account Balance: ${user_data[9]}\n'
            f'\t| PIN: {user_data[10]}\n'
            f'\t| Account Status: {user_data[11]}\n'
            f'\t| Account Type: {user_data[12]}\n'
            f'\t| Transaction PIN: {user_data[13]}\n'
            f'\t+------------------------------+\n{txf.end()}'
        )
    except Exception as e:
        print(f'error :{e}')
