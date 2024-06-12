import unittest
from datetime import datetime
from random import randint

from budget_graph.db_manager import DatabaseQueries
from budget_graph.encryption import getting_hash, get_salt, get_token
from budget_graph.dictionary import get_list_languages

from tests.build_test_infrastructure import connect_test_db, close_test_db


class DbSmokeTestData:
    def __init__(self):
        self.__languages: tuple = get_list_languages()
        self.__lang_len: int = len(self.__languages)
        self.__users_data: dict = {
                                      1:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 1,  # owner
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      2:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 10)]),
                                           'group_id': 2,  # owner
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      3:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 100)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      4:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 50)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      5:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(5, 25)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           }
                                  }
        self.__groups_tokens: tuple = tuple(get_token() for _ in range(3))

    def get_user_data(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data[attribute_1][attribute_2]

    def get_number_of_users(self) -> int:
        return len(self.__users_data)

    def get_group_token(self, group_id: int) -> str:
        return self.__groups_tokens[group_id - 1]


class SmokeTestDbQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    # First, we enter the minimum data using the methods of our main class for working with the database
    _data = DbSmokeTestData()
    _number_of_users: int = _data.get_number_of_users()

    def test_001_add_users_to_db_1(self):
        for i in range(1, SmokeTestDbQueries._number_of_users + 1):
            group_id: int | None = None if i in (1,2) else SmokeTestDbQueries._data.get_user_data(i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                              SmokeTestDbQueries._data.get_user_data(i, 'telegram_id'),
                              SmokeTestDbQueries._data.get_user_data(i, 'username'),
                              SmokeTestDbQueries._data.get_user_data(i, 'psw_salt'),
                              SmokeTestDbQueries._data.get_user_data(i, 'psw_hash'),
                              group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f"Failed at iteration: {i}")
            else:
                self.assertEqual(res, True, f"Failed at iteration: {i}")

    # Adding user language to the database
    def test_002_add_users_languages(self):
        for i in range(1, SmokeTestDbQueries._number_of_users + 1):
            res = self.test_db.add_user_language(SmokeTestDbQueries._data.get_user_data(i, 'telegram_id'),
                                                 SmokeTestDbQueries._data.get_user_data(i, 'language'))
            self.assertEqual(res, True, f"Failed at iteration: {i}")

    # Filling the transaction table
    def test_003_add_transaction_to_db(self):
        current_year: int = int(datetime.now().strftime("%Y"))
        res: list = []
        number_of_transactions: int = 10  # TODO -> 5_000
        for i in range(number_of_transactions):
            random_integer: int = randint(1, 25_000)
            transaction_amount: int = random_integer*(-1) if randint(1, 2) == 1 else random_integer
            if i % 2 == 0:
                res.append(self.test_db.add_transaction_to_db(
                    SmokeTestDbQueries._data.get_user_data(1, 'username'),
                    transaction_amount,
                    f'{randint(10, 28)}/{randint(4, 12)}/{randint(current_year - 6,
                                                                  current_year - 1)}',
                    'Other',
                    ''))
            else:
                res.append(self.test_db.add_transaction_to_db(
                    SmokeTestDbQueries._data.get_user_data(2, 'username'),
                    transaction_amount,
                    f'{randint(1, 20)}/{randint(1, 8)}/{randint(current_year - 9,
                                                                current_year - 4)}',
                    '',
                    'OK'))
        self.assertEqual(len(res), number_of_transactions, f'Number of transactions: {res}')
        self.assertEqual(all(res), True, f'Number of transactions with errors: {res.count(False)}')


class DatabaseTestData:
    def __init__(self):
        self.__languages: tuple = get_list_languages()
        self.__lang_len: int = len(self.__languages)
        self.__users_data_1: dict = {
                                      1:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,  # owner
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      2:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      3:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      4:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      5:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      6:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(1, 100)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      7:  {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      8: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                          'username': get_token()[:2] + str(randint(1, 9)),
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()),
                                          'group_id': 3,
                                          'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                          },
                                      9: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                          'username': get_token()[:7],
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                          'group_id': 3,
                                          'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                          },
                                      10: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:7],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      11: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(5000, 50000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      12: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      13: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      14: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        },
                                      15: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        },
                                      16: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:10] + str(randint(1, 100)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      17: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      18: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:2] + str(randint(1, 9)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      19: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                           'username': get_token()[:7],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      20: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                            'username': get_token()[:7],
                                            'psw_salt': get_salt(),
                                            'psw_hash': getting_hash(get_salt(), get_salt()),
                                            'group_id': 3,
                                            'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           },
                                      # this user should be rejected for inclusion in the group
                                      21: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                            'username': str(randint(3000, 300000)),
                                            'psw_salt': get_salt(),
                                            'psw_hash': getting_hash(get_salt(), get_salt()),
                                            'group_id': 3,
                                            'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                           }
                                     }

        self.__users_data_2: dict = {
                                    1: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,  # owner
                                        'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        },
                                    2: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                        'username': get_token()[:3],
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        },
                                    3: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        },
                                    4: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        },
                                    5: {'language': self.__languages[randint(0, self.__lang_len - 1)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(1, 100000000000) * randint(1, 9)
                                        }
                                }

    def get_user_data_1(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data_1[attribute_1][attribute_2]

    def get_number_of_users_1(self) -> int:
        return len(self.__users_data_1)

    def get_user_data_2(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data_2[attribute_1][attribute_2]

    def get_number_of_users_2(self) -> int:
        return len(self.__users_data_2)


class TestDbQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    # First, we enter the minimum data using the methods of our main class for working with the database
    _data = DatabaseTestData()
    _number_of_users_1: int = _data.get_number_of_users_1() - 1  # excluding the 21st user
    _number_of_users_2: int = _data.get_number_of_users_2()
    group_3_token: str = ''
    group_4_token: str = ''

    def test_004_add_users_to_db_1(self):
        for i in range(1, TestDbQueries._number_of_users_1 + 1):
            group_id: int | None = None if i == 1 else TestDbQueries._data.get_user_data_1(i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                TestDbQueries._data.get_user_data_1(i, 'telegram_id'),
                TestDbQueries._data.get_user_data_1(i, 'username'),
                TestDbQueries._data.get_user_data_1(i, 'psw_salt'),
                TestDbQueries._data.get_user_data_1(i, 'psw_hash'),
                group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f"Failed at iteration: {i}")
                TestDbQueries.group_3_token = res
            else:
                self.assertEqual(res, True, f"Failed at iteration: {i}")

    def test_004_add_users_to_db_2(self):
        for i in range(1, TestDbQueries._number_of_users_2 + 1):
            group_id: int | None = None if i == 1 else TestDbQueries._data.get_user_data_2(i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                TestDbQueries._data.get_user_data_2(i, 'telegram_id'),
                TestDbQueries._data.get_user_data_2(i, 'username'),
                TestDbQueries._data.get_user_data_2(i, 'psw_salt'),
                TestDbQueries._data.get_user_data_2(i, 'psw_hash'),
                group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f"Failed at iteration: {i}")
                TestDbQueries.group_4_token = res
            else:
                self.assertEqual(res, True, f"Failed at iteration: {i}")

    def test_005_add_users_languages_1(self):
        for i in range(1, TestDbQueries._number_of_users_1 + 1):
            res = self.test_db.add_user_language(TestDbQueries._data.get_user_data_1(i, 'telegram_id'),
                                                 TestDbQueries._data.get_user_data_1(i, 'language'))
            self.assertEqual(res, True, f"Failed at iteration: {i}")

    def test_005_add_users_languages_2(self):
        for i in range(1, TestDbQueries._number_of_users_2 + 1):
            res = self.test_db.add_user_language(TestDbQueries._data.get_user_data_2(i, 'telegram_id'),
                                                 TestDbQueries._data.get_user_data_2(i, 'language'))
            self.assertEqual(res, True, f"Failed at iteration: {i}")

    def test_006_add_extra_user_to_db(self):
        """
        add the 21st user - expect an error
        """
        number_of_extra_user: int = TestDbQueries._number_of_users_1 + 1  # 21
        group_id: int = TestDbQueries._data.get_user_data_1(number_of_extra_user, 'group_id')
        res: bool | str = self.test_db.registration_new_user(
            TestDbQueries._data.get_user_data_1(number_of_extra_user, 'telegram_id'),
            TestDbQueries._data.get_user_data_1(number_of_extra_user, 'username'),
            TestDbQueries._data.get_user_data_1(number_of_extra_user, 'psw_salt'),
            TestDbQueries._data.get_user_data_1(number_of_extra_user, 'psw_hash'),
            group_id=group_id)
        self.assertEqual(res, False)

#   # TODO -> check_limit_users_in_group

    # TODO -> select_data_for_household_table

    # TODO -> get_group_users_data

    def test_007_get_username_by_telegram_id(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_2)
        res: str = (
            self.test_db.get_username_by_telegram_id(TestDbQueries._data.get_user_data_2(number_of_user,
                                                                                         'telegram_id')))
        self.assertEqual(res, TestDbQueries._data.get_user_data_2(number_of_user, 'username'))

    def test_008_get_telegram_id_by_username(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_2)
        res: int = (
            self.test_db.get_telegram_id_by_username(TestDbQueries._data.get_user_data_2(number_of_user,
                                                                                         'username')))
        self.assertEqual(res, TestDbQueries._data.get_user_data_2(number_of_user, 'telegram_id'))

    def test_009_get_group_id_by_token_1(self):
        res: int = self.test_db.get_group_id_by_token(TestDbQueries.group_3_token)
        self.assertEqual(res, TestDbQueries._data.get_user_data_1(1, 'group_id'))

    def test_009_get_group_id_by_token_2(self):
        res: int = self.test_db.get_group_id_by_token(TestDbQueries.group_4_token)
        self.assertEqual(res, TestDbQueries._data.get_user_data_2(1, 'group_id'))

    def test_010_get_group_id_by_telegram_id_1(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_1)
        res: int = self.test_db.get_group_id_by_telegram_id(TestDbQueries._data.get_user_data_1(number_of_user,
                                                                                                'telegram_id'))
        self.assertEqual(res, TestDbQueries._data.get_user_data_1(number_of_user, 'group_id'),
                         f'number_of_user = {number_of_user}')

    def test_010_get_group_id_by_telegram_id_2(self):
        number_of_user: int = 21
        res: int = self.test_db.get_group_id_by_telegram_id(TestDbQueries._data.get_user_data_1(number_of_user,
                                                                                                'telegram_id'))
        self.assertEqual(res, 0)

    def test_011_get_group_id_token_by_username(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_1)
        res: tuple = self.test_db.get_group_id_token_by_username(TestDbQueries._data.get_user_data_1(number_of_user,
                                                                                                     'username'))
        self.assertEqual(res,
                         (TestDbQueries.group_3_token, TestDbQueries._data.get_user_data_1(number_of_user, 'group_id')),
                         f'type(res) = {type(res)}')

    def test_012_get_token_by_telegram_id_1(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_1)
        res: str = self.test_db.get_token_by_telegram_id(TestDbQueries._data.get_user_data_1(number_of_user,
                                                                                             'telegram_id'))
        self.assertEqual(res, TestDbQueries.group_3_token)

    def test_012_get_token_by_telegram_id_2(self):
        number_of_user: int = 21
        res: str = self.test_db.get_token_by_telegram_id(TestDbQueries._data.get_user_data_1(number_of_user,
                                                                                             'telegram_id'))
        self.assertEqual(res, '')

    def test_013_get_salt_by_username_1(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_1)
        res: str = self.test_db.get_salt_by_username(TestDbQueries._data.get_user_data_1(number_of_user, 'username'))
        self.assertEqual(res, TestDbQueries._data.get_user_data_1(number_of_user, 'psw_salt'))

    def test_013_get_salt_by_username_2(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_2)
        res: str = self.test_db.get_salt_by_username(TestDbQueries._data.get_user_data_2(number_of_user, 'username'))
        self.assertEqual(res, TestDbQueries._data.get_user_data_2(number_of_user, 'psw_salt'))

    def test_014_auth_by_username_1(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_1)
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data_1(number_of_user, 'username'),
                                                  TestDbQueries._data.get_user_data_1(number_of_user, 'psw_hash'))
        self.assertEqual(res, True)

    def test_014_auth_by_username_2(self):
        number_of_user: int = randint(1, TestDbQueries._number_of_users_2)
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data_2(number_of_user, 'username'),
                                                  TestDbQueries._data.get_user_data_2(number_of_user, 'psw_hash'))
        self.assertEqual(res, True)

    def test_014_auth_by_username_3(self):
        number_of_user: int = 21
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data_1(number_of_user, 'username'),
                                                  TestDbQueries._data.get_user_data_1(number_of_user, 'psw_hash'))
        self.assertEqual(res, False)

    def test_014_auth_by_username_4(self):
        """
        We will use the data of different users for authorization
        """
        number_of_user: int = 1
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data_1(number_of_user, 'username'),
                                                  TestDbQueries._data.get_user_data_2(number_of_user, 'psw_hash'))
        self.assertEqual(res, False)

    def test_015_get_group_usernames_1(self):
        group_id: int = 3
        res: tuple = self.test_db.get_group_usernames(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data_1(i, 'username')
                                    for i in range(1, TestDbQueries._number_of_users_1 + 1)))

    def test_015_get_group_usernames_2(self):
        group_id: int = 4
        res: tuple = self.test_db.get_group_usernames(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data_2(i, 'username')
                                    for i in range(1, TestDbQueries._number_of_users_2 + 1)))

    def test_015_get_group_usernames_3(self):
        group_id: int = 5  # non-existent group
        res: tuple = self.test_db.get_group_usernames(group_id)
        self.assertEqual(res, tuple())

    def test_016_get_group_telegram_ids_1(self):
        group_id: int = 3
        res: tuple = self.test_db.get_group_telegram_ids(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data_1(i, 'telegram_id')
                                    for i in range(1, TestDbQueries._number_of_users_1 + 1)))

    def test_016_get_group_telegram_ids_2(self):
        group_id: int = 4
        res: tuple = self.test_db.get_group_telegram_ids(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data_2(i, 'telegram_id')
                                    for i in range(1, TestDbQueries._number_of_users_2 + 1)))

    def test_016_get_group_telegram_ids_3(self):
        group_id: int = 5  # non-existent group
        res: tuple = self.test_db.get_group_telegram_ids(group_id)
        self.assertEqual(res, tuple())

    def test_017_get_group_owner_telegram_id_by_group_id_1(self):
        group_id: int = 3
        res: int = self.test_db.get_group_owner_telegram_id_by_group_id(group_id)
        self.assertEqual(res, TestDbQueries._data.get_user_data_1(1, 'telegram_id'))

    def test_017_get_group_owner_telegram_id_by_group_id_2(self):
        group_id: int = 4
        res: int = self.test_db.get_group_owner_telegram_id_by_group_id(group_id)
        self.assertEqual(res, TestDbQueries._data.get_user_data_2(1, 'telegram_id'))

    def test_017_get_group_owner_telegram_id_by_group_id_3(self):
        group_id: int = 5  # non-existent group
        res: int = self.test_db.get_group_owner_telegram_id_by_group_id(group_id)
        self.assertEqual(res, 0)

    def test_018_check_user_is_group_owner_by_telegram_id_1(self):
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data_1(1, 'telegram_id'), TestDbQueries._data.get_user_data_1(1, 'group_id'))
        self.assertEqual(res, True)

    def test_018_check_user_is_group_owner_by_telegram_id_2(self):
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data_2(1, 'telegram_id'), TestDbQueries._data.get_user_data_2(1, 'group_id'))
        self.assertEqual(res, True)

    def test_018_check_user_is_group_owner_by_telegram_id_3(self):
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data_1(2, 'telegram_id'), TestDbQueries._data.get_user_data_1(2, 'group_id'))
        self.assertEqual(res, False)

    def test_018_check_user_is_group_owner_by_telegram_id_4(self):
        # data from different users
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data_1(1, 'telegram_id'), TestDbQueries._data.get_user_data_2(1, 'group_id'))
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()
