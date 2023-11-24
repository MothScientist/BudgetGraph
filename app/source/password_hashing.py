from hashlib import pbkdf2_hmac
from secrets import choice

# Warning
# The pseudo-random generators os.random() should not be used for security purposes.
# For security or cryptographic uses, see the secrets module.


def get_salt(key_length: int = 32) -> str:
    """
    :return: random (entropy-based) character string of length 32
    """
    return ''.join(choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                   for _ in range(key_length))


def getting_hash(secure_key: str, salt: str,
                 iterations: int = 1024,
                 key_length: int = 32,
                 hash_algorithm: str = "sha3_256") -> str:
    """
    :param secure_key: user's password
    :param iterations: it is best to choose a number from 500 to 2000 (default = 1024)
    :param key_length: output key length (bytes) (default = 32 -> 64 in hex)
    :param hash_algorithm: md5/sha512/sha256/sha512/sha3_256/sha3_512 (default = sha3_256)
    :param salt: get_salt()
    :return: hash in hex format
    """
    return pbkdf2_hmac(hash_algorithm, secure_key.encode('utf-8'), salt.encode('utf-8'), iterations, key_length).hex()
