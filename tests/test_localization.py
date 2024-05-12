# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import unittest
from os import listdir
import json
from time import time
from budget_graph.dictionary import receive_translation


class TestLanguages(unittest.TestCase):
    def setUp(self):
        self.localization_files: tuple = tuple(listdir('../budget_graph/localization'))
        self.languages: tuple = tuple(lang[:2] for lang in self.localization_files)

        self.all_keys_for_each_language: list = []
        for lang in self.languages:
            with open(f"../budget_graph/localization/{lang}.json", encoding='utf-8') as language_json_file:
                keys_data = json.load(language_json_file)
            keys_list: list = keys_data.keys()
            self.all_keys_for_each_language.append(keys_list)

    # def test_languages_1(self):  # Checking multiple keys for presence in each language dictionary
    #     _keys = ("link_github", "get_my_token", "delete_group", "services", "enter_username", "create_new_user_error",
    #              "username", "current_owner_exception", "unknown_message", "unknown_user_in_group", "delete_table",
    #              "category", "set_date", "YES", "get_csv", "language_changed", "misunderstanding", "my")
    #     all_keys_for_all_languages: list[list, ...] = []
    #     res = all(_key in receive_translation(lang, _key) for _key in _keys for lang in self.languages)
    #     self.assertEqual(res, True)
    #
    def test_languages_2(self):  # Checking for equality of number of keys in each language
        dict_len: int = len(self.all_keys_for_each_language[0])
        number_of_languages: int = len(self.languages)
        res = all(dict_len == len(self.all_keys_for_each_language[i]) for i in range(1, number_of_languages))
        self.assertEqual(res, True)

    def test_languages_3(self):  # Checking the loading time of dictionaries
        test_list: list = []  # here we will add information about the dictionary for load simulation
        start = time()
        for lang in self.languages:
            with open(f"../budget_graph/localization/{lang}.json", encoding='utf-8') as f:
                keys_data = json.load(f)
            test_list += keys_data
        finish = time()
        res: bool = True if finish - start < 0.005 else False
        self.assertEqual(res, True)

    # def test_languages_4(self):  # Checking for empty keys
    #     res = all(_key.replace(" ", "") != "" for _key in Dictionary._languages.keys())
    #     self.assertEqual(res, True)
    #
    # def test_languages_5(self):  # Checking for empty keys
    #     # algorithm collects all the keys within the language keys ("en", "es", etc.) into a single tuple
    #     _keys = sum((tuple(Dictionary._languages[i].keys()) for i in Dictionary._languages), ())
    #
    #     # exclude all spaces from the values of this tuple and check that they are not equal to the empty string
    #     res = all(_key.replace(" ", "") != "" for _key in _keys)
    #
    #     self.assertEqual(res, True)

    # def test_languages_6(self):  # Checking for empty values
    #     _values = tuple(val for lang_dict in Dictionary._languages.values() for val in lang_dict.values())
    #     res = all(_value.replace(" ", "") != "" for _value in _values)
    #     self.assertEqual(res, True)
    #
    # def test_languages_7(self):  # Checking keys in a dictionary
    #     _keys_test = {"en", "ru", "es", "de", "fr", "is"}
    #     _keys = set(Dictionary._languages.keys())
    #     res = _keys_test == _keys
    #     self.assertEqual(res, True)
    #
    def test_languages_8(self):  # Checking to see if expected values are returned
        res = receive_translation("es", "invalid_value")
        self.assertEqual(res, "Valor no válido")

    def test_languages_9(self):
        res = receive_translation("en", "none_token")
        self.assertEqual(res, "(if you don't have one, enter \"None\")")

    def test_languages_10(self):
        res = receive_translation("fr", "current_owner_exception")
        self.assertEqual(res, "C'est l'actuel propriétaire du groupe.")

    def test_languages_11(self):
        res = receive_translation("ru", "no_description")
        self.assertEqual(res, "без описания")

    def test_languages_12(self):
        res = receive_translation("de", "change_owner")
        self.assertEqual(res, "Besitzer wechseln")

    def test_languages_13(self):
        res = receive_translation("is", "check_correct_username")
        self.assertEqual(res, "Athugaðu rétta stafsetningu notandanafns.")

    def test_languages_14(self):
        res = receive_translation("en", "start_after_change_language")
        self.assertEqual(res, "To change the language correctly, "
                              "please restart the bot by clicking on the /start button.")

    def test_languages_15(self):
        res = receive_translation("es", "data_is_safe")
        self.assertEqual(res, "¡Tus datos no se verán perjudicados!")


if __name__ == '__main__':
    unittest.main()
