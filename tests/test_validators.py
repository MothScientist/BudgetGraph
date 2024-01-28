import unittest
import asyncio
import re
from datetime import datetime, timedelta, timezone

from app.validation import (check_day_is_correct,
                            check_year_is_leap,
                            check_year_is_correct,
                            check_date_in_correct_format,
                            description_validation,
                            number_validation,
                            date_validation)


class TestDateValidation(unittest.TestCase):
    def test_day_1(self):  # today
        current_date = datetime.now(timezone.utc)
        day: int = int(current_date.strftime('%d'))
        month: int = int(current_date.strftime('%m'))
        year: int = int(current_date.strftime('%Y'))
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_day_2(self):  # a week ago
        week_ago = datetime.now(timezone.utc) + timedelta(days=-7)
        day: int = int(week_ago.strftime('%d'))
        month: int = int(week_ago.strftime('%m'))
        year: int = int(week_ago.strftime('%Y'))
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_day_3(self):  # tomorrow
        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
        day: int = int(tomorrow.strftime('%d'))
        month: int = int(tomorrow.strftime('%m'))
        year: int = int(tomorrow.strftime('%Y'))
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, False)

    def test_day_validator_4(self):  # leap year
        res = asyncio.run(check_day_is_correct(2020, 2, 29))
        self.assertEqual(res, True)

    def test_day_5(self):  # February 29th in non-leap years
        res = asyncio.run(check_day_is_correct(2021, 2, 29))
        self.assertEqual(res, False)

    def test_day_6(self):  # yesterday
        yesterday = datetime.now(timezone.utc) + timedelta(days=-1)
        day: int = int(yesterday.strftime('%d'))
        month: int = int(yesterday.strftime('%m'))
        year: int = int(yesterday.strftime('%Y'))
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_year_1(self):
        year: int = datetime.now(timezone.utc).year
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_year_2(self):
        year: int = datetime.now(timezone.utc).year - 10
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_year_3(self):
        year: int = datetime.now(timezone.utc).year - 11
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, False)

    def test_year_4(self):
        year: int = datetime.now(timezone.utc).year + 1
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, False)

    def test_year_5(self):
        year: int = datetime.now(timezone.utc).year - 5
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_leap_year_1(self):
        res = asyncio.run(check_year_is_leap(2020))
        self.assertEqual(res, True)

    def test_leap_year_2(self):
        res = asyncio.run(check_year_is_leap(2000))
        self.assertEqual(res, True)

    def test_leap_year_3(self):
        res = asyncio.run(check_year_is_leap(2100))
        self.assertEqual(res, False)

    def test_leap_year_4(self):
        res = asyncio.run(check_year_is_leap(2025))
        self.assertEqual(res, False)

    def test_leap_year_5(self):
        res = asyncio.run(check_year_is_leap(2024))
        self.assertEqual(res, True)

    def test_check_date_in_correct_format_1(self):
        res = asyncio.run(check_date_in_correct_format("01/01/2020"))
        self.assertEqual(res, True)

    def test_check_date_in_correct_format_2(self):
        res = asyncio.run(check_date_in_correct_format("32/01/2024"))
        self.assertEqual(res, False)

    def test_check_date_in_correct_format_3(self):
        res = asyncio.run(check_date_in_correct_format("30/01/2015"))
        self.assertEqual(res, True)

    def test_check_date_in_correct_format_4(self):
        res = asyncio.run(check_date_in_correct_format("01/01/2005"))
        self.assertEqual(res, False)

    def test_check_date_in_correct_format_5(self):
        res = asyncio.run(check_date_in_correct_format("01/14/2015"))
        self.assertEqual(res, False)

    def test_check_date_in_correct_format_6(self):
        res = asyncio.run(check_date_in_correct_format("01/12/2015"))
        self.assertEqual(res, True)

    def test_check_date_in_correct_format_7(self):
        res = asyncio.run(check_date_in_correct_format("12/05/2019"))
        self.assertEqual(res, True)

    def test_check_date_in_correct_format_8(self):
        res = asyncio.run(check_date_in_correct_format("31/11/2018"))
        self.assertEqual(res, True)

    def test_check_date_in_correct_format_9(self):
        res = asyncio.run(check_date_in_correct_format("01/00/2017"))
        self.assertEqual(res, False)

    def test_check_date_in_correct_format_10(self):
        res = asyncio.run(check_date_in_correct_format("00/12/2017"))
        self.assertEqual(res, False)

    def test_date_validation_1(self):
        current_date = datetime.now(timezone.utc).strftime('%d/%m/%Y')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, True)

    def test_date_validation_2(self):
        current_date = datetime.now(timezone.utc)
        current_day_month: str = current_date.strftime('%d/%m')
        year: int = int(current_date.strftime('%Y')) + 1
        res = asyncio.run(date_validation(f"{current_day_month}/{year}"))
        self.assertEqual(res, False)

    def test_date_validation_3(self):
        current_date = datetime.now(timezone.utc)
        current_day_month: str = current_date.strftime('%d/%m')
        year: int = int(current_date.strftime('%Y')) - 10
        res = asyncio.run(date_validation(f"{current_day_month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_4(self):
        tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)
        tomorrow_day_month: str = tomorrow.strftime('%d/%m')
        year: int = int(tomorrow.strftime('%Y'))
        res = asyncio.run(date_validation(f"{tomorrow_day_month}/{year}"))
        self.assertEqual(res, False)

    def test_date_validation_5(self):
        yesterday = datetime.now(timezone.utc) + timedelta(days=-1)
        yesterday_day_month: str = yesterday.strftime('%d/%m')
        year: int = int(yesterday.strftime('%Y'))
        res = asyncio.run(date_validation(f"{yesterday_day_month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_6(self):
        res = asyncio.run(date_validation(""))
        self.assertEqual(res, False)

    def test_date_validation_7(self):
        current_date = datetime.now(timezone.utc).strftime('%d-%m-%Y')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_8(self):
        current_date = datetime.now(timezone.utc).strftime('%Y/%m/%d')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_9(self):
        current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_10(self):
        current_date = datetime.now(timezone.utc)
        current_day_month: str = current_date.strftime('%d/%m')
        year: int = int(current_date.strftime('%Y')) + 1
        res = asyncio.run(date_validation(f"{current_day_month}/{year}"))
        self.assertEqual(res, False)


class TestRegistrationValidation(unittest.TestCase):
    def test_telegram_id_1(self):
        pass

    def test_password_1(self):
        pass

    def test_username_1(self):
        pass

    def test_telegram_id_unique_1(self):
        pass


class TestNumberValidation(unittest.TestCase):
    def test_number_validation_1(self):
        res = number_validation("100aaa0")
        self.assertEqual(res, 0)

    def test_number_validation_2(self):
        res = number_validation("0")
        self.assertEqual(res, 0)

    def test_number_validation_3(self):
        res = number_validation("1o")
        self.assertEqual(res, 0)


class TestDescriptionValidator(unittest.TestCase):
    def test_description_validator_1(self):
        res = description_validation("")
        self.assertEqual(res, True)


class TestTableNameValidator(unittest.TestCase):
    """
    Used in the create_table_group() function in database_control.py
    """
    def test_table_name_validator_1(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budget_1")
        self.assertEqual(res, True)

    def test_table_name_validator_2(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budget_01")
        self.assertEqual(res, False)

    def test_table_name_validator_3(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budget_100")
        self.assertEqual(res, True)

    def test_table_name_validator_4(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budjet_10")
        self.assertEqual(res, False)

    def test_table_name_validator_5(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "bubget_1")
        self.assertEqual(res, False)

    def test_table_name_validator_6(self):
        res = type(re.match(r"^budget_[1-9]\d{0,4}$", "bubget_1"))
        self.assertEqual(res, bool)

    def test_table_name_validator_7(self):
        res = type(re.match(r"^budget_[1-9]\d{0,4}$", "budget_100"))
        self.assertEqual(res, bool)

    def test_table_name_validator_8(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budget_0")
        self.assertEqual(res, False)

    def test_table_name_validator_9(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budget_")
        self.assertEqual(res, False)

    def test_table_name_validator_10(self):
        res = re.match(r"^budget_[1-9]\d{0,4}$", "budget")
        self.assertEqual(res, False)


class TestCategoryValidation(unittest.TestCase):
    def test_category_validation_1(self):
        pass

    def test_category_validation_2(self):
        pass

    def test_category_validation_3(self):
        pass

    def test_category_validation_4(self):
        pass

    def test_category_validation_5(self):
        pass


if __name__ == '__main__':
    unittest.main()
