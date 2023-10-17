import unittest

from budget_control.main.validators.description import description_validator


class TestDescriptionValidator(unittest.TestCase):
    def test_description_validator_1(self):
        res = description_validator("")
        self.assertEqual(res, 32)


if __name__ == '__main__':
    unittest.main()
