import unittest

from budget_control.main.validators.correction_date import correction_date


class TestCorrectionNumber(unittest.TestCase):
    def test_correction_date_1(self):
        res = correction_date("10.10.2020")
        self.assertEqual(res, "10/10/2020")


if __name__ == '__main__':
    unittest.main()
