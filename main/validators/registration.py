from flask import flash
from database_control import get_db, FDataBase


def registration_validator(username: str, password: str, tg_link: str) -> bool:
    """
    :param username: 3 to 15 characters
    :param password: 4 to 128 characters
    :param tg_link: https://t.me/{username} - username: 18 to 45 characters (unique)
    :return: If entered correctly, it will return True, otherwise it will issue a flash message and return False
    """
    if 3 <= len(username) <= 20:
        if 4 <= len(password) <= 128:
            if 18 <= len(tg_link) <= 45 and tg_link.startswith("https://t.me/"):
                dbase = FDataBase(get_db())
                if not dbase.get_id_by_username(username, tg_link):
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
    dbase = FDataBase(get_db())
    """
    :param token: checking if the token exists in the database
    :return: 0 - if there is no group with this token
             x - if the group exists (x - group id)
    """
    return dbase.get_group_id_by_token(token)
