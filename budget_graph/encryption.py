from os import urandom
from hashlib import pbkdf2_hmac, sha256
from secrets import choice

from budget_graph.logger import setup_logger  # noqa

logger_encrypt = setup_logger("logs/BotLog.log", "bot_logger")


def get_token(key_length_bytes: int = 16) -> str:
    """
    :return: random (entropy-based) character string of length 32 (16 bytes)
    """
    logger_encrypt.info("Getting new token")
    return urandom(key_length_bytes).hex()


# Warning
# The pseudo-random generators os.random() should not be used for security purposes.
# For security or cryptographic uses, see the secrets module.

def get_salt(key_length: int = 32) -> str:
    """
    :return: random (entropy-based) character string of length 32
    """
    logger_encrypt.info("Getting new salt")
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
    logger_encrypt.info(f"Getting new hash: "
                        f"len(secure_key) != 0: {len(secure_key) != 0}, "
                        f"len(salt) != 0: {len(salt) != 0}")
    return pbkdf2_hmac(hash_algorithm, secure_key.encode('utf-8'), salt.encode('utf-8'), iterations, key_length).hex()


def logging_hash(log: str | int) -> str:
    """
    This function should be very fast, since the logging load should not affect the result for the end user.
    """
    log = log if type(log) is str else str(log)
    return sha256(log.encode()).hexdigest()[:15]
