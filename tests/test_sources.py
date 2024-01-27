import sys
sys.path.append("..") # Adds higher directory to python modules path.
# pylint: disable=missing-docstring
import unittest

from app.source.password_hashing import getting_hash, get_salt
from app.source.token_generation import get_token
from app.source.dictionary import Languages


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


class TestCSVGeneration(unittest.TestCase):
    pass


class TestLanguages(unittest.TestCase):
    def test_languages_1(self):  # Checking multiple keys for presence in each language dictionary
        _keys = ["link_github", "get_my_token", "delete_group", "services", "enter_username", "create_new_user_error",
                 "username", "current_owner_exception", "unknown_message", "unknown_user_in_group", "delete_table"]
        res = all(_key in Languages._languages[lang] for _key in _keys for lang in Languages._languages.keys())
        self.assertEqual(res, True)
    
    def test_languages_2(self):  # Checking for equality of number of keys in each language
        dict_len = len(Languages._languages["en"])
        res = all(dict_len == len(Languages._languages[lang]) for lang in Languages._languages.keys())
        self.assertEqual(res, True)
    
    def test_languages_3(self):  # Checking to see if expected values are returned
        res = Languages.receive_translation("es", "invalid_value")
        self.assertEqual(res, "Valor no válido")
    
    def test_languages_4(self):
        res = Languages.receive_translation("en", "none_token")
        self.assertEqual(res, "(if you don't have one, enter \"None\")")
    
    def test_languages_5(self):
        res = Languages.receive_translation("fr", "current_owner_exception")
        self.assertEqual(res, "C'est l'actuel propriétaire du groupe.")

    def test_languages_6(self):
        res = Languages.receive_translation("ru", "no_description")
        self.assertEqual(res, "без описания")

    def test_languages_7(self):
        res = Languages.receive_translation("de", "change_owner")
        self.assertEqual(res, "Besitzer wechseln")

    def test_languages_8(self):
        res = Languages.receive_translation("is", "check_correct_username")
        self.assertEqual(res, "Athugaðu rétta stafsetningu notandanafns.")

    def test_languages_9(self):  # Error exception test (language is not listed)
        # If the language is not in the list, it will return the value in English
        res = Languages.receive_translation("it", "view_table")
        self.assertEqual(res, "View table")

    def test_languages_10(self):  # non-existent key
        res = Languages.receive_translation("de", "table_view")
        self.assertEqual(res, None)

    def test_languages_11(self):  # missing key and value
        res = Languages.receive_translation("", "")
        self.assertEqual(res, None)


if __name__ == '__main__':
    unittest.main()
