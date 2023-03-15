import string
import random

#size of string


N = 16

def generate_user_identifier():
    result = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=N))
    return result