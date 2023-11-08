import asyncio
import re
from datetime import datetime


async def date_validation(entered_date: str) -> bool:  # entered date in format YYYY-MM-DD (
    if not await check_date_in_correct_format(entered_date):
        return False

    _day: int = int(entered_date[:2])
    _month: int = int(entered_date[3:5])
    _year: int = int(entered_date[-4:])

    year_is_correct, month_is_correct, day_is_correct = await asyncio.gather(
        check_day_is_correct(_year, _month, _day),  # DD
        check_month_is_correct(_month, _year),  # MM
        check_year_is_correct(_year)  # YYYY
    )

    if year_is_correct and month_is_correct and day_is_correct:
        return True
    else:
        return False


async def check_date_in_correct_format(entered_date: str) -> bool:  # YYYY-MM-DD
    if re.match(r'^[0-3]\d/[0-1]\d/20[1-3]\d$', entered_date):
        return True
    return False


async def check_year_is_correct(entered_year: int) -> bool:
    current_year: int = datetime.now().year
    if current_year - 10 <= entered_year <= current_year:
        return True
    else:
        return False


async def check_month_is_correct(entered_month: int, entered_year: int) -> bool:
    if entered_month < 1 or entered_month > 12:
        return False

    current_month: int = datetime.now().month
    current_year: int = datetime.now().month

    if entered_year == current_year and entered_month > current_month:
        return False
    else:
        return True


async def check_day_is_correct(entered_year: int, entered_month: int, entered_day: int) -> bool:
    if 1 > entered_day > 31:
        return False

    current_day: int = datetime.now().day
    current_month: int = datetime.now().month
    current_year: int = datetime.now().year

    if current_year == entered_year and current_month == entered_month and entered_day <= current_day:
        return True

    if entered_month == 2:
        if check_year_is_leap(entered_year) and entered_day <= 29:
            return True
        elif entered_day <= 28:
            return True
    elif entered_month in [1, 3, 5, 7, 8, 10, 12] and current_day <= 31:  # 31
        return True
    elif entered_month in [4, 6, 9, 11] and current_day <= 30:  # 30
        return True
    else:
        return False


async def check_year_is_leap(year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
        return True
    else:
        return False
