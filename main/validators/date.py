import asyncio
import re
from datetime import date

# Timeit decorator
from time_checking import timeit


@timeit
async def date_validation(entered_date: str) -> bool:  # entered date in format YYYY-MM-DD (
    if not await check_date_in_correct_format(entered_date):
        return False

    _day: str = entered_date[:2]
    _month: str = entered_date[3:5]
    _year: str = entered_date[-4:]

    year_is_correct, month_is_correct, day_is_correct = await asyncio.gather(
        check_day_is_correct(_year, _month, _day),  # DD
        check_month_is_correct(_month),  # MM
        check_year_is_correct(_year)  # YYYY
    )

    if year_is_correct and month_is_correct and day_is_correct:
        return True
    else:
        return False


async def check_date_in_correct_format(entered_date: str) -> bool:  # YYYY-MM-DD
    if re.match(r'^(0|1|2|3)\d/(0|1)\d/20(1|2)\d$', entered_date):
        return True
    return False


async def check_year_is_correct(year: str) -> bool:
    current_year: str = str(date. today())[:4]
    entered_year: int = int(year)
    if int(current_year) - 10 <= entered_year <= int(current_year):
        return True
    else:
        return False


async def check_month_is_correct(month: str) -> bool:
    entered_month: int = int(month)
    if 1 <= entered_month <= 12:
        return True
    else:
        return False


async def check_day_is_correct(year: str, month: str, day: str) -> bool:
    entered_day: int = int(day)
    if 1 <= entered_day <= 31:
        return True
    else:
        return False


async def check_year_is_leap(year: str) -> bool:
    pass
