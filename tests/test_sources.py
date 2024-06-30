import unittest

from budget_graph.encryption import getting_hash, get_salt, get_token, logging_hash


class TestSaltGeneration(unittest.TestCase):
    def test_get_salt_1(self):
        res: int = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_2(self):
        res: int = len(get_salt(key_length=64))
        self.assertEqual(res, 64)

    def test_get_salt_3(self):
        res: int = len(get_salt(key_length=16))
        self.assertEqual(res, 16)

    def test_get_salt_4(self):
        res: bool = isinstance(get_salt(), str)
        self.assertTrue(res)


class TestPasswordHashing(unittest.TestCase):
    def test_getting_hash_1(self):
        res: str = getting_hash("test", "test")
        self.assertEqual(res, "cef5c5a0f141fa3161a580ab2f7a64f895a60c335861f9fdcef51cf84f5c9527")

    def test_getting_hash_2(self):
        res: str = getting_hash("1234567890", "qwerty")
        self.assertEqual(res, "04bee6f8d78036f0d12a2c3738ae8d28f92e86dac1c750ea89b9f719ea48ad03")

    def test_getting_hash_3(self):
        res: str = getting_hash("", "")
        self.assertEqual(res, "d38c83c56f0d40fbfab593058b4227de0ab71f0907f87f0d99c108c05e9c1065")


class TestTokenGeneration(unittest.TestCase):
    def test_get_token_1(self):
        res: int = len(get_token())
        self.assertEqual(res, 32)

    def test_get_token_2(self):
        res: bool = isinstance(get_token(), str)
        self.assertTrue(res)

    def test_get_token_3(self):
        res: int = len(get_token(key_length_bytes=30))
        self.assertEqual(res, 60)

    def test_get_token_4(self):
        res: int = len(get_token(key_length_bytes=8))
        self.assertEqual(res, 16)


class TestLogHashing(unittest.TestCase):
    def test_getting_log_hash_1(self):
        # to avoid manually updating secrets (.env)
        test_user_telegram_id: int = 123456789

        res: str = logging_hash(test_user_telegram_id)
        self.assertEqual(res, '3f44ce4724b496')

        res_len: int = len(res)
        self.assertEqual(res_len, 14)

        res_type: bool = isinstance(res, str)
        self.assertTrue(res_type)

        self.assertNotEqual(res, str(test_user_telegram_id))

    def test_getting_log_hash_2(self):
        test_user_email: str = 'email@index.com'

        res: str = logging_hash(test_user_email)
        self.assertEqual(res, '1d74ed9b54bdfb')

        res_len: int = len(res)
        self.assertEqual(res_len, 14)

        res_type: bool = isinstance(res, str)
        self.assertTrue(res_type)

        self.assertNotEqual(res, test_user_email)

    def test_getting_log_hash_3(self):
        invalid_value: str = ''
        res: str = logging_hash(invalid_value)
        self.assertEqual(res, '')


if __name__ == '__main__':
    unittest.main()
