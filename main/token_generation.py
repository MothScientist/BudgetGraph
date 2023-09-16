from secrets import choice


def get_token():
    """
    :return: random (entropy-based) character string of length 32
    """
    return ''.join(choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@%#&*") for _ in range(32))
