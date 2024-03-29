import asyncio
import re
from flask import flash
from datetime import datetime, timezone

import sys
sys.path.append('../')

from app.db_manager import DatabaseQueries, connect_db, close_db
from app.dictionary import Dictionary
from app.time_checking import timeit


@timeit
async def registration_validation(username: str, psw: str, telegram_id: str) -> bool:
    """
    :param username: 3 to 15 characters
    :param psw: 4 to 128 characters
    :param telegram_id:
    :return: If entered correctly, it will return True, otherwise it will issue a flash message and return False
    """

    username_is_valid, password_is_valid, telegram_id_is_valid = await asyncio.gather(
        username_validation(username),
        password_validation(psw),
        telegram_id_validation(telegram_id)
    )

    if username_is_valid:  # TODO remove flask flash and return raise error
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


async def username_validation(username: str) -> bool:
    connection = connect_db()
    dbase = DatabaseQueries(connection)
    username_is_exist: bool = dbase.check_username_is_exist(username)
    close_db(connection)

    if 3 <= len(username) <= 20 and re.match(r"^[a-zA-Z0-9]+$", username) and not username_is_exist:
        return True
    return False


async def password_validation(psw: str) -> bool:
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,32}$', psw):
        return True
    return False


async def telegram_id_validation(telegram_id: str) -> bool:  # type: ignore
    if re.match(r'^[1-9]\d{2,11}$', telegram_id):  # 3-12 digits
        telegram_id: int = int(telegram_id)
    else:
        return False

    connection = connect_db()
    dbase = DatabaseQueries(connection)
    telegram_id_is_exist: bool = dbase.check_telegram_id_is_exist(telegram_id)
    close_db(connection)

    if not telegram_id_is_exist:
        return True
    return False


async def date_validation(entered_date: str) -> bool:  # entered date in format DD/MM/YYYY
    if not await check_date_in_correct_format(entered_date):
        return False

    _day: int = int(entered_date[:2])
    _month: int = int(entered_date[3:5])
    _year: int = int(entered_date[-4:])
    day_is_correct = await check_day_is_correct(_year, _month, _day)

    if not day_is_correct:
        return False

    checking_date_in_unix_format: bool = await comparison_dates_unix_format(entered_date)
    if checking_date_in_unix_format:
        return True

    return False


async def comparison_dates_unix_format(entered_date: str) -> bool:
    """
    :param entered_date: date in format DD/MM/YYYY

    The custom date should not be less than 10 years from the current one
    and more than 1 day from the current one

    Time 1 day ahead is necessary due to the difference in time zones
    (since the user enters the date independently in the DD/MM/YYYY format)
    """
    twelve_hours_in_seconds: int = 43_200  # 12 hours in seconds
    ten_years_in_seconds: int = 315_360_000 + twelve_hours_in_seconds  # 3650 days in seconds
    current_time: int = int(datetime.now(timezone.utc).timestamp())  # unix format
    entered_date_unix: int = int(datetime.strptime(entered_date, '%d/%m/%Y').timestamp())

    if current_time - ten_years_in_seconds <= entered_date_unix <= current_time + twelve_hours_in_seconds:
        return True
    return False


async def check_date_in_correct_format(entered_date: str) -> bool:  # DD/MM/YYYY
    reg_exp = rf'^(0[1-9]|[1-2]\d|3[0-1])/(0[1-9]|1[0-2])/20[1-3]\d$'
    # month validation is not needed, inside the regular expression it is checked that the month is in the range 01-12.
    if re.match(reg_exp, entered_date):
        return True
    return False


async def check_day_is_correct(entered_year: int, entered_month: int, entered_day: int) -> bool:
    if 1 > entered_day > 31:
        return False

    if entered_month == 2:
        if await check_year_is_leap(entered_year) and entered_day <= 29:
            return True
        elif entered_day <= 28:
            return True
        return False
    elif entered_month in [1, 3, 5, 7, 8, 10, 12] and entered_day <= 31:
        return True
    elif entered_month in [4, 6, 9, 11] and entered_day <= 30:
        return True

    return False


async def check_year_is_leap(year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
        return True
    return False


def description_validation(description: str) -> bool:  # TODO
    if len(description) <= 50:
        return True
    return False


def value_validation(value: str) -> int:
    """
    Args:
        value: must be greater than 0
    Returns:
        int: int(number) if validation passed, returns 0 (False) if validation failed.
    """
    if re.match(r"^(?!0$)(?=.*\d)(?!0\d)\d{0,10}$", value):
        value: int = int(value)

        if value < 1000000000:
            return value
        return 0

    return 0


@timeit
def category_validation(lang: str, category: str) -> bool:
    categories: tuple = (
        f"{Dictionary.receive_translation(lang, "supermarkets")}",
        f"{Dictionary.receive_translation(lang, "restaurants")}",
        f"{Dictionary.receive_translation(lang, "clothes")}",
        f"{Dictionary.receive_translation(lang, "medicine")}",
        f"{Dictionary.receive_translation(lang, "transport")}",
        f"{Dictionary.receive_translation(lang, "devices")}",
        f"{Dictionary.receive_translation(lang, "education")}",
        f"{Dictionary.receive_translation(lang, "services")}",
        f"{Dictionary.receive_translation(lang, "travel")}",
        f"{Dictionary.receive_translation(lang, "housing")}",
        f"{Dictionary.receive_translation(lang, "transfer")}",
        f"{Dictionary.receive_translation(lang, "investments")}",
        f"{Dictionary.receive_translation(lang, "hobby")}",
        f"{Dictionary.receive_translation(lang, "jewelry")}",
        f"{Dictionary.receive_translation(lang, "salary")}",
        f"{Dictionary.receive_translation(lang, "charity")}",
        f"{Dictionary.receive_translation(lang, "other")}"
    )  # TODO: make a faster algorithm, although this one works within 0.00001 sec.

    if category in categories:
        return True
    return False

