from flask import flash
from database_control import get_db, FDataBase, connect_db, close_db_bot
import re


def registration_validator(username: str, psw: str, tg_link: str) -> bool:
    """
    :param username: 3 to 15 characters
    :param psw: 4 to 128 characters
    :param tg_link: https://t.me/{username} - username: 18 to 45 characters (unique)
    :return: If entered correctly, it will return True, otherwise it will issue a flash message and return False
    """
    if 3 <= len(username) <= 20 and not re.match(r'^[$\\/\\-_#@&*№!:;\'",`~]', username):
        if 4 <= len(psw) <= 128:
            if 18 <= len(tg_link) <= 45 and tg_link.startswith("https://t.me/"):
                dbase = FDataBase(get_db())
                if not dbase.get_id_by_username_or_tg_link(username=username, tg_link=tg_link):
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
    dbase = FDataBase(connection)
    group_id = dbase.get_group_id_by_token(token)
    close_db_bot(connection)
    return group_id
