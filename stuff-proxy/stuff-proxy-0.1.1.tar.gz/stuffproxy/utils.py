from random import choice
import string


def generate_secret(length=32):
    s = ''
    for i in range(0, length):
        s += choice(string.ascii_letters + string.digits)  # + string.punctuation)

    return s
