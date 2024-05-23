import time


def end():
    """Method to reset string formatting"""
    return '\033[0m'


def bold():
    """Method to bold text"""
    return '\033[1m'


def dim():
    """Method to dim text"""
    return '\033[2m'


def italic():
    """Method to italicize text"""
    return '\033[3m'


def underline():
    """Method to underline text"""
    return '\033[4m'


def invert_colors():
    """Method to swap fore and background colors"""
    return '\033[7m'


def hidden():
    """Method to make text hidden or invisible"""
    return '\033[8m'


def black():
    return '\033[30m'


def red():
    return '\033[31m'


def green():
    return '\033[32m'


def yellow():
    return '\033[33m'


def blue():
    return '\033[34m'


def magenta():
    return '\033[35m'


def cyan():
    return '\033[36m'


def white():
    return '\033[37m'


def gray():
    return '\033[90m'


def bright_red():
    return '\033[91m'


def bright_green():
    return '\033[92m'


def bright_yellow():
    return '\033[93m'


def bright_blue():
    return '\033[94m'


def bright_magenta():
    return '\033[95m'


def bright_cyan():
    return '\033[96m'


def bright_white():
    return '\033[97m'


def black_bg():
    return '\033[40m'


def red_bg():
    return '\033[41m'


def green_bg():
    return '\033[42m'


def yellow_bg():
    return '\033[43m'


def blue_bg():
    return '\033[44m'


def magenta_bg():
    return '\033[45m'


def cyan_bg():
    return '\033[46m'


def gray_bg():
    return '\033[100m'


def bright_red_bg():
    return '\033[101m'


def bright_green_bg():
    return '\033[102m'


def bright_yellow_bg():
    return '\033[103m'


def bright_blue_bg():
    return '\033[104m'


def bright_magenta_bg():
    return '\033[105m'


def bright_cyan_bg():
    return '\033[106m'


def bright_white_bg():
    return '\033[107m'


def get_user_input(prompt):
    """function that prompts user for input"""
    return input(prompt)


def display_error(message):
    """function that displays error message"""
    print(red() + message + end())
    time.sleep(1)


def print_with_delay(text, delay=0.255):
    """function that simulates text by text typing"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
