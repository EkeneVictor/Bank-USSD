from loan_money import process_loan_application, check_loan_status, make_loan_repayment
import time
import textformatting as txf
import loggedinmenu
import config
import backs


def loan_menu(user_name):
    print(
        txf.bold() + "\t\t\t\t\t\t\t\t\t\t\t\t\t+-----------------------+---------------+------------------+--------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| Loan  Menu                                                             |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+----------------+------------------+--------------+")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t| 1.  Apply for Loan   | 2. Loan Status | 3. Repay Loan    | 4.   Exit    |")
    print("\t\t\t\t\t\t\t\t\t\t\t\t\t+----------------------+----------------+------------------+--------------+\n")

    user_input = input(">>>: ")
    if user_input == "1":
        time.sleep(3)
        amount = float(input("Enter loan amount: "))
        repayment_period = int(input("Enter repayment period in months: "))
        trans_pin_input = input("Enter your transaction pin: ")
        process_loan_application(user_name, amount, repayment_period, trans_pin_input,  config.pin_)
        backs.back_to_loan_menu()
    elif user_input == "2":
        time.sleep(2)
        response = check_loan_status(user_name)
        print(response)
        backs.back_to_loan_menu()
    elif user_input == '3':
        time.sleep(1)
        response = make_loan_repayment(user_name)
        print(response)
        backs.back_to_loan_menu()
    elif user_input == '4':
        time.sleep(1.5)
        txf.print_with_delay(txf.italic() + '\n\tExiting...' + txf.end())
        loggedinmenu.logged_in_menu()
    else:
        print("Invalid input. Please try again.")
