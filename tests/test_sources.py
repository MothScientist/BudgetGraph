# pylint: disable=missing-docstring

import unittest

from app.encryption import getting_hash, get_salt, get_token


class TestPasswordHashing(unittest.TestCase):
    def test_get_salt_1(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_2(self):
        res = len(get_salt(key_length=64))
        self.assertEqual(res, 64)

    def test_get_salt_3(self):
        res = len(get_salt(key_length=16))
        self.assertEqual(res, 16)

    def test_get_salt_4(self):
        res = type(get_salt())
        self.assertEqual(res, str)

    def test_getting_hash_1(self):
        res = getting_hash("test", "test")
        self.assertEqual(res, "cef5c5a0f141fa3161a580ab2f7a64f895a60c335861f9fdcef51cf84f5c9527")

    def test_getting_hash_2(self):
        res = getting_hash("1234567890", "qwerty")
        self.assertEqual(res, "04bee6f8d78036f0d12a2c3738ae8d28f92e86dac1c750ea89b9f719ea48ad03")

    def test_getting_hash_3(self):
        res = getting_hash("", "")
        self.assertEqual(res, "d38c83c56f0d40fbfab593058b4227de0ab71f0907f87f0d99c108c05e9c1065")


class TestTokenGeneration(unittest.TestCase):
    def test_get_token_1(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_2(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_3(self):
        res = len(get_token(key_length_bytes=30))
        self.assertEqual(res, 60)

    def test_get_token_4(self):
        res = len(get_token(key_length_bytes=8))
        self.assertEqual(res, 16)


if __name__ == '__main__':
    unittest.main()
