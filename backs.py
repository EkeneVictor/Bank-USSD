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
