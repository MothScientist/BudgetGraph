import unittest
import asyncio
from datetime import datetime, timedelta

from validators.number import number_validation
from validators.description import description_validation
from source.password_hashing import getting_hash, get_salt
from validators.table_name import table_name_validation
from token_generation import get_token
from validators.date import (check_day_is_correct, check_year_is_leap, check_month_is_correct, check_year_is_correct,
                             check_date_in_correct_format, date_validation)


class TestDateValidation(unittest.TestCase):
    def test_wrong_day_1(self):  # today
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_wrong_day_2(self):  # a week ago
        week_ago = str(datetime.now().date() + timedelta(days=-7))
        day: int = int(week_ago[-2:])
        month: int = int(week_ago[5:7])
        year: int = int(week_ago[:4])
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_wrong_day_3(self):  # tomorrow
        tomorrow = str(datetime.now().date() + timedelta(days=1))
        day: int = int(tomorrow[-2:])
        month: int = int(tomorrow[5:7])
        year: int = int(tomorrow[:4])
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, False)

    def test_wrong_day_4(self):  # leap year
        day: int = 29
        month: int = 2
        year: int = 2020
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_wrong_day_5(self):  # February 29th in non-leap years
        day: int = 29
        month: int = 2
        year: int = 2021
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, False)

    def test_wrong_day_6(self):  # yesterday
        yesterday = str(datetime.now().date() + timedelta(days=-1))
        day: int = int(yesterday[-2:])
        month: int = int(yesterday[5:7])
        year: int = int(yesterday[:4])
        res = asyncio.run(check_day_is_correct(year, month, day))
        self.assertEqual(res, True)

    def test_wrong_month_1(self):
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(check_month_is_correct(month, year))
        self.assertEqual(res, True)

    def test_wrong_month_2(self):
        tomorrow = str(datetime.now().date() + timedelta(days=31))
        month: int = int(tomorrow[5:7])
        year: int = int(tomorrow[:4])
        res = asyncio.run(check_month_is_correct(month, year))
        self.assertEqual(res, False)

    def test_wrong_month_3(self):
        month: int = 13
        year: int = 2020
        res = asyncio.run(check_month_is_correct(month, year))
        self.assertEqual(res, False)

    def test_wrong_month_4(self):
        month: int = 0
        year: int = 2019
        res = asyncio.run(check_month_is_correct(month, year))
        self.assertEqual(res, False)

    def test_wrong_month_5(self):
        month: int = 6
        year: int = 2025
        res = asyncio.run(check_month_is_correct(month, year))
        self.assertEqual(res, True)

    def test_wrong_year_1(self):
        year: int = datetime.now().year
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_wrong_year_2(self):
        year: int = datetime.now().year - 10
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, True)

    def test_wrong_year_3(self):
        year: int = datetime.now().year - 11
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, False)

    def test_wrong_year_4(self):
        year: int = datetime.now().year + 1
        res = asyncio.run(check_year_is_correct(year))
        self.assertEqual(res, False)

    def test_wrong_year_5(self):
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
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_2(self):
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year + 1
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, False)

    def test_date_validation_3(self):
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year - 10
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_4(self):
        tomorrow = str(datetime.now().date() + timedelta(days=1))
        day: int = int(tomorrow[-2:])
        month: int = int(tomorrow[5:7])
        year: int = int(tomorrow[:4])
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, False)

    def test_date_validation_5(self):
        yesterday = str(datetime.now().date() + timedelta(days=-1))
        day: int = int(yesterday[-2:])
        month: int = int(yesterday[5:7])
        year: int = int(yesterday[:4])
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_6(self):
        res = asyncio.run(date_validation(""))
        self.assertEqual(res, False)

    def test_date_validation_7(self):
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{day}-{month}-{year}"))
        self.assertEqual(res, False)

    def test_date_validation_8(self):
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{year}/{month}/{day}"))
        self.assertEqual(res, False)

    def test_date_validation_9(self):
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year
        res = asyncio.run(date_validation(f"{year}-{month}-{day}"))
        self.assertEqual(res, False)

    def test_date_validation_10(self):
        day: int = datetime.now().day
        month: int = datetime.now().month
        year: int = datetime.now().year + 1
        res = asyncio.run(date_validation(f"{day}/{month}/{year}"))
        self.assertEqual(res, False)


class TestRegistrationValidation(unittest.TestCase):
    def test_wrong_telegram_id_1(self):
        pass

    def test_wrong_password_1(self):
        pass

    def test_wrong_username_1(self):
        pass

    def test_telegram_id_not_unique_1(self):
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


class TestPasswordHashing(unittest.TestCase):
    def test_get_salt_1(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_2(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_3(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_4(self):
        res = len(get_salt(key_length=64))
        self.assertEqual(res, 64)

    def test_get_salt_5(self):
        res = len(get_salt(key_length=16))
        self.assertEqual(res, 16)

    def test_get_salt_6(self):
        res = type(get_salt())
        self.assertEqual(res, str)

    def test_get_salt_7(self):
        res = type(get_salt(key_length=16))
        self.assertEqual(res, str)

    def test_get_salt_8(self):
        res = type(get_salt(key_length=64))
        self.assertEqual(res, str)

    def test_getting_hash_1(self):
        res = getting_hash("test", "test")
        self.assertEqual(res, "cef5c5a0f141fa3161a580ab2f7a64f895a60c335861f9fdcef51cf84f5c9527")

    def test_getting_hash_2(self):
        res = getting_hash("1234567890", "qwerty")
        self.assertEqual(res, "04bee6f8d78036f0d12a2c3738ae8d28f92e86dac1c750ea89b9f719ea48ad03")

    def test_getting_hash_3(self):
        res = getting_hash("", "")
        self.assertEqual(res, "d38c83c56f0d40fbfab593058b4227de0ab71f0907f87f0d99c108c05e9c1065")

    def test_getting_hash_4(self):
        res = type(getting_hash("", ""))
        self.assertEqual(res, str)

    def test_getting_hash_5(self):
        res = type(getting_hash("qwertyqwertyqwerty", "123qwerty123qwerty123qwerty"))
        self.assertEqual(res, str)


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


class TestTokenGeneration(unittest.TestCase):
    def test_get_token_1(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_2(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_3(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_4(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_5(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_6(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_7(self):
        res = len(get_token(key_length_bytes=30))
        self.assertEqual(res, 60)

    def test_get_token_8(self):
        res = len(get_token(key_length_bytes=50))
        self.assertEqual(res, 100)

    def test_get_token_9(self):
        res = len(get_token(key_length_bytes=120))
        self.assertEqual(res, 240)

    def test_get_token_10(self):
        res = len(get_token(key_length_bytes=8))
        self.assertEqual(res, 16)


if __name__ == '__main__':
    unittest.main()
