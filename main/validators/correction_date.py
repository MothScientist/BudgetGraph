import asyncio
import re
from datetime import date

# Timeit decorator
from time_checking import timeit


@timeit
async def correction_date(entered_date: str) -> str:  # YYYY-MM-DD -> DD/MM/YYYY
    if not await date_in_correct_format(entered_date):
        entered_date: str = str(date. today())
        return f"{entered_date[-2:]}/{entered_date[5:7]}/{entered_date[:4]}"

    year, month, day = await asyncio.gather(
        correction_year(entered_date[:4]),  # YYYY
        correction_month(entered_date[5:7]),  # MM
        correction_day(entered_date[-2:])  # DD
    )

    return f"{day}/{month}/{year}"


async def date_in_correct_format(entered_date: str) -> bool:  # YYYY-MM-DD
    if re.match(r'^20(1|2)\d-(0|1)\d-(0|1|2|3)\d$', entered_date):
        return True
    return False


async def correction_year(year: str) -> str:
    current_year: str = str(date. today())[:4]
    entered_year: int = int(year)
    if int(current_year) - 10 <= entered_year <= int(current_year):
        return year
    else:
        return current_year


async def correction_month(month: str) -> str:
    current_month: str = str(date. today())[5:7]
    entered_month: int = int(month)
    if 1 <= entered_month <= 12:
        return month
    else:
        return current_month


async def correction_day(day: str) -> str:
    current_day: str = str(date. today())[-2:]
    entered_day: int = int(day)
    if 1 <= entered_day <= 31:
        return day
    else:
        return current_day
