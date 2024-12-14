import sys
from secrets import compare_digest

sys.path.append('../')

from budget_graph.logger import setup_logger
from budget_graph.encryption import logging_hash

logger_registration = setup_logger("logs/RegistrationLog.log", "registration_logger")


# pylint: disable=too-many-arguments, too-many-positional-arguments
def user_registration(db_connection, token: str, telegram_id: int, username: str, psw_salt: str, psw_hash: str) \
        -> tuple[bool, str]:
    """
    Returns the status and a string (either with a token or an error message)
    """
    if compare_digest(token, 'None'):
        res: str = db_connection.registration_new_user(telegram_id, username, psw_salt, psw_hash)
        if res:
            return True, res
        logger_registration.error(f"Error adding new user to database: TelegramID: {logging_hash(telegram_id)}, "
                                  f"username: {logging_hash(username)}")
        return False, 'create_new_user_or_group_error'

    if len(token) == 32 and token.isalnum() and token.islower():
        group_id: int = db_connection.get_group_id_by_token(token)
        if not group_id:
            return False, 'group_not_exist'
        res: bool = db_connection.registration_new_user(telegram_id, username, psw_salt, psw_hash,
                                                                        group_id=group_id)
        if res:
            return True, ''
        logger_registration.error(f"Error adding new user to database: TelegramID: {logging_hash(telegram_id)}, "
                                  f"username: {logging_hash(username)}, group id #{group_id}")
        return False, 'group_is_full'

    return False, 'invalid_token_format'
