import unittest
import asyncio
from datetime import datetime, timedelta

from validators.number import number_validation
from validators.description import description_validation
from validators.table_name import table_name_validation
from validators.date import (check_day_is_correct, check_year_is_leap, check_year_is_correct,
                                   check_date_in_correct_format, date_validation)


class TestDateValidation(unittest.TestCase):
    def test_day_1(self):  # today
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_day_2(self):  # a week ago
        week_ago = str(datetime.now().date() + timedelta(days=-7))
        day: int = int(week_ago[-2:])
        month: int = int(week_ago[5:7])
        year: int = int(week_ago[:4])
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_day_3(self):  # tomorrow
        tomorrow = str(datetime.now().date() + timedelta(days=1))
        day: int = int(tomorrow[-2:])
        month: int = int(tomorrow[5:7])
        year: int = int(tomorrow[:4])
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, False)

    def test_day_validator_4(self):  # leap year
        day: int = 29
        month: int = 2
        year: int = 2020
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_day_5(self):  # February 29th in non-leap years
        day: int = 29
        month: int = 2
        year: int = 2021
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, False)

    def test_day_6(self):  # yesterday
        yesterday = str(datetime.now().date() + timedelta(days=-1))
        day: int = int(yesterday[-2:])
        month: int = int(yesterday[5:7])
        year: int = int(yesterday[:4])
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_year_1(self):
        year: int = datetime.now().year
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_year_2(self):
        year: int = datetime.now().year - 10
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_year_3(self):
        year: int = datetime.now().year - 11
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, False)

    def test_year_4(self):
        year: int = datetime.now().year + 1
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, False)

    def test_year_5(self):
        year: int = datetime.now().year - 5
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
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_2(self):
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year + 1
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, False)

    def test_date_validation_3(self):
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year - 10
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_4(self):
        tomorrow = str(datetime.now().date() + timedelta(days=1))
        day: str = f"0{datetime.now().day}" if int(tomorrow[-2:]) < 10 else str(int(tomorrow[-2:]))
        month: str = f"0{datetime.now().month}" if int(tomorrow[5:7]) < 10 else str(int(tomorrow[5:7]))
        year: int = int(tomorrow[:4])
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, False)

    def test_date_validation_5(self):
        yesterday = str(datetime.now().date() + timedelta(days=-1))
        day: str = f"0{datetime.now().day}" if int(yesterday[-2:]) < 10 else str(int(yesterday[-2:]))
        month: str = f"0{datetime.now().month}" if int(yesterday[5:7]) < 10 else str(int(yesterday[5:7]))
        year: int = int(yesterday[:4])
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_6(self):
        res = asyncio.run(date_validation(""))
        self.assertEqual(res, False)

    def test_date_validation_7(self):
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{day}-{month}-{year}"))
        self.assertEqual(res, False)

    def test_date_validation_8(self):
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{year}/{month}/{day}"))
        self.assertEqual(res, False)

    def test_date_validation_9(self):
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{year}-{month}-{day}"))
        self.assertEqual(res, False)

    def test_date_validation_10(self):
        day: str = f"0{datetime.now().day}" if datetime.now().day < 10 else str(datetime.now().day)
        month: str = f"0{datetime.now().month}" if datetime.now().month < 10 else str(datetime.now().month)
        year: int = datetime.now().year + 1
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
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
    def test_table_name_validator_1(self):
        res = table_name_validation("budget_1")
        self.assertEqual(res, True)

    def test_table_name_validator_2(self):
        res = table_name_validation("budget_01")
        self.assertEqual(res, False)

    def test_table_name_validator_3(self):
        res = table_name_validation("budget_100")
        self.assertEqual(res, True)

    def test_table_name_validator_4(self):
        res = table_name_validation("budjet_10")
        self.assertEqual(res, False)

    def test_table_name_validator_5(self):
        res = table_name_validation("bubget_1")
        self.assertEqual(res, False)

    def test_table_name_validator_6(self):
        res = type(table_name_validation("bubget_1"))
        self.assertEqual(res, bool)

    def test_table_name_validator_7(self):
        res = type(table_name_validation("budget_100"))
        self.assertEqual(res, bool)

    def test_table_name_validator_8(self):
        res = table_name_validation("budget_0")
        self.assertEqual(res, False)

    def test_table_name_validator_9(self):
        res = table_name_validation("budget_")
        self.assertEqual(res, False)

    def test_table_name_validator_10(self):
        res = table_name_validation("budget")
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
