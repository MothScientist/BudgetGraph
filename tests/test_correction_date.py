import unittest
import asyncio

from budget_control.main.validators.correction_date import correction_date, date_in_correct_format, correction_year, correction_month, correction_day


class TestCorrectionNumber(unittest.TestCase):
    def test_correction_date_1(self):
        res = asyncio.run(correction_date("2020-10-20"))
        self.assertEqual(res, "20/10/2020")


class TestDateInCorrectFormat(unittest.TestCase):
    def test_date_in_correct_format_1(self):
        res = asyncio.run(date_in_correct_format("2020-10-10"))
        self.assertEqual(res, True)

    def test_date_in_correct_format_2(self):
        res = asyncio.run(date_in_correct_format("3020-10-20"))
        self.assertEqual(res, False)

    def test_date_in_correct_format_3(self):
        res = asyncio.run(date_in_correct_format("1999-10-20"))
        self.assertEqual(res, False)

    def test_date_in_correct_format_4(self):
        res = asyncio.run(date_in_correct_format("2032-10-20"))
        self.assertEqual(res, False)

    def test_date_in_correct_format_5(self):
        res = asyncio.run(date_in_correct_format("2010-10-20"))
        self.assertEqual(res, True)

    def test_date_in_correct_format_6(self):
        res = asyncio.run(date_in_correct_format("2011-10-20"))
        self.assertEqual(res, True)

    def test_date_in_correct_format_7(self):
        res = asyncio.run(date_in_correct_format("1899-10-20"))
        self.assertEqual(res, False)


class TestCorrectionYear(unittest.TestCase):
    pass


class TestCorrectionMonth(unittest.TestCase):
    pass


class TestCorrectionDay(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
