import unittest
from main.validators.registration import registration_validator


class RegistrationFormTest(unittest.TestCase):

    def test_0(self):
        self.assertFalse(registration_validator("", "", ""))


if __name__ == '__main__':
    unittest.main()
