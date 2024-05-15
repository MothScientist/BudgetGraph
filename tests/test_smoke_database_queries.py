# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import unittest
from random import randint

from budget_graph.db_manager import DatabaseQueries
from budget_graph.encryption import getting_hash, get_salt, get_token
from budget_graph.dictionary import get_list_languages

from tests.manage_smoke_test_db import connect_test_db, close_test_db


class SmokeTestData:
    def __init__(self):
        self.__languages: tuple = get_list_languages()
        self.__lang_len: int = len(self.__languages)
        self.__users_data: dict = {
                                      1:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 1,  # owner
                                           'telegram_id': randint(1,1000)
                                           },
                                      2:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 2,  # owner
                                           'telegram_id': randint(1001,10000)
                                           },
                                      3:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token() + get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(10001,100000)
                                           },
                                      4:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(100001,10000000)
                                           },
                                      5:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(10000001,10000000000)
                                           }
                                  }

    def get_user_data(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data[attribute_1][attribute_2]


class SmokeTestForDatabaseQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    # First, we enter the minimum data using the methods of our main class for working with the database
    _data = SmokeTestData()

    # Groups
    def test_1_create_new_group_1(self):
        res = self.test_db.create_new_group(SmokeTestForDatabaseQueries._data.get_user_data(1, 'telegram_id'))
        self.assertEqual(len(res), 32)

    def test_2_create_new_group_2(self):
        res = self.test_db.create_new_group(SmokeTestForDatabaseQueries._data.get_user_data(2, 'telegram_id'))
        self.assertEqual(len(res), 32)

    # Users
    def test_3_add_user_to_db_1(self):
        res = self.test_db.add_user_to_db(SmokeTestForDatabaseQueries._data.get_user_data(1, 'username'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(1, 'psw_salt'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(1, 'psw_hash'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(1, 'group_id'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(1, 'telegram_id'))
        self.assertEqual(res, True)

    def test_4_add_user_to_db_2(self):
        res = self.test_db.add_user_to_db(SmokeTestForDatabaseQueries._data.get_user_data(2, 'username'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(2, 'psw_salt'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(2, 'psw_hash'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(2, 'group_id'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(2, 'telegram_id'))
        self.assertEqual(res, True)

    def test_5_add_user_to_db_3(self):
        res = self.test_db.add_user_to_db(SmokeTestForDatabaseQueries._data.get_user_data(3, 'username'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(3, 'psw_salt'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(3, 'psw_hash'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(3, 'group_id'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(3, 'telegram_id'))
        self.assertEqual(res, True)

    def test_6_add_user_to_db_4(self):
        res = self.test_db.add_user_to_db(SmokeTestForDatabaseQueries._data.get_user_data(4, 'username'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(4, 'psw_salt'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(4, 'psw_hash'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(4, 'group_id'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(4, 'telegram_id'))
        self.assertEqual(res, True)

    def test_7_add_user_to_db_5(self):
        res = self.test_db.add_user_to_db(SmokeTestForDatabaseQueries._data.get_user_data(5, 'username'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(5, 'psw_salt'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(5, 'psw_hash'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(5, 'group_id'),
                                          SmokeTestForDatabaseQueries._data.get_user_data(5, 'telegram_id'))
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()
