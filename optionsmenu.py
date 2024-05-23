import time
import textformatting as txf
import sys


def options_menu():
    time.sleep(1)
    print('\n\n')
    print(':' * 200)
    print('\n\n')
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1m+--------------------+----------+---------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| Options Menu                            |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+--------------------+----------+---------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1. Create Account  | 2. Login | 3. Exit |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+--------------------+----------+---------+\n")

    option = input("Select an option: \033[0m")
    time.sleep(2)

    if option == "1":
        import create_acct
        create_acct.create_acct()
    elif option == "2":
        import log_in
        log_in.logged_in()
    elif option == '3':
        time.sleep(0.5)
        txf.print_with_delay(txf.italic() + '\n\t\tExiting...\n' + txf.end())
        time.sleep(4)
        exit()
    else:
        txf.display_error('Invalid option. Please try again.')

    print("\033[34m\033[1m1. Press # to go back to options menu\n2. Press * to exit\033[0m")
    bck = input(": ")
    if bck == '#':
        options_menu()
    else:
        sys.exit()

    exit()
