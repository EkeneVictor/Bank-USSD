import time
import sys



def typing_dots():
    dots = ['.', '..', '...', '....', '.....', '....', '...', '..', '.', ' ']
    for dot in dots:
        print(f'\rCipher: {dot}', end='', flush=True)
        time.sleep(0.2555)


def print_slowly(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)

