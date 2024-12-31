from sys import path as sys_path
import re
from functools import cache
from datetime import datetime, timezone

sys_path.append('../')

from budget_graph.db_manager import DatabaseQueries, connect_db, close_db  # noqa
from budget_graph.dictionary import receive_translation  # noqa
from budget_graph.time_checking import timeit  # noqa


@timeit
async def registration_validation(username: str, psw: str, telegram_id: str) -> tuple[bool, int]:
    """
    :param username: 3 to 15 characters
    :param psw: 4 to 128 characters
    :param telegram_id:
    :return: If entered correctly, it will return True, otherwise it will issue a flash message and return False
    """
    if not await username_validation(username):
        return False, 1
    if not await password_validation(psw):
        return False, 2
    if not await telegram_id_validation(telegram_id):
        return False, 3
    return True, 0


async def username_validation(username: str) -> bool:
    connection = connect_db()
    dbase = DatabaseQueries(connection)
    username_is_exist: bool = dbase.check_username_is_exist(username)
    close_db(connection)

    if 3 <= len(username) <= 20 and re.match(r'^[a-zA-Z0-9]+$', username) and not username_is_exist:
        return True
    return False


async def password_validation(psw: str) -> bool:
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&_]{8,32}$', psw):
        return True
    return False


async def telegram_id_validation(telegram_id: str) -> bool:
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
    twelve_hours_in_seconds: int = 43_200  # 12 hours in seconds (time zone accounting)
    ten_years_in_seconds: int = 315_360_000  # 3650 days in seconds (10 years)
    time_diff: int = ten_years_in_seconds + twelve_hours_in_seconds
    current_time: int = int(datetime.now(timezone.utc).timestamp())  # unix format
    entered_date_unix: int = int(datetime.strptime(entered_date, '%d/%m/%Y').timestamp())

    if current_time - time_diff <= entered_date_unix <= current_time + twelve_hours_in_seconds:
        return True
    return False


async def check_date_in_correct_format(entered_date: str) -> bool:  # DD/MM/YYYY
    reg_exp = r'^(0[1-9]|[1-2]\d|3[0-1])/(0[1-9]|1[0-2])/20[1-3]\d$'
    # month validation is not needed, inside the regular expression it is checked that the month is in the range 01-12.
    if re.match(reg_exp, entered_date):
        return True
    return False


async def check_day_is_correct(entered_year: int, entered_month: int, entered_day: int) -> bool:
    if entered_day < 1 or entered_day > 31:
        return False

    if entered_month == 2:
        if await check_year_is_leap(entered_year):
            return entered_day <= 29
        return entered_day <= 28
    if entered_month in [1, 3, 5, 7, 8, 10, 12]:
        return entered_day <= 31
    if entered_month in [4, 6, 9, 11]:
        return entered_day <= 30
    return False


async def check_year_is_leap(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def description_validation(description: str) -> bool:  # TODO
    if not isinstance(description, str):
        description = str(description)
    return len(description) <= 50


def value_validation(value: str) -> int:
    """
    Args:
        value: must be greater than 0
    Returns:
        int: int(number) if validation passed, returns 0 (False) if validation failed.
    """
    if re.match(r"^(?!0$)(?=.*\d)(?!0\d)\d{0,10}$", value):
        value: int = int(value)
        if value < 100_000_000:
            return value
    return 0


@cache
def category_validation(lang: str, category: str) -> bool:
    categories: tuple = get_translations_for_categories(lang)
    return category in categories


@cache
def get_translations_for_categories(lang: str) -> tuple:
    categories: tuple = ("supermarkets", "restaurants", "clothes", "medicine", "transport", "devices", "education",
                         "services", "travel", "housing", "transfer", "investments", "hobby", "jewelry", "salary",
                         "charity", "other")
    categories_translate = tuple(receive_translation(lang, category) for category in categories)
    return categories_translate
