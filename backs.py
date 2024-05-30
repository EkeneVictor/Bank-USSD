import time
import sys
import config


def back_to_options_menu():
    print("\033[34m\033[1m1. Press # to go back to options menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        import optionsmenu
        optionsmenu.options_menu()
    else:
        sys.exit()


def back_to_admin_menu():
    print("\033[34m\033[1m1. Press # to go back to admin menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        import adminmenu
        adminmenu.admin_menu()
    else:
        sys.exit()


def back_to_logged_in_menu():
    print("\033[34m\033[1m1. Press # to go back to logged in menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        import loggedinmenu
        loggedinmenu.logged_in_menu()
    else:
        sys.exit()


def back_to_bill_payment_menu():
    print("\033[34m\033[1m1. Press # to go back to bills payment menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        import bills_payment_menu
        bills_payment_menu.bills_payment_menu()
    else:
        sys.exit()


def back_to_loan_menu():
    print("\033[34m\033[1m1. Press # to go back to loan menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        import loan_money
        loan_money.loan_menu(config.user_name)
    else:
        sys.exit()


def back_to_top_up_menu():
    print("\033[34m\033[1m1. Press # to go back to top up menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        from mobile_menu import mobile_top_up_menu
        mobile_top_up_menu()
    else:
        sys.exit()
