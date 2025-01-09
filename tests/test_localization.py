import unittest
import json
from time import time
from budget_graph.dictionary import receive_translation, get_list_languages


class TestLanguages(unittest.TestCase):
    languages: tuple = get_list_languages()

    all_keys_for_each_language_list: list = []
    for lang in languages:
        with open(f'../budget_graph/localization/{lang}.json', encoding='utf-8') as language_json_file:
            keys_data = json.load(language_json_file)
        keys_list: list = list(keys_data.keys())
        all_keys_for_each_language_list.append(keys_list)
    # immutable
    all_keys_for_each_language: tuple = tuple(all_keys_for_each_language_list)

    def test_languages_1(self):
        """
        Checking multiple keys for presence in each language dictionary
        """
        _keys: tuple = (
            'link_github', 'get_my_token', 'delete_group', 'services', 'enter_username', 'create_new_user_error',
            'username', 'current_owner_exception', 'unknown_message', 'unknown_user_in_group', 'delete_table',
            'category', 'set_date', 'YES', 'get_csv', 'language_changed', 'misunderstanding', 'my'
        )
        res: bool = all(receive_translation(lang, _key) for _key in _keys for lang in TestLanguages.languages)
        self.assertTrue(res, f'Missing keys: {[(_key, lang) for _key in _keys for lang in TestLanguages.languages 
                                              if receive_translation(lang, _key) is None]}')

    def test_languages_2(self):
        """
        Checking for equality of number of keys in each language
        """
        dict_len: int = len(TestLanguages.all_keys_for_each_language[0])
        number_of_languages: int = len(TestLanguages.languages)
        res: bool = all(dict_len == len(TestLanguages.all_keys_for_each_language[i])
                        for i in range(number_of_languages))
        self.assertTrue(res)

    def test_languages_3(self):
        """
        Checking the loading time of dictionaries
        """
        test_list: list = []  # here we will add information about the dictionary for load simulation
        start: float = time()
        for lang in self.languages:
            with open(f'../budget_graph/localization/{lang}.json', encoding='utf-8') as f:
                keys_data = json.load(f)
            test_list += keys_data
        finish: float = time()
        res: bool = True if finish - start < 0.05 else False
        self.assertTrue(res, f'Actual time: {finish - start}')

    def test_languages_4(self):
        """
        Checking for empty keys
        """
        # algorithm collects all the keys within the language keys ('en', 'es', etc.) into a single tuple
        _keys = sum((tuple(i) for i in TestLanguages.all_keys_for_each_language), ())
        # exclude all spaces from the values of this tuple and check that they are not equal to the empty string
        res = all(_key.replace(' ', '') != '' for _key in _keys)
        self.assertTrue(res)

    def test_languages_5(self):
        """
        Checking for empty values
        """
        _values = tuple(receive_translation(lang, key) for key in TestLanguages.all_keys_for_each_language[0]
                        for lang in TestLanguages.languages)
        res = all(_value.replace(' ', '') != '' for _value in _values)
        self.assertTrue(res)

    def test_languages_6(self):
        """
        Checking for uniqueness of keys
        """
        for lang_keys in TestLanguages.all_keys_for_each_language:
            res: bool = (len(lang_keys) == len(set(lang_keys)))
            self.assertTrue(res)

    def test_languages_7(self):
        """
        Checking for uniqueness of values
        """
        for lang in TestLanguages.languages:
            for keys in TestLanguages.all_keys_for_each_language:
                _values = tuple(receive_translation(lang, key) for key in keys)
                res: bool = (len(_values) == len(set(_values)))
                self.assertTrue(res, f'Language: {lang}; len(_values) = {len(_values)}; '
                                     f'len(set(_values)) = {len(set(_values))}')

    def test_languages_8(self):
        unknown_key: str = '123123'
        res: str = receive_translation('es', unknown_key)
        self.assertEqual(res, 'Error')

    def test_languages_9(self):
        res: str = receive_translation('es', 'invalid_value')
        self.assertEqual(res, 'Valor no válido')

    def test_languages_10(self):
        res: str = receive_translation('en', 'none_token')
        self.assertEqual(res, "(if you don't have one, enter \'None\')")

    def test_languages_11(self):
        res: str = receive_translation('fr', 'current_owner_exception')
        self.assertEqual(res, "C'est l'actuel propriétaire du groupe.")

    def test_languages_12(self):
        res: str = receive_translation('ru', 'no_description')
        self.assertEqual(res, 'без описания')

    def test_languages_13(self):
        unknown_key: str = 'unknown_key_unknown_key'
        res: str = receive_translation('en', unknown_key)
        self.assertEqual(res, 'Error')

    def test_languages_14(self):
        res: str = receive_translation('de', 'change_owner')
        self.assertEqual(res, 'Besitzer wechseln')

    def test_languages_15(self):
        res: str = receive_translation('is', 'check_correct_username')
        self.assertEqual(res, 'Athugaðu rétta stafsetningu notandanafns.')

    def test_languages_16(self):
        res: str = receive_translation('en', 'start_after_change_language')
        self.assertEqual(res, 'To change the language correctly, '
                              'please restart the bot by clicking on the /start button.')

    def test_languages_17(self):
        res: str = receive_translation('es', 'data_is_safe')
        self.assertEqual(res, '¡Tus datos no se verán perjudicados!')

    def test_languages_18(self):
        unknown_lang: str = 'gb'
        res: str = receive_translation(unknown_lang, 'data_is_safe')
        self.assertEqual(res, 'Error')

    def test_languages_19(self):
        res: str = receive_translation('kk', 'add_description')
        self.assertEqual(res, 'Сипаттама қосу (50 таңбадан артық емес)')

    def test_languages_20(self):
        res: str = receive_translation('kk', 'add_income')
        self.assertEqual(res, 'Табыс қосыңыз')

    def test_languages_21(self):
        res: str = receive_translation('kk', 'group_is_full')
        self.assertEqual(res, 'Бұл белгі бар топ жоқ немесе ол толы. Қосымша ақпарат алу үшін топ мүшелеріне '
                              'хабарласыңыз немесе өз тобыңызды жасаңыз!')

    def test_languages_22(self):
        unknown_phrase: str = 'qwerty'
        res: str = receive_translation('kk', unknown_phrase)
        self.assertEqual(res, 'Error')

    def test_languages_23(self):
        res: str = receive_translation('pt', 'view_table')
        self.assertEqual(res, 'Ver tabela')

    def test_languages_24(self):
        res: str = receive_translation('pt', 'premium')
        self.assertEqual(res, 'Prêmio')

    def test_languages_25(self):
        res: str = receive_translation('pt', 'USERNAME')
        self.assertEqual(res, 'NOME DE UTILIZADOR')

    def test_languages_26(self):
        unknown_phrase: str = 'earth_moon'
        res: str = receive_translation('pt', unknown_phrase)
        self.assertEqual(res, 'Error')

    def test_get_list_languages_1(self):
        res: tuple = get_list_languages()
        # don`t take into account the order of languages in the tuple
        self.assertEqual(list(res).sort(), ['ru', 'es', 'de', 'en', 'is', 'fr', 'pt', 'kk'].sort())

    def test_get_list_languages_2(self):
        languages: tuple = get_list_languages()
        self.assertTrue(all(len(lang) == 2 for lang in languages))


if __name__ == '__main__':
    unittest.main()
