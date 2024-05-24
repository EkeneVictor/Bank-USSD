import time
from optionsmenu import options_menu
import sys
import textformatting as txf


def start_bank():
    time.sleep(2)
    try:
        a = 0
        while a < 3:
            a += 1
            # Input prompt styled in bold and underlined
            start_time = time.time()
            print("\033[1m\033[4mENTER USSD:\033[0m", end=" ")

            # Get user input
            ussd = input()

            stop_time = time.time()

            if (stop_time - start_time) >= 5:
                time.sleep(2)
                txf.display_error('Error...')
                time.sleep(2)
                txf.print_with_delay(txf.italic() + 'Timeout' + txf.end())
                time.sleep(1.5)
                exit()

            if ussd[0] != '*':
                print("\033[91mInput is not a USSD code ...\033[0m\n")

            if ussd != "*389#":
                print("\033[91mInvalid USSD code\n please re-enter USSD ...\033[0m\n")

            else:
                time.sleep(2)
                print('\t\t\t\t\t\t\t\t\t\t\t\t\t+~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~+')
                print('\t\t\t\t\t\t\t\t\t\t\t\t\t||-----------------------------------------||')
                print('\t\t\t\t\t\t\t\t\t\t\t\t\t|| \033[1m\033[7m Welcome To our USSD Banking service...\033[0m ||')
                print('\t\t\t\t\t\t\t\t\t\t\t\t\t||_________________________________________||\n')

                time.sleep(2)
                print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t||+------------------------------+||")
                print(
                    "\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\033[1m\033[3m     How may we help you\033[0m        ||\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t||+------------------------------+||\n")
                time.sleep(1.5)
                options_menu()
                exit()
        else:
            time.sleep(0.5)
            print("\033[91m checking discrepancies...")
            time.sleep(1)
            print('invalid USSD code')
            time.sleep(5)
            print("An error has occurred.\033[0m")
            time.sleep(2)
            sys.exit()
    except Exception as e:
        print(f'error: {e}')
