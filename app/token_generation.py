import os


def get_token(key_length_bytes: int = 16) -> str:
    """
    :return: random (entropy-based) character string of length 32 (16 bytes)
    """
    return os.urandom(key_length_bytes).hex()
