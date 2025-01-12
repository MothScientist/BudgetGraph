"""
Checking some unit tests with a modified .toml config when deploying an application
"""

import unittest
from json import load as json_load
from budget_graph.dictionary import receive_translation
from budget_graph.global_config import GlobalConfig

GlobalConfig.set_config()


class TestConfigLanguages(unittest.TestCase):
    """
    Testing application localization modules when the parameter in the .toml file localization_enable = false
    """
    languages: tuple = ('ru', 'es', 'de', 'en', 'is', 'fr', 'pt', 'kk')

    with open(f'../budget_graph/localization/en.json', encoding='utf-8') as language_json_file:
        keys_data = json_load(language_json_file)
    all_keys_for_each_language: tuple = tuple(keys_data.keys())

    def test_languages_001(self):
        self.assertFalse(GlobalConfig.localization_enable)

    def test_languages_002(self):
        unknown_key: str = 'unknown_key_unknown_key'
        res: str = receive_translation('en', unknown_key)
        self.assertEqual(res, 'Error')

    def test_languages_003(self):
        unknown_lang: str = 'vw'
        res: str = receive_translation(unknown_lang, 'data_is_safe')
        self.assertEqual(res, 'Error')

    def test_languages_004(self):
        for key in TestConfigLanguages.all_keys_for_each_language:
            answer: str = receive_translation('en', key)
            for lang in TestConfigLanguages.languages:
                res: str = receive_translation(lang, key)
                self.assertEqual(res, answer, f'lang: {lang}; key: {key}')


if __name__ == '__main__':
    unittest.main()
