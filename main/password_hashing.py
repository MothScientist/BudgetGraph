import hashlib


def generate_hash(secure_key: str, iterations=512, key_length=32, hash_algorithm="sha256", salt=""):

    """
    :param secure_key: your password
    :param iterations: it is best to choose a number from 500 to 2000
    :param key_length: output key length in hex
    :param hash_algorithm: it is best to choose sha256 or sha512 - they will provide sufficient reliability and speed
    :param salt: Any string for unique hash generation, not currently used
    :return: hash in hex format
    """

    return hashlib.pbkdf2_hmac(hash_algorithm, secure_key.encode('utf-8'), salt.encode('utf-8'), iterations, key_length).hex()
