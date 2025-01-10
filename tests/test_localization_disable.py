"""
Checking some unit tests with a modified .toml config when deploying an application
"""

import unittest
from budget_graph.dictionary import receive_translation
from budget_graph.global_config import GlobalConfig

GlobalConfig.set_config()


class TestConfigLanguages(unittest.TestCase):
    """
    Testing application localization modules when the parameter in the .toml file localization_enable = false
    """
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
        res: str = receive_translation('is', 'check_correct_username')
        self.assertEqual(res, 'Check the correct spelling of the username.')

    def test_languages_005(self):
        res: str = receive_translation('en', 'start_after_change_language')
        self.assertEqual(res, 'To change the language correctly, '
                              'please restart the bot by clicking on the /start button.')

    def test_languages_006(self):
        res: str = receive_translation('es', 'data_is_safe')
        self.assertEqual(res, 'Your data will not be harmed!')
        
    def test_languages_007(self):
        res: str = receive_translation('de', 'change_owner')
        self.assertNotEqual(res, 'Besitzer wechseln')

    def test_languages_008(self):
        res: str = receive_translation('kk', 'add_income')
        self.assertNotEqual(res, 'Error')

    def test_languages_009(self):
        res: str = receive_translation('pt', 'view_table')
        self.assertNotEqual(res, 'Ver tabela')


if __name__ == '__main__':
    unittest.main()
