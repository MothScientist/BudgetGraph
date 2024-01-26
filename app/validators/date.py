import asyncio
import re
from datetime import datetime, timezone


async def date_validation(entered_date: str) -> bool:  # entered date in format DD/MM/YYYY
    if not await check_date_in_correct_format(entered_date):
        return False
    _day: int = int(entered_date[:2])
    _month: int = int(entered_date[3:5])
    _year: int = int(entered_date[-4:])
    year_is_correct, day_is_correct = await asyncio.gather(
        check_day_is_correct(_year, _month, _day),  # DD
        check_year_is_correct(_year)  # YYYY
    )

    if year_is_correct and day_is_correct:
        return True
    return False


async def check_date_in_correct_format(entered_date: str) -> bool:  # DD/MM/YYYY
    reg_exp = rf'^(0[1-9]|[1-2]\d|3[0-1])/(0[1-9]|1[0-2])/20[1-3]\d$'
    # month validation is not needed, inside the regular expression it is checked that the month is in the range 01-12.
    if re.match(reg_exp, entered_date):
        return True
    return False


async def check_year_is_correct(entered_year: int) -> bool:
    current_year: int = datetime.now(timezone.utc).year
    if current_year - 10 <= entered_year <= current_year:
        return True
    return False


async def check_day_is_correct(entered_year: int, entered_month: int, entered_day: int) -> bool:
    if 1 > entered_day > 31:
        return False

    current_day: int = datetime.now(timezone.utc).day
    current_month: int = datetime.now(timezone.utc).month
    current_year: int = datetime.now(timezone.utc).year

    if current_year == entered_year and current_month == entered_month and entered_day > current_day:
        return False

    if entered_month == 2:
        if await check_year_is_leap(entered_year) and entered_day <= 29:
            return True
        elif entered_day <= 28:
            return True
        return False
    elif entered_month in [1, 3, 5, 7, 8, 10, 12] and current_day <= 31:  # 31
        return True
    elif entered_month in [4, 6, 9, 11] and current_day <= 30:  # 30
        return True
    return False


async def check_year_is_leap(year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
        return True
    return False
