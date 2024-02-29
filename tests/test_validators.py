import unittest
import asyncio
import re
from datetime import datetime, timedelta, timezone

from app.validation import (check_day_is_correct,
                            check_year_is_leap,
                            check_date_in_correct_format,
                            comparison_dates_unix_format,
                            description_validation,
                            value_validation,
                            date_validation,
                            category_validation)

from app.dictionary import Dictionary


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

    def test_comparison_dates_unix_format_1(self):
        _date = datetime.now(timezone.utc) + timedelta(days=-1)
        # Redefine the date in our format: DD/MM/YYYY
        redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
        res = asyncio.run(comparison_dates_unix_format(redefine_date))
        self.assertEqual(res, True)

    def test_comparison_dates_unix_format_2(self):
        _date = datetime.now(timezone.utc)
        # Redefine the date in our format: DD/MM/YYYY
        redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
        res = asyncio.run(comparison_dates_unix_format(redefine_date))
        self.assertEqual(res, True)

    # timedelta(days=1) There is no point in checking, since the result will differ due to time zones

    def test_comparison_dates_unix_format_3(self):
        _date = datetime.now(timezone.utc) + timedelta(days=2)
        # Redefine the date in our format: DD/MM/YYYY
        redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
        res = asyncio.run(comparison_dates_unix_format(redefine_date))
        self.assertEqual(res, False)

    def test_comparison_dates_unix_format_4(self):
        _date = datetime.now(timezone.utc) - timedelta(days=3649)
        # Redefine the date in our format: DD/MM/YYYY
        redefine_date: str = f"{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}"
        res = asyncio.run(comparison_dates_unix_format(redefine_date))
        self.assertEqual(res, True)

    # timedelta(days=3650) There is no point in checking, since the result will differ due to time zones

    def test_comparison_dates_unix_format_5(self):
        _date = datetime.now(timezone.utc) - timedelta(days=3651)
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
        tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)
        tomorrow_day: str = tomorrow.strftime('%d')
        month: str = tomorrow.strftime('%m')
        year: int = int(tomorrow.strftime('%Y'))
        res = asyncio.run(date_validation(f"{tomorrow_day}/{month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_4(self):
        yesterday = datetime.now(timezone.utc) + timedelta(days=-1)
        yesterday_day_month: str = yesterday.strftime('%d/%m')
        year: int = int(yesterday.strftime('%Y'))
        res = asyncio.run(date_validation(f"{yesterday_day_month}/{year}"))
        self.assertEqual(res, True)

    def test_date_validation_5(self):
        res = asyncio.run(date_validation(""))
        self.assertEqual(res, False)

    def test_date_validation_6(self):
        current_date = datetime.now(timezone.utc).strftime('%d-%m-%Y')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_7(self):
        current_date = datetime.now(timezone.utc).strftime('%Y/%m/%d')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_8(self):
        current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        res = asyncio.run(date_validation(current_date))
        self.assertEqual(res, False)

    def test_date_validation_9(self):
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
        res: int = value_validation("100aaa0")
        self.assertEqual(res, 0)

    def test_number_validation_2(self):
        res: int = value_validation("0")
        self.assertEqual(res, 0)

    def test_number_validation_3(self):
        res: int = value_validation("1o")
        self.assertEqual(res, 0)


class TestDescriptionValidator(unittest.TestCase):
    def test_description_validator_1(self):
        res = description_validation("")
        self.assertEqual(res, True)


class TestTableNameValidator(unittest.TestCase):  # TODO delete after changing data storage concept
    """
    Used in the create_table_group() function in db_manager.py
    """
    def test_table_name_validator_1(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budget_1") else False
        self.assertEqual(res, True)

    def test_table_name_validator_2(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budget_01") else False
        self.assertEqual(res, False)

    def test_table_name_validator_3(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budget_100") else False
        self.assertEqual(res, True)

    def test_table_name_validator_4(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budjet_10") else False
        self.assertEqual(res, False)

    def test_table_name_validator_5(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "bubget_1") else False
        self.assertEqual(res, False)

    def test_table_name_validator_6(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budget_0") else False
        self.assertEqual(res, False)

    def test_table_name_validator_7(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budget_") else False
        self.assertEqual(res, False)

    def test_table_name_validator_8(self):
        res: bool = True if re.match(r"^budget_[1-9]\d{0,4}$", "budget") else False
        self.assertEqual(res, False)


class TestCategoryValidation(unittest.TestCase):
    def test_category_validation_1(self):  # All categories for all languages
        categories_keys: tuple = ("supermarkets", "restaurants", "clothes", "medicine", "transport",
                                  "devices", "education", "services", "travel", "housing", "investments",
                                  "hobby", "jewelry", "salary", "charity", "other")

        _languages: tuple = tuple(Dictionary._languages.keys())

        # We get all the values by keys (tuple above) from all language dictionaries
        categories_values: tuple = tuple(Dictionary._languages[lang][_key] for lang in _languages for _key in categories_keys)  # noqa

        # Now we check that they all pass validation
        res: bool = all(category_validation(lang, Dictionary.receive_translation(lang, category)) for lang in _languages for category in categories_keys)  # noqa
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
