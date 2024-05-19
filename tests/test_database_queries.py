# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import unittest
from datetime import datetime
from random import randint

from budget_graph.db_manager import DatabaseQueries
from budget_graph.encryption import getting_hash, get_salt, get_token
from budget_graph.dictionary import get_list_languages

from tests.build_test_infrastructure import connect_test_db, close_test_db


class DatabaseSmokeTestData:
    def __init__(self):
        self.__languages: tuple = get_list_languages()
        self.__lang_len: int = len(self.__languages)
        self.__users_data: dict = {
                                      1:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 1,  # owner
                                           'telegram_id': randint(1, 1000)
                                           },
                                      2:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 10)]),
                                           'group_id': 2,  # owner
                                           'telegram_id': randint(1001, 10000)
                                           },
                                      3:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 100)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(10001, 100000)
                                           },
                                      4:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 50)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(100001, 10000000)
                                           },
                                      5:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(5, 25)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(10000001, 10000000000)
                                           }
                                  }

    def get_user_data(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data[attribute_1][attribute_2]

    def get_dict_len(self) -> int:
        return len(self.__users_data)


class SmokeTestForDatabaseQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    # First, we enter the minimum data using the methods of our main class for working with the database
    _data = DatabaseSmokeTestData()

    # Groups
    def test_1_create_new_group_1(self):
        for i in range(1, 3):
            res = self.test_db.create_new_group(SmokeTestForDatabaseQueries._data.get_user_data(i, 'telegram_id'))
            self.assertEqual(len(res), 32, f"Failed at iteration: {i}")

    # Users
    def test_2_add_users_to_db_1(self):
        for i in range(1, SmokeTestForDatabaseQueries._data.get_dict_len() + 1):
            res = self.test_db.add_user_to_db(SmokeTestForDatabaseQueries._data.get_user_data(i, 'username'),
                                              SmokeTestForDatabaseQueries._data.get_user_data(i, 'psw_salt'),
                                              SmokeTestForDatabaseQueries._data.get_user_data(i, 'psw_hash'),
                                              SmokeTestForDatabaseQueries._data.get_user_data(i, 'group_id'),
                                              SmokeTestForDatabaseQueries._data.get_user_data(i, 'telegram_id'))
            self.assertEqual(res, True)

    # Adding user language to the database
    def test_3_add_users_languages_1(self):
        for i in range(1, SmokeTestForDatabaseQueries._data.get_dict_len() + 1):
            res = self.test_db.add_user_language(SmokeTestForDatabaseQueries._data.get_user_data(i, 'telegram_id'),
                                                 SmokeTestForDatabaseQueries._data.get_user_data(i, 'language'))
            self.assertEqual(res, True, f"Failed at iteration: {i}")

    # Filling the transaction table
    def test_4_add_transaction_to_db_1(self):
        current_year: int = int(datetime.now().strftime("%Y"))
        res: list = []
        for i in range(1_000):
            random_integer: int = randint(1, 25_000)
            transaction_amount: int = random_integer*(-1) if randint(1, 2) == 1 else random_integer
            if i % 2 == 0:
                res.append(self.test_db.add_transaction_to_db(
                    SmokeTestForDatabaseQueries._data.get_user_data(1, 'username'),
                    transaction_amount,
                    f'{randint(10, 28)}/{randint(4, 12)}/{randint(current_year - 6,
                                                                  current_year - 1)}',
                    'Other',
                    ''))
            else:
                res.append(self.test_db.add_transaction_to_db(
                    SmokeTestForDatabaseQueries._data.get_user_data(2, 'username'),
                    transaction_amount,
                    f'{randint(1, 20)}/{randint(1, 8)}/{randint(current_year - 9,
                                                                current_year - 4)}',
                    '',
                    'OK'))
        self.assertEqual(len(res), 1_000, f'Number of transactions: {res}')
        self.assertEqual(all(res), True, f'Number of transactions with errors: {res.count(False)}')


class DatabaseTestData:
    def __init__(self):
        # TODO - языки и список брать наследованием из первого класса
        self.__languages: tuple = get_list_languages()
        self.__lang_len: int = len(self.__languages)
        self.__users_data: dict = {
                                      1:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,  # owner
                                           'telegram_id': randint(1, 1000)
                                           },
                                      2:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1001, 10000)
                                           },
                                      3:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(10001, 100000)
                                           },
                                      4:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100001, 10000000)
                                           },
                                      5:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(10000001, 10000000000)
                                           },
                                      6:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(1, 100)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(10, 1000)
                                           },
                                      7:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 9)
                                           },
                                      8: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                          'username': get_token()[:2] + str(randint(1, 9)),
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()),
                                          'group_id': 3,
                                          'telegram_id': randint(1001, 10000)
                                          },
                                      9: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                          'username': get_token()[:7],
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                          'group_id': 3,
                                          'telegram_id': randint(90000, 9000000)
                                          },
                                      10: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:7],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(600000, 60000000)
                                           },
                                      11: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(5000, 50000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(4000000, 4000000000)
                                           },
                                      12: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(8000, 7000000)
                                           },
                                      13: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(9000, 10000000)
                                           },
                                      14: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(10000, 40000000)
                                        },
                                      15: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(4000000, 80000000000)
                                        },
                                      16: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(1, 100)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(150, 5000)
                                           },
                                      17: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(120, 9000)
                                           },
                                      18: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:2] + str(randint(1, 9)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(4001, 50000)
                                           },
                                      19: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:7],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(70000, 95000)
                                           },
                                      20: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                            'username': get_token()[:7],
                                            'psw_salt': get_salt(),
                                            'psw_hash': getting_hash(get_salt(), get_salt()),
                                            'group_id': 3,
                                            'telegram_id': randint(300000, 80000000)
                                           },
                                      # this user should be rejected for inclusion in the group
                                      21: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                            'username': str(randint(3000, 300000)),
                                            'psw_salt': get_salt(),
                                            'psw_hash': getting_hash(get_salt(), get_salt()),
                                            'group_id': 3,
                                            'telegram_id': randint(4000000, 7000000000)
                                           }
                                     }

    def get_user_data(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data[attribute_1][attribute_2]

    def get_dict_len(self) -> int:
        return len(self.__users_data)


class BaseTestForDatabaseQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    # First, we enter the minimum data using the methods of our main class for working with the database
    _data = DatabaseTestData()

    def test_5_create_new_group_1(self):
        res = self.test_db.create_new_group(BaseTestForDatabaseQueries._data.get_user_data(1, 'telegram_id'))
        self.assertEqual(len(res), 32)

    def test_6_add_users_to_db_1(self):
        for i in range(1, BaseTestForDatabaseQueries._data.get_dict_len()):  # 1 - 20
            res = self.test_db.add_user_to_db(BaseTestForDatabaseQueries._data.get_user_data(i, 'username'),
                                              BaseTestForDatabaseQueries._data.get_user_data(i, 'psw_salt'),
                                              BaseTestForDatabaseQueries._data.get_user_data(i, 'psw_hash'),
                                              BaseTestForDatabaseQueries._data.get_user_data(i, 'group_id'),
                                              BaseTestForDatabaseQueries._data.get_user_data(i, 'telegram_id'))
            self.assertEqual(res, True, f"Failed at iteration: {i}")

    def test_7_add_extra_user_to_db_1(self):
        """
        add the 21st user - expect an error
        """
        res = self.test_db.add_user_to_db(BaseTestForDatabaseQueries._data.get_user_data(21, 'username'),
                                          BaseTestForDatabaseQueries._data.get_user_data(21, 'psw_salt'),
                                          BaseTestForDatabaseQueries._data.get_user_data(21, 'psw_hash'),
                                          BaseTestForDatabaseQueries._data.get_user_data(21, 'group_id'),
                                          BaseTestForDatabaseQueries._data.get_user_data(21, 'telegram_id'))
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()
