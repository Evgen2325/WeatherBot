import random


def generate_random_password(user_input):
    symbols = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!?@#$%&'
    try:
        count_of_block_of_pass = int(user_input)
        pass_str = ''
        for i in range(count_of_block_of_pass):
            for j in range(count_of_block_of_pass):
                pass_str += random.choice(symbols)
            i += 1
            pass_str += '-'
        return pass_str[:-1]

    except Exception:
        return f'input only 1-10'
