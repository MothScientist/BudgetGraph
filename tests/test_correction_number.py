import unittest

from validators.correction_number import correction_number


class TestCorrectionNumber(unittest.TestCase):
    def test_correction_number_1(self):
        res = correction_number("100aaa0")
        self.assertEqual(res, 1000)


if __name__ == '__main__':
    unittest.main()
