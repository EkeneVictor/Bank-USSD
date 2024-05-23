import time
import sys


def back_to_options_menu():
    print("\033[34m\033[1m1. Press # to go back to options menu\n2. Press * to exit\033[0m")
    bck = input(":")
    time.sleep(1)
    if bck == '#':
        # noinspection PyUnresolvedReferences
        options_menu()
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
