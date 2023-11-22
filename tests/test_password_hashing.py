import unittest

from password_hashing import getting_hash, get_salt


class TestPasswordHashing(unittest.TestCase):
    def test_get_salt_1(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_2(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_3(self):
        res = len(get_salt())
        self.assertEqual(res, 32)

    def test_get_salt_4(self):
        res = len(get_salt(key_length=64))
        self.assertEqual(res, 64)

    def test_get_salt_5(self):
        res = len(get_salt(key_length=16))
        self.assertEqual(res, 16)

    def test_get_salt_6(self):
        res = type(get_salt())
        self.assertEqual(res, str)

    def test_get_salt_7(self):
        res = type(get_salt(key_length=16))
        self.assertEqual(res, str)

    def test_get_salt_8(self):
        res = type(get_salt(key_length=64))
        self.assertEqual(res, str)

    def test_getting_hash_1(self):
        res = getting_hash("test", "test")
        self.assertEqual(res, "cef5c5a0f141fa3161a580ab2f7a64f895a60c335861f9fdcef51cf84f5c9527")

    def test_getting_hash_2(self):
        res = getting_hash("unittest", "test")
        self.assertEqual(res, "2ceacf66615a9e8bad6e6675bc55279aea8f09c190186aec3e2491e1bbbd5960")

    def test_getting_hash_3(self):
        res = getting_hash("unknown", "unknown123")
        self.assertEqual(res, "493646dc4e9a4f78af2c1f25c59c86f452e25b035e77dcfbd637318d9d599d7d")

    def test_getting_hash_4(self):
        res = getting_hash("1234567890", "qwerty")
        self.assertEqual(res, "04bee6f8d78036f0d12a2c3738ae8d28f92e86dac1c750ea89b9f719ea48ad03")

    def test_getting_hash_5(self):
        res = getting_hash("qwerty12345", "12345QWERTY")
        self.assertEqual(res, "cb5b60c8a592fb35b3ad8f19f9a722fe8c34dc3d80f23ac1dbe8ec3274c687b9")

    def test_getting_hash_6(self):
        res = getting_hash("", "")
        self.assertEqual(res, "d38c83c56f0d40fbfab593058b4227de0ab71f0907f87f0d99c108c05e9c1065")

    def test_getting_hash_7(self):
        res = type(getting_hash("", ""))
        self.assertEqual(res, str)

    def test_getting_hash_8(self):
        res = type(getting_hash("qwertyqwertyqwerty", "123qwerty123qwerty123qwerty"))
        self.assertEqual(res, str)


if __name__ == '__main__':
    unittest.main()
