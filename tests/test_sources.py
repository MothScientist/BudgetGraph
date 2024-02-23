# pylint: disable=missing-docstring

import unittest

from app.encryption import getting_hash, get_salt, get_token
from app.dictionary import Dictionary
from app.create_csv import create_csv_file, get_file_size_kb, get_file_checksum


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


class TestCreateCSV(unittest.TestCase):
    def test_create_csv_1(self):
        pass

    def test_create_csv_2(self):
        pass

    def test_create_csv_3(self):
        pass
    
    def test_file_size_1(self):
        pass

    def test_file_size_2(self):
        pass

    def test_file_size_3(self):
        pass

    def test_file_checksum_1(self):
        pass

    def test_file_checksum_2(self):
        pass

    def test_file_checksum_3(self):
        pass


class TestLanguages(unittest.TestCase):
    def test_languages_1(self):  # Checking multiple keys for presence in each language dictionary
        _keys = ("link_github", "get_my_token", "delete_group", "services", "enter_username", "create_new_user_error",
                 "username", "current_owner_exception", "unknown_message", "unknown_user_in_group", "delete_table",
                 "category", "set_date", "YES", "get_csv", "language_changed", "misunderstanding", "my")
        res = all(_key in Dictionary._languages[lang] for _key in _keys for lang in Dictionary._languages.keys())
        self.assertEqual(res, True)
    
    def test_languages_2(self):  # Checking for equality of number of keys in each language
        dict_len = len(Dictionary._languages["en"])
        res = all(dict_len == len(Dictionary._languages[lang]) for lang in Dictionary._languages.keys())
        self.assertEqual(res, True)
    
    def test_languages_3(self):  # Checking to see if expected values are returned
        res = Dictionary.receive_translation("es", "invalid_value")
        self.assertEqual(res, "Valor no válido")
    
    def test_languages_4(self):
        res = Dictionary.receive_translation("en", "none_token")
        self.assertEqual(res, "(if you don't have one, enter \"None\")")
    
    def test_languages_5(self):
        res = Dictionary.receive_translation("fr", "current_owner_exception")
        self.assertEqual(res, "C'est l'actuel propriétaire du groupe.")

    def test_languages_6(self):
        res = Dictionary.receive_translation("ru", "no_description")
        self.assertEqual(res, "без описания")

    def test_languages_7(self):
        res = Dictionary.receive_translation("de", "change_owner")
        self.assertEqual(res, "Besitzer wechseln")

    def test_languages_8(self):
        res = Dictionary.receive_translation("is", "check_correct_username")
        self.assertEqual(res, "Athugaðu rétta stafsetningu notandanafns.")

    def test_languages_9(self):  # Checking for empty keys
        res = all(_key.replace(" ", "") != "" for _key in Dictionary._languages.keys())
        self.assertEqual(res, True)

    def test_languages_10(self):  # Checking for empty keys
        # algorithm collects all the keys within the language keys ("en", "es", etc.) into a single tuple
        _keys = sum((tuple(Dictionary._languages[i].keys()) for i in Dictionary._languages), ())

        # exclude all spaces from the values of this tuple and check that they are not equal to the empty string
        res = all(_key.replace(" ", "") != "" for _key in _keys)

        self.assertEqual(res, True)

    def test_languages_11(self):  # Checking for empty values
        _values = tuple(val for lang_dict in Dictionary._languages.values() for val in lang_dict.values())
        res = all(_value.replace(" ", "") != "" for _value in _values)
        self.assertEqual(res, True)

    def test_languages_12(self):  # Checking keys in a dictionary
        _keys_test = {"en", "ru", "es", "de", "fr", "is"}
        _keys = set(Dictionary._languages.keys())
        res = _keys_test == _keys
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()
