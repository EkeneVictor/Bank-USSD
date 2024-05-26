import time
import textformatting as txf
import check_account_details_userside as chck
import delete_acct_userside as dealloc
import deposit_money
import withdraw_money
import transfer_money
import gen_acct_stat_user
import edit_acct_info_user
import bills_payment_menu
import config


def logged_in_menu():
    """function that calls a menu if user is logged in"""
    time.sleep(3)
    print(txf.bold() + '\n\t    +------------------------------+----------------------+--------------------------------+')
    print('\t\t|    Please choose an option                                                           |')
    print('\t\t+------------------------------+----------------------+--------------------------------+')
    print('\t\t|   1. Check Account details   |   2. Delete Account  |  3.      Deposit Money         |')
    print('\t\t+------------------------------+----------------------+--------------------------------+')
    print('\t\t|   4.    Withdraw Money       |   5. Transfer Money  |  6. Generate Account Statement |')
    print('\t\t+------------------------------+----------------------+--------------------------------+')
    print('\t\t|   7.   Edit Account Info     |   8.   Log  out      |  9.      Bills   payment       |')
    print('\t\t+------------------------------+----------------------+--------------------------------+')
    print('\t\t|   10.  Chat with Cipher AI   |                      |                                |')
    print('\t\t+------------------------------+----------------------+--------------------------------+')

    time.sleep(2)
    while True:
        cntn = input('>>> ' + txf.end())
        if cntn != '1' and cntn != '2' and cntn != '3' and cntn != '4' and cntn != '5' and cntn != '6' and cntn != '7' and cntn != '8' and cntn != '9' and cntn != '10':
            time.sleep(2)
            continue
        else:
            time.sleep(1)

        if cntn == '1':
            time.sleep(2)
            chck.check_acct_details(config.user_name, config.pin_)
            break
        elif cntn == '2':
            time.sleep(1)
            dealloc.delete_account(config.user_name, config.pin_)
            break
        elif cntn == '3':
            time.sleep(1)
            deposit_money.deposit_money(config.user_name, config.pin_)
            break
        elif cntn == '4':
            time.sleep(1)
            withdraw_money.withdraw_money(config.user_name, config.pin_)
            break
        elif cntn == '5':
            time.sleep(1.5)
            recipient_account = str(input("\n\033[1mEnter recipient's account number: \033[0m"))
            time.sleep(1.5)
            bill = float(input("\n\033[1mEnter the amount to transfer: \033[0m"))
            time.sleep(0.5)
            description = input("\n\033[1mEnter description: \033[0m")
            transfer_money.transfer_money(config.user_name, config.pin_, recipient_account, bill, description)
            break
        elif cntn == '6':
            time.sleep(4)
            gen_acct_stat_user.generate_account_statement(config.user_name)
            break
        elif cntn == '7':
            time.sleep(2)
            edit_acct_info_user.edit_acct_info(config.user_name, config.pin_)
            break
        elif cntn == '8':
            time.sleep(3)
            txf.print_with_delay(txf.italic() + '\t\tlogging out...' + txf.end())
            time.sleep(3)
            print(txf.italic() + '\t\tlogged out successfully' + txf.end())
            import backs
            backs.back_to_options_menu()
            break
        elif cntn == '9':
            time.sleep(0.5)
            bills_payment_menu.bills_payment_menu()
            break
        elif cntn == '10':
            from cipher_ai import cipher_ai
            time.sleep(1.5)
            cipher_ai()
            break
        else:
            print("\n\033[31mInvalid option. Please choose again.\033[0m")
            continue

    import backs
    backs.back_to_logged_in_menu()
