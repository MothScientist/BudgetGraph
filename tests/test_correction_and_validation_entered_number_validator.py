import unittest

from budget_control.main.validators.correction_and_validation_entered_number import correction_and_validation_entered_number


class TestCorrectionAndValidationEnteredNumber(unittest.TestCase):
    def test_correction_and_validation_entered_number_1(self):
        res = correction_and_validation_entered_number("100aaa0")
        self.assertEqual(res, 1000)


if __name__ == '__main__':
    unittest.main()
