"""
Checking some unit tests with a modified .toml config when deploying an application
"""

import unittest
from budget_graph.dictionary import receive_translation


class TestConfigLanguages(unittest.TestCase):
    """
    Testing application localization modules when the parameter in the .toml file localization_enable = false
    """
    def test_languages_01(self):
        unknown_key: str = 'unknown_key_unknown_key'
        res: str = receive_translation('en', unknown_key)
        self.assertEqual(res, 'Error')

    def test_languages_02(self):
        unknown_lang: str = 'vw'
        res: str = receive_translation(unknown_lang, 'data_is_safe')
        self.assertEqual(res, 'Error')

    def test_languages_03(self):
        res: str = receive_translation('is', 'check_correct_username')
        self.assertEqual(res, 'Check the correct spelling of the username.')

    def test_languages_04(self):
        res: str = receive_translation('en', 'start_after_change_language')
        self.assertEqual(res, 'To change the language correctly, '
                              'please restart the bot by clicking on the /start button.')

    def test_languages_05(self):
        res: str = receive_translation('es', 'data_is_safe')
        self.assertEqual(res, 'Your data will not be harmed!')
        
    def test_languages_06(self):
        res: str = receive_translation('de', 'change_owner')
        self.assertNotEqual(res, 'Besitzer wechseln')

    def test_languages_07(self):
        res: str = receive_translation('kk', 'add_income')
        self.assertNotEqual(res, 'Error')

    def test_languages_08(self):
        res: str = receive_translation('pt', 'view_table')
        self.assertNotEqual(res, 'Ver tabela')


if __name__ == '__main__':
    unittest.main()
