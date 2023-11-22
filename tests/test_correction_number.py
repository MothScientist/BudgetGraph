import unittest

from validators.correction_number import correction_number


class TestCorrectionNumber(unittest.TestCase):
    def test_correction_number_1(self):
        res = correction_number("100aaa0")
        self.assertEqual(res, 0)

    def test_correction_number_2(self):
        res = correction_number("0")
        self.assertEqual(res, 0)

    def test_correction_number_3(self):
        res = correction_number("1o")
        self.assertEqual(res, 0)


if __name__ == '__main__':
    unittest.main()
