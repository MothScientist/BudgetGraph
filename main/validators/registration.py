from flask import flash
from database_control import get_db, DatabaseQueries, connect_db, close_db_main
import re


def registration_validator(username: str, psw: str, telegram_id: str) -> bool:
    """
    :param username: 3 to 15 characters
    :param psw: 4 to 128 characters
    :param telegram_id:
    :return: If entered correctly, it will return True, otherwise it will issue a flash message and return False
    """
    if 3 <= len(username) <= 20 and re.match(r"^[a-zA-Z0-9]+$", username):
        if 4 <= len(psw) <= 128:
            if len(telegram_id) <= 12 and re.match(r'^\d+$', telegram_id):
                dbase = DatabaseQueries(get_db())
                telegram_id: int = int(telegram_id)
                if not dbase.get_id_by_username_or_telegram_id(username=username, telegram_id=telegram_id):
                    return True
                else:
                    flash("Error - the username is taken or the link is entered incorrectly.", category="error")
            else:  # each error has its own flash message so that the user knows where he made a mistake
                flash("Error - invalid telegram link.", category="error")
        else:
            flash("Error - invalid password format. Use 4 to 128 characters.", category="error")
    else:
        flash("Error - invalid username format. Use 3 to 20 characters.", category="error")
    return False


def token_validator(token: str) -> int:
    """
    :param token: checking if the token exists in the database
    :return: 0 - if there is no group with this token
             x - if the group exists (x - group id)
    """
    connection = connect_db()
    dbase = DatabaseQueries(connection)
    group_id = dbase.get_group_id_by_token(token)
    close_db_main(connection)
    return group_id


if __name__ == '__main__':
    pass
