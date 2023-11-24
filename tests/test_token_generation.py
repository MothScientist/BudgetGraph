import unittest

from source.token_generation import get_token


class TestTokenGeneration(unittest.TestCase):
    def test_get_token_1(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_2(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_3(self):
        res = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_4(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_5(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_6(self):
        res = type(get_token())
        self.assertEqual(res, str)

    def test_get_token_7(self):
        res = len(get_token(key_length_bytes=30))
        self.assertEqual(res, 60)

    def test_get_token_8(self):
        res = len(get_token(key_length_bytes=50))
        self.assertEqual(res, 100)

    def test_get_token_9(self):
        res = len(get_token(key_length_bytes=120))
        self.assertEqual(res, 240)

    def test_get_token_10(self):
        res = len(get_token(key_length_bytes=8))
        self.assertEqual(res, 16)


if __name__ == '__main__':
    unittest.main()
