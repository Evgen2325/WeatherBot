import random


def generate_random_password():
    symbols = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM.,\\?!-_'
    length = random.randint(10, 20)
    password = ''
    for i in range(int(length)):
        password += random.choice(symbols)
    return password
