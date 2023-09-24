from flask import flash
from database_control import DatabaseQueries, connect_db, close_db_main
import re
import asyncio


async def username_validator(username: str) -> bool:
    connection = connect_db()
    dbase = DatabaseQueries(connection)
    username_is_unique = dbase.check_username_is_unique(username)
    close_db_main(connection)

    if 3 <= len(username) <= 20 and re.match(r"^[a-zA-Z0-9]+$", username) and username_is_unique:
        return True

    else:
        return False


async def password_validator(psw: str) -> bool:
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,32}$', psw):
        return True
    else:
        return False


async def telegram_id_validator(telegram_id: str) -> bool:
    if re.match(r'^[1-9]\d{2,11}$', telegram_id):
        telegram_id: int = int(telegram_id)
    else:
        return False

    connection = connect_db()
    dbase = DatabaseQueries(connection)
    telegram_id_is_unique = dbase.check_telegram_id_is_unique(telegram_id)
    close_db_main(connection)

    if telegram_id_is_unique:
        return True
    else:
        return False


async def registration_validator(username: str, psw: str, telegram_id: str) -> bool:
    """
    :param username: 3 to 15 characters
    :param psw: 4 to 128 characters
    :param telegram_id:
    :return: If entered correctly, it will return True, otherwise it will issue a flash message and return False
    """

    username_is_valid, password_is_valid, telegram_id_is_valid = await asyncio.gather(
        username_validator(username),
        password_validator(psw),
        telegram_id_validator(telegram_id),
    )

    if username_is_valid:
        if password_is_valid:
            if telegram_id_is_valid:
                return True
            else:
                flash("Error - invalid telegram ID.", category="error")
        else:  # each error has its own flash message so that the user knows where he made a mistake
            flash("Error - invalid password format. Use 8-32 characters / at least 1 number and 1 letter",
                  category="error")
    else:
        flash("Error - invalid username format. Use 3 to 20 characters.", category="error")
    return False


if __name__ == '__main__':
    pass
