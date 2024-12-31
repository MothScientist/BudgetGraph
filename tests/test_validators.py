import unittest
from os import listdir
from string import ascii_letters
from random import choice
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
                                     username_validation,
                                     registration_validation)


class TestDateValidation(unittest.IsolatedAsyncioTestCase):

    datetime_now = datetime.now(timezone.utc)

    @staticmethod
    async def helper_day_delta(day_delta):
        return TestDateValidation.datetime_now - timedelta(days=day_delta)

    @staticmethod
    async def helper_redefine_date(_date):
        return f'{_date.strftime('%d')}/{_date.strftime('%m')}/{_date.strftime('%Y')}'

    async def test_day_is_correct_001(self):
        for day_delta in range(-500, 500):
            _date = await TestDateValidation.helper_day_delta(day_delta)
            _day: int = int(_date.strftime('%d'))
            _month: int = int(_date.strftime('%m'))
            _year: int = int(_date.strftime('%Y'))
            res = await check_day_is_correct(_year, _month, _day)
            full_date_view = await TestDateValidation.helper_redefine_date(_date)
            self.assertTrue(res, f'day_delta = {day_delta}\n'
                                f'date = {full_date_view}')

    async def test_day_is_correct_002(self):
        _years: tuple = (15, 17, 18, 19, 21, 22, 23, 25, 26, 27, 29, 30, 31, 33, 34, 35, 37, 38, 39, 41, 42, 43, 45, 46)
        _month: int = 2
        _day: int = 29
        for _year in _years:
            res = await check_day_is_correct(int(f'20{_year}'), _month, _day)
            self.assertFalse(res, f'20{_year}/{_month}/{_year}')

    async def test_day_is_correct_003(self):
        _day: int = 31
        for _year in range(1980, 2120):
            for _month in (4, 6, 9, 11):
                res = await check_day_is_correct(_year, _month, _day)
                self.assertFalse(res, f'{_year}/{_month}/{_day}')

    async def test_day_is_correct_004(self):
        _day: int = 30
        for _year in range(1980, 2120):
            for _month in (4, 6, 9, 11):
                res = await check_day_is_correct(_year, _month, _day)
                self.assertTrue(res, f'{_year}/{_month}/{_day}')

    async def test_day_is_correct_005(self):
        _day: int = 31
        for _year in range(1980, 2120):
            for _month in (1, 3, 5, 7, 8, 10, 12):
                res = await check_day_is_correct(_year, _month, _day)
                self.assertTrue(res, f'{_year}/{_month}/{_day}')

    async def test_day_is_correct_006(self):
        _day: int = 30
        for _year in range(1980, 2120):
            for _month in (1, 3, 5, 7, 8, 10, 12):
                res = await check_day_is_correct(_year, _month, _day)
                self.assertTrue(res, f'{_year}/{_month}/{_day}')

    async def test_day_is_correct_007(self):
        for _day in range(32, 500):
            for _year in range(1985, 2120):
                for _month in (1, 13):
                    res = await check_day_is_correct(_year, _month, _day)
                    self.assertFalse(res, f'{_year}/{_month}/{_day}')

    async def test_day_is_correct_008(self):
        for _day in range(-150, 1):
            for _year in range(1980, 2120):
                for _month in (1, 13):
                    res = await check_day_is_correct(_year, _month, _day)
                    self.assertFalse(res, f'{_year}/{_month}/{_day}')

    # datetime.now(timezone.utc) + timedelta(days=1) and datetime.now(timezone.utc) - timedelta(days=3650)
    # There is no point in checking, since the result will differ due to time zones

    async def test_comparison_dates_unix_format_001(self):
        for day_delta in range(120):
            _date = await TestDateValidation.helper_day_delta(day_delta)
            # Redefine the date in our format: DD/MM/YYYY
            redefine_date = await TestDateValidation.helper_redefine_date(_date)
            res = await comparison_dates_unix_format(redefine_date)
            self.assertTrue(res)

    async def test_comparison_dates_unix_format_002(self):
        for day_delta in range(3600, 3650):
            _date = await TestDateValidation.helper_day_delta(day_delta)
            redefine_date = await TestDateValidation.helper_redefine_date(_date)
            res = await comparison_dates_unix_format(redefine_date)
            self.assertTrue(res)

    async def test_comparison_dates_unix_format_003(self):
        for day_delta in range(2, 120):
            _date = await TestDateValidation.helper_day_delta(day_delta)
            redefine_date = await TestDateValidation.helper_redefine_date(_date)
            res = await comparison_dates_unix_format(redefine_date)
            self.assertTrue(res)

    async def test_comparison_dates_unix_format_004(self):
        for day_delta in range(3651, 3700):
            _date = await TestDateValidation.helper_day_delta(day_delta)
            redefine_date = await TestDateValidation.helper_redefine_date(_date)
            res = await comparison_dates_unix_format(redefine_date)
            self.assertFalse(res)

    async def test_leap_year_001(self):
        ''' Leap years '''
        for leap_year in (1600, 1992, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036, 2040, 2156, 2400):
            res = await check_year_is_leap(leap_year)
            self.assertTrue(res, leap_year)

    async def test_leap_year_002(self):
        ''' Non-leap years '''
        for non_leap_year in (1700, 1800, 1900, 2025, 2026, 2027, 2029, 2030, 2100, 2100, 2200, 2300, 2500, 2600):
            res = await check_year_is_leap(non_leap_year)
            self.assertFalse(res, non_leap_year)

    async def test_check_date_in_correct_format_001(self):
        res = await check_date_in_correct_format('01/01/2020')
        self.assertTrue(res)

    async def test_check_date_in_correct_format_002(self):
        res = await check_date_in_correct_format('32/01/2024')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_003(self):
        res = await check_date_in_correct_format('30/01/2015')
        self.assertTrue(res)

    async def test_check_date_in_correct_format_004(self):
        res = await check_date_in_correct_format('01/01/2005')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_005(self):
        res = await check_date_in_correct_format('01/14/2015')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_006(self):
        res = await check_date_in_correct_format('01/12/2015')
        self.assertTrue(res)

    async def test_check_date_in_correct_format_007(self):
        res = await check_date_in_correct_format('12/05/2019')
        self.assertTrue(res)

    async def test_check_date_in_correct_format_008(self):
        res = await check_date_in_correct_format('31/11/2018')
        self.assertTrue(res)

    async def test_check_date_in_correct_format_009(self):
        res = await check_date_in_correct_format('01/00/2017')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_010(self):
        res = await check_date_in_correct_format('00/12/2017')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_011(self):
        res = await check_date_in_correct_format('12/12/201')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_012(self):
        res = await check_date_in_correct_format('12/12/')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_013(self):
        res = await check_date_in_correct_format('12/12')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_014(self):
        res = await check_date_in_correct_format('12/2017')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_015(self):
        res = await check_date_in_correct_format('0101/2020')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_016(self):
        res = await check_date_in_correct_format('01.01.2020')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_017(self):
        res = await check_date_in_correct_format(r'01\01\2020')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_018(self):
        res = await check_date_in_correct_format('01/2020')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_019(self):
        res = await check_date_in_correct_format('01/00/2020')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_020(self):
        res = await check_date_in_correct_format('01/01/20200')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_021(self):
        for day in range(1, 10):
            for month in range(1, 3):
                for year in range(4):
                    res = await check_date_in_correct_format(f'0{day}/0{month}/202{year}')
                    self.assertTrue(res, f'0{day}/0{month}/202{year}')

    async def test_check_date_in_correct_format_022(self):
        for day in range(10):
            for month in range(3):
                for year in range(18, 23):
                    res = await check_date_in_correct_format(f'1{day}/1{month}/20{year}')
                    self.assertTrue(res, f'1{day}/1{month}/20{year}')

    async def test_check_date_in_correct_format_023(self):
        res = await check_date_in_correct_format('01012020')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_024(self):
        res = await check_date_in_correct_format('None')
        self.assertFalse(res)

    async def test_check_date_in_correct_format_025(self):
        res = await check_date_in_correct_format('')
        self.assertFalse(res)

    async def test_date_validation_001(self):
        current_date = TestDateValidation.datetime_now.strftime('%d/%m/%Y')
        res = await date_validation(current_date)
        self.assertTrue(res)

    async def test_date_validation_002(self):
        current_date = TestDateValidation.datetime_now
        current_day_month: str = current_date.strftime('%d/%m')
        year: int = int(current_date.strftime('%Y')) + 1
        res = await date_validation(f'{current_day_month}/{year}')
        self.assertFalse(res)

    async def test_date_validation_003(self):
        yesterday = TestDateValidation.datetime_now + timedelta(days=-1)
        yesterday_day_month: str = yesterday.strftime('%d/%m')
        year: int = int(yesterday.strftime('%Y'))
        res = await date_validation(f'{yesterday_day_month}/{year}')
        self.assertTrue(res)

    async def test_date_validation_004(self):
        res = await date_validation('')
        self.assertFalse(res)

    async def test_date_validation_005(self):
        current_date = TestDateValidation.datetime_now.strftime('%d-%m-%Y')
        res = await date_validation(current_date)
        self.assertFalse(res)

    async def test_date_validation_006(self):
        current_date = TestDateValidation.datetime_now.strftime('%Y/%m/%d')
        res = await date_validation(current_date)
        self.assertFalse(res)

    async def test_date_validation_007(self):
        current_date = TestDateValidation.datetime_now.strftime('%Y-%m-%d')
        res = await date_validation(current_date)
        self.assertFalse(res)

    async def test_date_validation_008(self):
        current_date = TestDateValidation.datetime_now
        current_day_month: str = current_date.strftime('%d/%m')
        year: int = int(current_date.strftime('%Y')) + 1
        res = await date_validation(f'{current_day_month}/{year}')
        self.assertFalse(res)

    async def test_date_validation_009(self):
        current_date = TestDateValidation.datetime_now.strftime('%d.%m.%Y')
        res = await date_validation(current_date)
        self.assertFalse(res)

    async def test_date_validation_010(self):
        current_date = TestDateValidation.datetime_now.strftime('%d/%m/%Y/')
        res = await date_validation(current_date)
        self.assertFalse(res)

    async def test_date_validation_011(self):
        current_date = TestDateValidation.datetime_now.strftime('%Y/%m/%d')
        res = await date_validation(current_date)
        self.assertFalse(res)

    async def test_date_validation_012(self):
        current_date = TestDateValidation.datetime_now.strftime('')
        res = await date_validation(current_date)
        self.assertFalse(res)


class TestRegistrationValidation(unittest.IsolatedAsyncioTestCase):
    ###########################################################################
    # Here it is enough to check that it returns correct error codes, since tests for validators are written separately

    async def test_registration_validation_001(self):
        res = await registration_validation('', '', '')
        self.assertFalse(res[0])

    async def test_registration_validation_002(self):
        res = await registration_validation('username', 'username_123', '12345')
        self.assertTrue(res[0])

    async def test_registration_validation_003(self):
        res = await registration_validation('username', 'username_123', '')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 3, res[1])

    async def test_registration_validation_005(self):
        res = await registration_validation('username', '', '12345')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 2, res[1])

    async def test_registration_validation_006(self):
        res = await registration_validation('', 'username_123', '12345')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 1, res[1])

    async def test_registration_validation_007(self):
        res = await registration_validation('', '', '12345')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 1, res)

    async def test_registration_validation_008(self):
        res = await registration_validation('username', '', '')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 2, res)

    async def test_registration_validation_009(self):
        res = await registration_validation('', 'username_123', '')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 1, res)

    async def test_registration_validation_010(self):
        res = await registration_validation('', '', '')
        self.assertFalse(res[0])
        self.assertEqual(res[1], 1, res)

    ###########################################################################

    async def test_telegram_id_001(self):
        res = await telegram_id_validation('99')  # 2
        self.assertFalse(res)

    async def test_telegram_id_002(self):
        res = await telegram_id_validation('100')  # 3
        self.assertTrue(res)

    async def test_telegram_id_003(self):
        res = await telegram_id_validation('0')
        self.assertFalse(res)

    async def test_telegram_id_004(self):
        res = await telegram_id_validation('00000')
        self.assertFalse(res)

    async def test_telegram_id_005(self):
        res = await telegram_id_validation('100oo')
        self.assertFalse(res)

    async def test_telegram_id_006(self):
        res = await telegram_id_validation('123456781942')  # 12
        self.assertTrue(res)

    async def test_telegram_id_007(self):
        res = await telegram_id_validation('1232456784192')  # 13
        self.assertFalse(res)

    async def test_telegram_id_008(self):
        res = await telegram_id_validation('5')  # 1
        self.assertFalse(res)

    async def test_telegram_id_009(self):
        for factor in range(2):
            res = await telegram_id_validation(str(10 ** factor))
            self.assertFalse(res, f'factor = {factor}')

    async def test_telegram_id_010(self):
        for factor in range(2, 12):
            res = await telegram_id_validation(str(10 ** factor))
            self.assertTrue(res, f'factor = {factor}')

    async def test_telegram_id_011(self):
        for factor in range(12, 25):
            res = await telegram_id_validation(str(10 ** factor))
            self.assertFalse(res, f'factor = {factor}')

    @staticmethod
    async def get_string_ascii_letters(length):
        random_string = ''.join(choice(ascii_letters) for _ in range(length))
        return random_string

    async def test_password_001(self):
        res = await password_validation('qwerty123')
        self.assertTrue(res)

    async def test_password_002(self):
        res = await password_validation('qwerty')
        self.assertFalse(res)

    async def test_password_003(self):
        res = await password_validation('strong_password')
        self.assertFalse(res)

    async def test_password_004(self):
        res = await password_validation('strong_password_123456789')
        self.assertTrue(res)

    async def test_password_005(self):
        for i in range(100_000_000, 100_050_000):
            res = await password_validation(str(i))
            self.assertFalse(res)

    async def test_password_006(self):
        for length in range(1_000):
            password = await TestRegistrationValidation.get_string_ascii_letters(length)
            res = await password_validation(password)
            self.assertFalse(res)

    async def test_password_007(self):
        res = await password_validation('')
        self.assertFalse(res)

    async def test_password_008(self):
        res = await password_validation('strong_password_123456789_strong_password_123456789_strong_password_123456789')
        self.assertFalse(res)

    async def test_password_009(self):
        res = await password_validation('___________________________________________________________')
        self.assertFalse(res)

    async def test_password_010(self):
        res = await password_validation('                                      ')
        self.assertFalse(res)


class TestNumberValidation(unittest.TestCase):
    def test_number_validation_001(self):
        res: int = value_validation('99999999')
        self.assertEqual(res, 99_999_999)

    def test_number_validation_002(self):
        res: int = value_validation('1000000000')
        self.assertEqual(res, 0)

    def test_number_validation_003(self):
        res: int = value_validation('1000000001')
        self.assertEqual(res, 0)

    def test_number_validation_004(self):
        res: int = value_validation('0')
        self.assertEqual(res, 0)

    def test_number_validation_005(self):
        res: int = value_validation('1o')
        self.assertEqual(res, 0)

    def test_number_validation_006(self):
        res: int = value_validation('100a')
        self.assertEqual(res, 0)

    def test_number_validation_007(self):
        res: int = value_validation('01')
        self.assertEqual(res, 0)

    def test_number_validation_008(self):
        res: int = value_validation('010')
        self.assertEqual(res, 0)

    def test_number_validation_009(self):
        res: int = value_validation('')
        self.assertEqual(res, 0)

    def test_number_validation_010(self):
        res: int = value_validation('00')
        self.assertEqual(res, 0)

    def test_number_validation_011(self):
        res: int = value_validation('100_000')
        self.assertEqual(res, 0)

    def test_number_validation_012(self):
        for value in range(125_000):
            res: int = value_validation(str(value))
            self.assertEqual(res, value)

    def test_number_validation_013(self):
        for value in range(1_000_000, 1_050_000):
            res: int = value_validation(str(value))
            self.assertEqual(res, value)

    def test_number_validation_014(self):
        for value in range(99_999_999, 99_975_000, -1):
            res: int = value_validation(str(value))
            self.assertEqual(res, value)

    def test_number_validation_015(self):
        for value in range(100_000_000, 100_025_000):
            res: int = value_validation(str(value))
            self.assertEqual(res, 0)

    def test_number_validation_016(self):
        res: int = value_validation('')
        self.assertEqual(res, 0)

    def test_number_validation_017(self):
        res: int = value_validation('None')
        self.assertEqual(res, 0)

    def test_number_validation_018(self):
        res: int = value_validation('qwerty_qwerty_qwerty_qwerty_qwerty')
        self.assertEqual(res, 0)

    def test_number_validation_019(self):
        value: int = 500_000
        res: int = value_validation(str(value))
        self.assertEqual(res, value)

    def test_number_validation_020(self):
        value: int = 980_123
        res: int = value_validation(str(value))
        self.assertEqual(res, value)

    def test_number_validation_021(self):
        value: float = 100.00
        res: int = value_validation(str(value))
        self.assertEqual(res, 0)

    def test_number_validation_022(self):
        value: float = 1250.50
        res: int = value_validation(str(value))
        self.assertEqual(res, 0)


class TestDescriptionValidator(unittest.TestCase):
    def test_description_validator_001(self):
        res = description_validation('')
        self.assertTrue(res)

    def test_description_validator_002(self):
        res = description_validation('The clarity of our position is obvious: modern de')  # 49
        self.assertTrue(res)

    def test_description_validator_003(self):
        res = description_validation('The clarity of our position is obvious: modern dev')  # 50
        self.assertTrue(res)

    def test_description_validator_004(self):
        res = description_validation('The clarity of our position is obvious: modern deve')  # 51
        self.assertFalse(res)


class TestCategoryValidation(unittest.TestCase):
    def test_category_validation_001(self):  # All categories for all localization
        categories: tuple = ('supermarkets', 'restaurants', 'clothes', 'medicine', 'transport', 'devices', 'education',
                             'services', 'travel', 'housing', 'investments', 'hobby', 'jewelry', 'salary', 'charity',
                             'other')
        localization_files: tuple = tuple(listdir('../budget_graph/localization'))
        languages: tuple = tuple(lang[:2] for lang in localization_files)
        # Now we check that they all pass validation
        res: bool = all(category_validation(lang, receive_translation(lang, category)) for lang in languages for category in categories)  # noqa
        self.assertTrue(res)

    def test_category_validation_002(self):  # The phrase exists, but in a different language
        res: bool = category_validation('en', 'Viajar')
        self.assertFalse(res)

    def test_category_validation_003(self):  # The language is in the dictionary, but there is no phrase
        res: bool = category_validation('is', 'Dictionary')
        self.assertFalse(res)

    def test_category_validation_004(self):  # Typo in phrase
        res: bool = category_validation('en', 'Service')  # 'Service', but in the dictionary 'Services'
        self.assertFalse(res)
        
    def test_category_validation_005(self):
        localization_files: tuple = tuple(listdir('../budget_graph/localization'))
        languages: tuple = tuple(lang[:2] for lang in localization_files)
        for lang in languages:
            res: bool = category_validation(lang, '')
            self.assertFalse(res, lang)


if __name__ == '__main__':
    unittest.main()
