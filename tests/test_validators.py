# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import unittest
import asyncio
from os import listdir
from datetime import datetime, timedelta, timezone

from budget_graph.dictionary import receive_translation
from budget_graph.validation import (check_day_is_correct,
                                     check_year_is_leap,
                                     check_date_in_correct_format,
                                     comparison_dates_unix_format,
                                     description_validation,
                                     value_validation,
                                     date_validation,
                                     category_validation,
                                     telegram_id_validation,
                                     password_validation,
                                     username_validation)


class TestDateValidation(unittest.TestCase):
    # def test_day_is_correct_1(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_2(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_3(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_4(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_5(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_6(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_7(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_8(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_9(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )
    #
    # def test_day_is_correct_10(self):
    #     res = asyncio.run(check_day_is_correct(""))
    #     self.assertEqual(res, )

    # datetime.now(timezone.utc) + timedelta(days=1) and datetime.now(timezone.utc) - timedelta(days=3650)
    # There is no point in checking, since the result will differ due to time zones
    # TODO add separate tests for timezone (i.e. manually set timezone and time - and check

    def test_comparison_dates_unix_format_1(self):
        for day_delta in range(0, 120):  # TODO DOCUMENTATION
            _date = datetime.now(timezone.utc) - timedelta(days=day_delta)
            # Redefine the date in our format: DD/MM/YYYY
            redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
            res = asyncio.run(comparison_dates_unix_format(redefine_date))
            self.assertEqual(res, True)

    def test_comparison_dates_unix_format_2(self):
        for day_delta in range(3250, 3650):  # TODO DOCUMENTATION
            _date = datetime.now(timezone.utc) - timedelta(days=day_delta)
            # Redefine the date in our format: DD/MM/YYYY
            redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
            res = asyncio.run(comparison_dates_unix_format(redefine_date))
            self.assertEqual(res, True)

    def test_comparison_dates_unix_format_3(self):
        for day_delta in range(2, 120):  # TODO DOCUMENTATION
            _date = datetime.now(timezone.utc) + timedelta(days=day_delta)
            # Redefine the date in our format: DD/MM/YYYY
            redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
            res = asyncio.run(comparison_dates_unix_format(redefine_date))
            self.assertEqual(res, False)

    def test_comparison_dates_unix_format_4(self):
        for day_delta in range(3651, 3700):  # TODO DOCUMENTATION
            _date = datetime.now(timezone.utc) - timedelta(days=day_delta)
            # Redefine the date in our format: DD/MM/YYYY
            redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
            res = asyncio.run(comparison_dates_unix_format(redefine_date))
            self.assertEqual(res, False)

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

    def test_leap_year_6(self):
        res = asyncio.run(check_year_is_leap(2028))
        self.assertEqual(res, True)

    def test_leap_year_7(self):
        res = asyncio.run(check_year_is_leap(2030))
        self.assertEqual(res, False)

    def test_leap_year_8(self):
        res = asyncio.run(check_year_is_leap(2032))
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
        yesterday = datetime.now(timezone.utc) + timedelta(days=-1)
        yesterday_day_month: str = yesterday.strftime('%d/%m')
        year: int = int(yesterday.strftime('%Y'))
        res = asyncio.run(date_validation(f"{yesterday_day_month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_4(self):
        res = asyncio.run(date_validation(""))
        self.assertEqual(res, False)

    def test_date_validation_5(self):
        current_date = datetime.now(timezone.utc).strftime('%d-%m-%Y')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_6(self):
        current_date = datetime.now(timezone.utc).strftime('%Y/%m/%d')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_7(self):
        current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_8(self):
        current_date = datetime.now(timezone.utc)
        current_day_month: str = current_date.strftime('%d/%m')
        year: int = int(current_date.strftime('%Y')) + 1
        res = asyncio.run(date_validation(f"{current_day_month}/{year}"))
        self.assertEqual(res, False)


class TestRegistrationValidation(unittest.TestCase):
    def test_telegram_id_1(self):
        res = asyncio.run(telegram_id_validation("99"))  # 2
        self.assertEqual(res, False)

    def test_telegram_id_2(self):
        res = asyncio.run(telegram_id_validation("100"))  # 3
        self.assertEqual(res, True)

    def test_telegram_id_3(self):
        res = asyncio.run(telegram_id_validation("0"))
        self.assertEqual(res, False)

    def test_telegram_id_4(self):
        res = asyncio.run(telegram_id_validation("00000"))
        self.assertEqual(res, False)

    def test_telegram_id_5(self):
        res = asyncio.run(telegram_id_validation("100oo"))
        self.assertEqual(res, False)

    def test_telegram_id_6(self):
        res = asyncio.run(telegram_id_validation("123456781942"))  # 12
        self.assertEqual(res, True)

    def test_telegram_id_7(self):
        res = asyncio.run(telegram_id_validation("1232456784192"))  # 13
        self.assertEqual(res, False)

    def test_telegram_id_8(self):
        res = asyncio.run(telegram_id_validation("5"))  # 1
        self.assertEqual(res, False)


class TestNumberValidation(unittest.TestCase):
    def test_number_validation_1(self):
        res: int = value_validation("999999999")
        self.assertEqual(res, 999999999)

    def test_number_validation_2(self):
        res: int = value_validation("1000000000")
        self.assertEqual(res, 0)

    def test_number_validation_3(self):
        res: int = value_validation("1000000001")
        self.assertEqual(res, 0)

    def test_number_validation_4(self):
        res: int = value_validation("0")
        self.assertEqual(res, 0)

    def test_number_validation_5(self):
        res: int = value_validation("1o")
        self.assertEqual(res, 0)

    def test_number_validation_6(self):
        res: int = value_validation("100a")
        self.assertEqual(res, 0)

    def test_number_validation_7(self):
        res: int = value_validation("01")
        self.assertEqual(res, 0)

    def test_number_validation_8(self):
        res: int = value_validation("010")
        self.assertEqual(res, 0)

    def test_number_validation_9(self):
        res: int = value_validation("")
        self.assertEqual(res, 0)

    def test_number_validation_10(self):
        res: int = value_validation("00")
        self.assertEqual(res, 0)

    def test_number_validation_11(self):
        res: int = value_validation("100_000")
        self.assertEqual(res, 0)

    def test_number_validation_12(self):
        for value in range(0, 1_500_000):
            res: int = value_validation(str(value))
            self.assertEqual(res, value)

    def test_number_validation_13(self):
        for value in range(10_000_000, 11_250_000):
            res: int = value_validation(str(value))
            self.assertEqual(res, value)

    def test_number_validation_14(self):
        for value in range(999_999_999, 998_500_000, -1):
            res: int = value_validation(str(value))
            self.assertEqual(res, value)

    def test_number_validation_15(self):
        for value in range(1_000_000_000, 1_000_500_000):
            res: int = value_validation(str(value))
            self.assertEqual(res, 0)


class TestDescriptionValidator(unittest.TestCase):
    def test_description_validator_1(self):
        res = description_validation("")
        self.assertEqual(res, True)

    def test_description_validator_2(self):
        res = description_validation("The clarity of our position is obvious: modern de")  # 49
        self.assertEqual(res, True)

    def test_description_validator_3(self):
        res = description_validation("The clarity of our position is obvious: modern dev")  # 50
        self.assertEqual(res, True)

    def test_description_validator_4(self):
        res = description_validation("The clarity of our position is obvious: modern deve")  # 51
        self.assertEqual(res, False)


class TestCategoryValidation(unittest.TestCase):
    def test_category_validation_1(self):  # All categories for all localization
        categories: tuple = ("supermarkets", "restaurants", "clothes", "medicine", "transport", "devices", "education",
                             "services", "travel", "housing", "investments", "hobby", "jewelry", "salary", "charity",
                             "other")
        localization_files: tuple = tuple(listdir('../budget_graph/localization'))
        languages: tuple = tuple(lang[:2] for lang in localization_files)
        # Now we check that they all pass validation
        res: bool = all(category_validation(lang, receive_translation(lang, category)) for lang in languages for category in categories)  # noqa
        self.assertEqual(res, True)

    def test_category_validation_2(self):  # The phrase exists, but in a different language
        res: bool = category_validation("en", "Viajar")
        self.assertEqual(res, False)

    def test_category_validation_3(self):  # The language is in the dictionary, but there is no phrase
        res: bool = category_validation("is", "Dictionary")
        self.assertEqual(res, False)

    def test_category_validation_4(self):  # Typo in phrase
        res: bool = category_validation("en", "Service")  # 'Service', but in the dictionary 'Services'
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()
