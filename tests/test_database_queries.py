import unittest
from random import randint, randrange
from functools import cache
from datetime import datetime, timedelta, timezone

from budget_graph.db_manager import DatabaseQueries
from budget_graph.dictionary import get_list_languages
from budget_graph.registration_service import user_registration
from budget_graph.encryption import getting_hash, get_salt, get_token

from tests.build_test_infrastructure import connect_test_db, close_test_db

LANGUAGES: tuple = get_list_languages()
LANG_LEN: int = len(LANGUAGES)

SMOKE_NUMBER_OF_TRANSACTIONS: int = 1_500
NUMBER_OF_TRANSACTION_CYCLE: int = 750
NUMBER_OF_TRANSACTION_CYCLE_FOR_ONE_DAY: int = 250


class DbSmokeTestData:
    """
    Data class, interaction only through methods to avoid data modification
    """
    def __init__(self):
        self.__users_data: dict = {
                                      1:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 1,  # owner
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      2:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 10)]),
                                           'group_id': 2,  # owner
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      3:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 100)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      4:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 50)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      5:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(5, 25)]),
                                           'group_id': randint(1,2),
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           }
                                  }

    @cache
    def get_user_data(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data[attribute_1][attribute_2]

    @cache
    def get_number_of_users(self) -> int:
        return len(self.__users_data)


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
                self.assertTrue(res, f"Failed at iteration: {i}")

    # Adding user language to the database
    def test_002_add_users_languages(self):
        for i in range(1, SmokeTestDbQueries._number_of_users + 1):
            res = self.test_db.add_user_language(SmokeTestDbQueries._data.get_user_data(i, 'telegram_id'),
                                                 SmokeTestDbQueries._data.get_user_data(i, 'language'))
            self.assertTrue(res, f"Failed at iteration: {i}")

    # Filling the transaction table
    def test_003_add_transaction_to_db(self):
        current_year: int = int(datetime.now().strftime("%Y"))
        res: list = []
        number_of_transactions: int = SMOKE_NUMBER_OF_TRANSACTIONS
        for i in range(number_of_transactions):
            random_integer: int = randint(1, 25_000)
            transaction_amount: int = random_integer*(-1) if randint(1, 2) == 1 else random_integer
            if i % 2 == 0:
                res.append(self.test_db.add_transaction_to_db(
                    transaction_amount,
                    f'{randint(current_year - 6, current_year - 1)}-{randint(4, 12)}-{randint(10, 28)}',
                    'Other',
                    '',
                    # use telegram_id to enter data into the table
                    telegram_id=SmokeTestDbQueries._data.get_user_data(1, 'telegram_id')))
            else:
                res.append(self.test_db.add_transaction_to_db(
                    transaction_amount,
                    f'{randint(1, 20)}/{randint(1, 8)}/{randint(current_year - 9, current_year - 4)}',
                    '',
                    'OK',
                    # use username to enter data into the table
                    username=SmokeTestDbQueries._data.get_user_data(2, 'username')))
        self.assertEqual(len(res), number_of_transactions, f'Number of transactions: {res}')
        self.assertTrue(all(res), f'Number of transactions with errors: {res.count(False)}')

    def test_004_check_transactions_1(self):
        req: tuple = self.test_db.select_data_for_household_table(
            SmokeTestDbQueries._data.get_user_data(1, 'group_id'),
            0
        )
        res: int = len(req)
        self.assertEqual(res, SMOKE_NUMBER_OF_TRANSACTIONS // 2, f'number_of_transactions = {res}')

    def test_004_check_transactions_2(self):
        req: tuple = self.test_db.select_data_for_household_table(
            SmokeTestDbQueries._data.get_user_data(2, 'group_id'),
            0
        )
        res: int = len(req)
        self.assertEqual(res, SMOKE_NUMBER_OF_TRANSACTIONS // 2, f'number_of_transactions = {res}')

    def test_005_check_sum_in_transactions_1(self):
        req: tuple = self.test_db.select_data_for_household_table(
            SmokeTestDbQueries._data.get_user_data(1, 'group_id'),
            0  # all records
        )  # get a list of transactions from most recent to oldest -> so then we turn it over
        res: tuple = tuple((i[2], i[3]) for i in req[::-1])  # (transfer, total)

        res_for_first_transaction: bool = (res[0][0] == res[0][1])
        self.assertTrue(res_for_first_transaction, f'res_for_first_transaction = {res_for_first_transaction},'
                                                   f'res[0][0] = {res[0][0]}, res[0][1] = {res[0][1]}')

        for j in range(1, len(res)):
            diff: bool = (res[j][1] - res[j][0] == res[j - 1][1])
            self.assertTrue(diff, f'The amount in the transaction does not match #{j}, '
                                  f'res[j][1] = {res[j][1]}, res[j][0] = {res[j][0]}, '
                                  f'res[j-1][1] = {res[j - 1][1]} => '
                                  f'res[j][1] - res[j][0] = {res[j][1] - res[j][0]}')

    def test_005_check_sum_in_transactions_2(self):
        req: tuple = self.test_db.select_data_for_household_table(
            SmokeTestDbQueries._data.get_user_data(2, 'group_id'),
            0  # all records
        )  # get a list of transactions from most recent to oldest -> so then we turn it over
        res: tuple = tuple((i[2], i[3]) for i in req[::-1])  # (transfer, total)

        res_for_first_transaction: bool = (res[0][0] == res[0][1])
        self.assertTrue(res_for_first_transaction, f'res_for_first_transaction = {res_for_first_transaction},'
                                                   f'res[0][0] = {res[0][0]}, res[0][1] = {res[0][1]}')

        for j in range(1, len(res)):
            diff: bool = (res[j][1] - res[j][0] == res[j - 1][1])
            self.assertTrue(diff, f'The amount in the transaction does not match #{j}, '
                                  f'res[j][1] = {res[j][1]}, res[j][0] = {res[j][0]}, '
                                  f'res[j-1][1] = {res[j - 1][1]} => '
                                  f'res[j][1] - res[j][0] = {res[j][1] - res[j][0]}')


class DatabaseTestData:
    """
    Data class, interaction only through methods to avoid data modification
    """
    def __init__(self):
        self.__users_data_1: dict = {
                                      1:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,  # owner
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      2:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      3:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      4:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      5:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      6:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10] + str(randint(1, 100)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      7:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      8: {'language': LANGUAGES[randrange(LANG_LEN)],
                                          'username': get_token()[:2] + str(randint(1, 9)),
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()),
                                          'group_id': 3,
                                          'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                          },
                                      9: {'language': LANGUAGES[randrange(LANG_LEN)],
                                          'username': get_token()[:7],
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                          'group_id': 3,
                                          'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                          },
                                      10: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:7],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      11: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': str(randint(5000, 50000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      12: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      13: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      14: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      15: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': str(randint(100, 1000000000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      16: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10] + str(randint(1, 100)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      17: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      18: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:2] + str(randint(1, 9)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      19: {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:7],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 3,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      20: {'language': LANGUAGES[randrange(LANG_LEN)],
                                            'username': get_token()[:7],
                                            'psw_salt': get_salt(),
                                            'psw_hash': getting_hash(get_salt(), get_salt()),
                                            'group_id': 3,
                                            'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      # this user should be rejected for inclusion in the group
                                      21: {'language': LANGUAGES[randrange(LANG_LEN)],
                                            'username': str(randint(3000, 300000)),
                                            'psw_salt': get_salt(),
                                            'psw_hash': getting_hash(get_salt(), get_salt()),
                                            'group_id': 3,
                                            'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           }
                                     }

        self.__users_data_2: dict = {
                                    1: {'language': LANGUAGES[randrange(LANG_LEN)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,  # owner
                                        'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                        },
                                    2: {'language': LANGUAGES[randrange(LANG_LEN)],
                                        'username': get_token()[:3],
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                        },
                                    3: {'language': LANGUAGES[randrange(LANG_LEN)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                        },
                                    4: {'language': LANGUAGES[randrange(LANG_LEN)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                        },
                                    5: {'language': LANGUAGES[randrange(LANG_LEN)],
                                        'username': get_token()[:5] + str(randint(10, 1000)),
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 4,
                                        'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                        }
                                }

    @cache
    def get_user_data(self, group_id: int, attribute_1: int, attribute_2: str) -> int | str:
        if group_id == 3:
            return self.__users_data_1[attribute_1][attribute_2]
        return self.__users_data_2[attribute_1][attribute_2]

    @cache
    def get_number_of_users(self, group_id: int) -> int:
        if group_id == 3:
            return len(self.__users_data_1)
        return len(self.__users_data_2)


class TestDbQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    # First, we enter the minimum data using the methods of our main class for working with the database
    _data = DatabaseTestData()
    _number_of_users_group_3: int = _data.get_number_of_users(3) - 1  # excluding the 21st user
    _number_of_users_group_4: int = _data.get_number_of_users(4)

    group_3_token: str = ''
    group_4_token: str = ''

    def test_006_add_users_to_db_1(self):
        for i in range(1, TestDbQueries._number_of_users_group_3 + 1):
            group_id: int | None = None if i == 1 else TestDbQueries._data.get_user_data(3, i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                TestDbQueries._data.get_user_data(3, i, 'telegram_id'),
                TestDbQueries._data.get_user_data(3, i, 'username'),
                TestDbQueries._data.get_user_data(3, i, 'psw_salt'),
                TestDbQueries._data.get_user_data(3, i, 'psw_hash'),
                group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f"Failed at iteration: {i}")
                TestDbQueries.group_3_token = res
            else:
                self.assertEqual(res, True, f"Failed at iteration: {i}")

    def test_006_add_users_to_db_2(self):
        for i in range(1, TestDbQueries._number_of_users_group_4 + 1):
            group_id: int | None = None if i == 1 else TestDbQueries._data.get_user_data(4, i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                TestDbQueries._data.get_user_data(4, i, 'telegram_id'),
                TestDbQueries._data.get_user_data(4, i, 'username'),
                TestDbQueries._data.get_user_data(4, i, 'psw_salt'),
                TestDbQueries._data.get_user_data(4, i, 'psw_hash'),
                group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f"Failed at iteration: {i}")
                TestDbQueries.group_4_token = res
            else:
                self.assertTrue(res, f"Failed at iteration: {i}")

    def test_007_add_users_languages_1(self):
        group_id: int = 3
        for i in range(1, TestDbQueries._number_of_users_group_3 + 1):
            res = self.test_db.add_user_language(TestDbQueries._data.get_user_data(group_id, i, 'telegram_id'),
                                                 TestDbQueries._data.get_user_data(group_id, i, 'language'))
            self.assertTrue(res, f"Failed at iteration: {i}")

    def test_007_add_users_languages_2(self):
        group_id: int = 4
        for i in range(1, TestDbQueries._number_of_users_group_4 + 1):
            res = self.test_db.add_user_language(TestDbQueries._data.get_user_data(group_id, i, 'telegram_id'),
                                                 TestDbQueries._data.get_user_data(group_id, i, 'language'))
            self.assertTrue(res, f"Failed at iteration: {i}")

    def test_008_add_extra_user_to_db(self):
        """
        add the 21st user - expect an error
        """
        number_of_extra_user: int = 21
        group_id: int = 3
        res: bool | str = self.test_db.registration_new_user(
            TestDbQueries._data.get_user_data(group_id, number_of_extra_user, 'telegram_id'),
            TestDbQueries._data.get_user_data(group_id, number_of_extra_user, 'username'),
            TestDbQueries._data.get_user_data(group_id, number_of_extra_user, 'psw_salt'),
            TestDbQueries._data.get_user_data(group_id, number_of_extra_user, 'psw_hash'),
            group_id=group_id)
        self.assertFalse(res)

    def test_009_get_username_by_telegram_id(self):
        group_id: int = 4
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_4)
        res: str = (
            self.test_db.get_username_by_telegram_id(TestDbQueries._data.get_user_data(group_id,
                                                                                       number_of_user,
                                                                                       'telegram_id')))
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, number_of_user, 'username'))

    def test_010_get_telegram_id_by_username(self):
        group_id: int = 4
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_4)
        res: int = (
            self.test_db.get_telegram_id_by_username(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                         'username')))
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, number_of_user, 'telegram_id'))

    def test_011_get_group_id_by_token_1(self):
        group_id: int = 3
        res: int = self.test_db.get_group_id_by_token(TestDbQueries.group_3_token)
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'group_id'))

    def test_011_get_group_id_by_token_2(self):
        group_id: int = 4
        res: int = self.test_db.get_group_id_by_token(TestDbQueries.group_4_token)
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'group_id'))

    def test_012_get_group_id_by_telegram_id_1(self):
        group_id: int = 3
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_3)
        res: int = self.test_db.get_group_id_by_telegram_id(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                              'telegram_id'))
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, number_of_user, 'group_id'),
                         f'number_of_user = {number_of_user}')

    def test_012_get_group_id_by_telegram_id_2(self):
        group_id: int = 3
        number_of_user: int = 21
        res: int = self.test_db.get_group_id_by_telegram_id(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                              'telegram_id'))
        self.assertEqual(res, 0)

    def test_013_get_group_id_token_by_username_1(self):
        group_id: int = 3
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_3)
        res: tuple = self.test_db.get_group_id_token_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                                   number_of_user,
                                                                                                   'username'))
        self.assertEqual(res,
                         (TestDbQueries.group_3_token, TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                         'group_id')),
                         f'type(res) = {type(res)}')

    def test_013_get_group_id_token_by_username_2(self):
        group_id: int = 4
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_4)
        res: tuple = self.test_db.get_group_id_token_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                                   number_of_user,
                                                                                                   'username'))
        self.assertEqual(res,
                         (TestDbQueries.group_4_token, TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                         'group_id')),
                         f'type(res) = {type(res)}')

    def test_014_get_token_by_telegram_id_1(self):
        group_id: int = 3
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_3)
        res: str = self.test_db.get_token_by_telegram_id(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                           'telegram_id'))
        self.assertEqual(res, TestDbQueries.group_3_token)

    def test_014_get_token_by_telegram_id_2(self):
        group_id: int = 3
        number_of_user: int = 21
        res: str = self.test_db.get_token_by_telegram_id(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                           'telegram_id'))
        self.assertEqual(res, '')

    def test_015_get_salt_by_username_1(self):
        group_id: int = 3
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_3)
        res: str = self.test_db.get_salt_by_username(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                       'username'))
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, number_of_user, 'psw_salt'))

    def test_015_get_salt_by_username_2(self):
        group_id: int = 4
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_4)
        res: str = self.test_db.get_salt_by_username(TestDbQueries._data.get_user_data(group_id, number_of_user,
                                                                                       'username'))
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, number_of_user, 'psw_salt'))

    def test_016_auth_by_username_1(self):
        group_id: int = 3
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_3)
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                    number_of_user,
                                                                                    'username'),
                                                  TestDbQueries._data.get_user_data(group_id,
                                                                                    number_of_user,
                                                                                    'psw_hash'))
        self.assertTrue(res)

    def test_016_auth_by_username_2(self):
        group_id: int = 4
        number_of_user: int = randint(1, TestDbQueries._number_of_users_group_4)
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                    number_of_user,
                                                                                    'username'),
                                                  TestDbQueries._data.get_user_data(group_id,
                                                                                    number_of_user,
                                                                                    'psw_hash'))
        self.assertTrue(res)

    def test_016_auth_by_username_3(self):
        group_id: int = 3
        number_of_user: int = 21
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                    number_of_user,
                                                                                    'username'),
                                                  TestDbQueries._data.get_user_data(group_id,
                                                                                    number_of_user,
                                                                                    'psw_hash'))
        self.assertFalse(res)

    def test_016_auth_by_username_4(self):
        """
        We will use the data of different users for authorization
        """
        number_of_user: int = 1
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data(3, number_of_user, 'username'),
                                                  TestDbQueries._data.get_user_data(4, number_of_user, 'psw_hash'))
        self.assertFalse(res)

    def test_016_auth_by_username_5(self):
        group_id: int = 3
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                    3,
                                                                                    'username'),
                                                  TestDbQueries._data.get_user_data(group_id,
                                                                                    4,
                                                                                    'psw_hash'))
        self.assertFalse(res)

    def test_016_auth_by_username_6(self):
        group_id: int = 4
        res: bool = self.test_db.auth_by_username(TestDbQueries._data.get_user_data(group_id,
                                                                                    randint(1, 2),
                                                                                    'username'),
                                                  TestDbQueries._data.get_user_data(group_id,
                                                                                    randint(3, 4),
                                                                                    'psw_hash'))
        self.assertFalse(res)

    def test_017_get_group_usernames_1(self):
        group_id: int = 3
        res: tuple = self.test_db.get_group_usernames(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data(group_id, i, 'username')
                                    for i in range(1, TestDbQueries._number_of_users_group_3 + 1)))

    def test_017_get_group_usernames_2(self):
        group_id: int = 4
        res: tuple = self.test_db.get_group_usernames(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data(group_id, i, 'username')
                                    for i in range(1, TestDbQueries._number_of_users_group_4 + 1)))

    def test_017_get_group_usernames_3(self):
        group_id: int = 5  # non-existent group
        res: tuple = self.test_db.get_group_usernames(group_id)
        self.assertEqual(res, tuple())

    def test_018_get_group_telegram_ids_1(self):
        group_id: int = 3
        res: tuple = self.test_db.get_group_telegram_ids(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data(group_id, i, 'telegram_id')
                                    for i in range(1, TestDbQueries._number_of_users_group_3 + 1)))

    def test_018_get_group_telegram_ids_2(self):
        group_id: int = 4
        res: tuple = self.test_db.get_group_telegram_ids(group_id)
        self.assertEqual(res, tuple(TestDbQueries._data.get_user_data(group_id, i, 'telegram_id')
                                    for i in range(1, TestDbQueries._number_of_users_group_4 + 1)))

    def test_018_get_group_telegram_ids_3(self):
        group_id: int = 5  # non-existent group
        res: tuple = self.test_db.get_group_telegram_ids(group_id)
        self.assertEqual(res, tuple())

    def test_019_check_user_is_group_owner_by_telegram_id_1(self):
        group_id: int = 3
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(group_id, 1, 'telegram_id'),
            TestDbQueries._data.get_user_data(group_id, 1, 'group_id')
        )
        self.assertTrue(res)

    def test_019_check_user_is_group_owner_by_telegram_id_2(self):
        group_id: int = 4
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(group_id, 1, 'telegram_id'),
            TestDbQueries._data.get_user_data(group_id, 1, 'group_id')
        )
        self.assertTrue(res)

    def test_019_check_user_is_group_owner_by_telegram_id_3(self):
        group_id: int = 3
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(group_id, 2, 'telegram_id'),
            TestDbQueries._data.get_user_data(group_id, 2, 'group_id')
        )
        self.assertFalse(res)

    def test_019_check_user_is_group_owner_by_telegram_id_4(self):
        # data from different users
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(3, 1, 'telegram_id'), TestDbQueries._data.get_user_data(4, 1, 'group_id'))
        self.assertFalse(res)

    def test_019_check_user_is_group_owner_by_telegram_id_5(self):
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(4, randint(1, 5), 'telegram_id'),
            TestDbQueries._data.get_user_data(3, randint(10, 15), 'group_id'))
        self.assertFalse(res)

    def test_019_check_user_is_group_owner_by_telegram_id_6(self):
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(3, randint(1, 3), 'telegram_id'),
            TestDbQueries._data.get_user_data(4, randint(4, 5), 'group_id'))
        self.assertFalse(res)

    def test_019_check_user_is_group_owner_by_telegram_id_7(self):
        res: bool = self.test_db.check_user_is_group_owner_by_telegram_id(
            TestDbQueries._data.get_user_data(4, randint(3, 5), 'telegram_id'),
            TestDbQueries._data.get_user_data(3, randint(1, 2), 'group_id'))
        self.assertFalse(res)

    def test_020_get_group_owner_username_by_group_id_1(self):
        group_id: int = 3
        res: str = self.test_db.get_group_owner_username_by_group_id(
            TestDbQueries._data.get_user_data(group_id, 1, 'group_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'username'))

    def test_020_get_group_owner_username_by_group_id_2(self):
        group_id: int = 4
        res: str = self.test_db.get_group_owner_username_by_group_id(
            TestDbQueries._data.get_user_data(group_id, 1, 'group_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'username'))

    def test_020_get_group_owner_username_by_group_id_3(self):
        group_id: int = 3
        res: str = self.test_db.get_group_owner_username_by_group_id(
            TestDbQueries._data.get_user_data(group_id, 16, 'group_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'username'))

    def test_020_get_group_owner_username_by_group_id_4(self):
        group_id: int = 4
        res: str = self.test_db.get_group_owner_username_by_group_id(
            TestDbQueries._data.get_user_data(group_id, 3, 'group_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'username'))

    def test_020_get_group_owner_username_by_group_id_5(self):
        res: str = self.test_db.get_group_owner_username_by_group_id(
            # non-existent group
            10_000
        )
        self.assertEqual(res, '')

    def test_020_get_group_owner_username_by_group_id_6(self):
        res: str = self.test_db.get_group_owner_username_by_group_id(
            # negative number
            -10
        )
        self.assertEqual(res, '')

    def test_021_check_username_is_exist_1(self):
        group_id: int = 3
        res: bool = self.test_db.check_username_is_exist(
            TestDbQueries._data.get_user_data(group_id, 10, 'username')
        )
        self.assertTrue(res)

    def test_021_check_username_is_exist_2(self):
        group_id: int = 4
        res: bool = self.test_db.check_username_is_exist(
            TestDbQueries._data.get_user_data(group_id, 3, 'username')
        )
        self.assertTrue(res)

    def test_021_check_username_is_exist_3(self):
        group_id: int = 3
        res: bool = self.test_db.check_username_is_exist(
            TestDbQueries._data.get_user_data(group_id, 21, 'username')
        )
        self.assertFalse(res)

    def test_021_check_username_is_exist_4(self):
        res: bool = self.test_db.check_username_is_exist('')
        self.assertFalse(res)

    def test_022_check_telegram_id_is_exist_1(self):
        group_id: int = 3
        res: bool = self.test_db.check_telegram_id_is_exist(
            TestDbQueries._data.get_user_data(group_id, 15, 'telegram_id')
        )
        self.assertTrue(res)

    def test_022_check_telegram_id_is_exist_2(self):
        group_id: int = 4
        res: bool = self.test_db.check_telegram_id_is_exist(
            TestDbQueries._data.get_user_data(group_id, 5, 'telegram_id')
        )
        self.assertTrue(res)

    def test_022_check_telegram_id_is_exist_3(self):
        group_id: int = 3
        res: bool = self.test_db.check_telegram_id_is_exist(
            TestDbQueries._data.get_user_data(group_id, 21, 'telegram_id')
        )
        self.assertFalse(res)

    def test_022_check_telegram_id_is_exist_4(self):
        res: bool = self.test_db.check_telegram_id_is_exist(0)
        self.assertFalse(res)

    def test_023_check_token_is_unique_1(self):
        token: str = TestDbQueries.group_3_token
        res: bool = self.test_db.check_token_is_unique(token)
        self.assertFalse(res)

    def test_023_check_token_is_unique_2(self):
        token: str = TestDbQueries.group_4_token
        res: bool = self.test_db.check_token_is_unique(token)
        self.assertFalse(res)

    def test_023_check_token_is_unique_3(self):
        token: str = get_token()
        res: bool = self.test_db.check_token_is_unique(token)
        self.assertTrue(res)

    def test_023_check_token_is_unique_4(self):
        token: str = ''  # noqa
        res: bool = self.test_db.check_token_is_unique(token)
        self.assertTrue(res)  # the token type is incorrect, but there is no such thing in the database -> unique

    def test_024_check_limit_users_in_group_1(self):
        group_id: int = 3
        res: bool = self.test_db.check_limit_users_in_group(
            TestDbQueries._data.get_user_data(group_id, 12, 'group_id')
        )
        self.assertFalse(res, f'Group #{TestDbQueries._data.get_user_data(group_id, 12, 'group_id')}')

    def test_024_check_limit_users_in_group_2(self):
        group_id: int = 4
        res: bool = self.test_db.check_limit_users_in_group(
            TestDbQueries._data.get_user_data(group_id, 3, 'group_id')
        )
        self.assertTrue(res, f'Group #{TestDbQueries._data.get_user_data(group_id, 3, 'group_id')}')

    def test_024_check_limit_users_in_group_3(self):
        res: bool = self.test_db.check_limit_users_in_group(
            1_000  # non-existent group
        )
        self.assertFalse(res)

    def test_024_check_limit_users_in_group_4(self):
        group_id: int = 3
        res: bool = self.test_db.check_limit_users_in_group(
            TestDbQueries._data.get_user_data(group_id, 17, 'group_id')
        )
        self.assertFalse(res, f'Group #{TestDbQueries._data.get_user_data(group_id, 12, 'group_id')}')

    def test_024_check_limit_users_in_group_5(self):
        group_id: int = 4
        res: bool = self.test_db.check_limit_users_in_group(
            TestDbQueries._data.get_user_data(group_id, 1, 'group_id')
        )
        self.assertTrue(res, f'Group #{TestDbQueries._data.get_user_data(group_id, 3, 'group_id')}')

    def test_025_get_user_language_1(self):
        group_id: int = 3
        res: str = self.test_db.get_user_language(
            TestDbQueries._data.get_user_data(group_id, 1, 'telegram_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 1, 'language'))

    def test_025_get_user_language_2(self):
        group_id: int = 3
        res: str = self.test_db.get_user_language(
            TestDbQueries._data.get_user_data(group_id, 5, 'telegram_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 5, 'language'))

    def test_025_get_user_language_3(self):
        group_id: int = 3
        res: str = self.test_db.get_user_language(
            TestDbQueries._data.get_user_data(group_id, 16, 'telegram_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 16, 'language'))

    def test_025_get_user_language_4(self):
        group_id: int = 4
        res: str = self.test_db.get_user_language(
            TestDbQueries._data.get_user_data(group_id, 3, 'telegram_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 3, 'language'))

    def test_025_get_user_language_5(self):
        group_id: int = 4
        res: str = self.test_db.get_user_language(
            TestDbQueries._data.get_user_data(group_id, 5, 'telegram_id')
        )
        self.assertEqual(res, TestDbQueries._data.get_user_data(group_id, 5, 'language'))

    def test_025_get_user_language_6(self):
        res: str = self.test_db.get_user_language(0)  # non-existent user
        self.assertEqual(res, 'en')

    def test_026_transaction_cycle_1(self):
        """
        Checking that entries were successfully created and deleted:
        add_transaction_to_db -> check_record_id_is_exist = True ->
        -> process_delete_transaction_record -> check_record_id_is_exist = False
        """
        group_id: int = 3
        current_year: int = int(datetime.now().strftime("%Y"))

        for i in range(1, NUMBER_OF_TRANSACTION_CYCLE):
            if i % 2 == 0:
                res_1: bool = self.test_db.add_transaction_to_db(
                    randint(10, 100_000),
                    f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 9, current_year - 1)}',
                    get_salt()[:randint(1, 25)],  # category
                    str(i)[:randint(1, 50)],  # description
                    telegram_id=TestDbQueries._data.get_user_data(group_id,
                                                                  randint(1, TestDbQueries._number_of_users_group_3),
                                                                  'telegram_id')
                )
            else:
                res_1: bool = self.test_db.add_transaction_to_db(
                    randint(10, 100_000),
                    f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 9, current_year - 1)}',
                    get_salt()[:randint(1, 25)],  # category
                    str(i)[:randint(1, 50)],  # description
                    username=TestDbQueries._data.get_user_data(group_id,
                                                               randint(1, TestDbQueries._number_of_users_group_3),
                                                               'username')
                )
            self.assertTrue(res_1, f'Iteration number = {i}')

        for transaction_id in range(1, NUMBER_OF_TRANSACTION_CYCLE):
            res_2: bool = self.test_db.check_record_id_is_exist(group_id, transaction_id)
            self.assertTrue(res_2, f'Iteration number = {transaction_id}')

        for transaction_id in range(1, NUMBER_OF_TRANSACTION_CYCLE):
            res_3: bool = self.test_db.process_delete_transaction_record(group_id, transaction_id)
            # in the next loop we will remove these records from the set
            self.assertTrue(res_3, f'Iteration number = {transaction_id}')

        # We check that all entered entries have been deleted
        for deleted_transaction_id in range(1, NUMBER_OF_TRANSACTION_CYCLE):
            res_4: bool = self.test_db.check_record_id_is_exist(group_id, deleted_transaction_id)
            self.assertFalse(res_4, f'Iteration number = {deleted_transaction_id}')

    def test_026_transaction_cycle_2(self):
        """
        in this test example we remove random entries and check if the “totals” fields are recalculated correctly
        """
        group_id: int = 4
        current_year: int = int(datetime.now().strftime("%Y"))
        # use set so that there are no duplicate identifiers
        random_records_to_delete: tuple = tuple({
            randint(1, NUMBER_OF_TRANSACTION_CYCLE) for _ in range(NUMBER_OF_TRANSACTION_CYCLE // 10)
        })

        for i in range(1, NUMBER_OF_TRANSACTION_CYCLE):
            if i % 5 == 0:
                res_1: bool = self.test_db.add_transaction_to_db(
                    randint(10, 100_000),
                    f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 9, current_year - 1)}',
                    get_salt()[:randint(1, 25)],  # category
                    str(i)[:randint(1, 50)],  # description
                    telegram_id=TestDbQueries._data.get_user_data(group_id,
                                                                  randint(1, TestDbQueries._number_of_users_group_4),
                                                                  'telegram_id')
                )
            else:
                res_1: bool = self.test_db.add_transaction_to_db(
                    randint(10, 100_000),
                    f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 9, current_year - 1)}',
                    get_salt()[:randint(1, 25)],  # category
                    str(i)[:randint(1, 50)],  # description
                    username=TestDbQueries._data.get_user_data(group_id,
                                                               randint(1, TestDbQueries._number_of_users_group_4),
                                                               'username')
                )
            self.assertTrue(res_1, f'Iteration number = {i}')

        for transaction_id in range(1, NUMBER_OF_TRANSACTION_CYCLE):
            res_2: bool = self.test_db.check_record_id_is_exist(group_id, transaction_id)
            self.assertTrue(res_2, f'Iteration number = {transaction_id}')

        # delete randomly selected records
        for transaction_id in random_records_to_delete:
            res_3: bool = self.test_db.process_delete_transaction_record(group_id, transaction_id)
            self.assertTrue(res_3, f'Iteration number = {transaction_id}')

        # checking that records have been deleted
        for transaction_id in random_records_to_delete:
            res_4: bool = self.test_db.check_record_id_is_exist(group_id, transaction_id)
            self.assertFalse(res_4, f'Iteration number = {transaction_id}')

        # check that the calculation of the "total" fields is correct:
        req: tuple = self.test_db.select_data_for_household_table(group_id, 0)
        res: tuple = tuple((i[2], i[3]) for i in req[::-1])  # (transfer, total)

        res_for_first_transaction: bool = (res[0][0] == res[0][1])
        self.assertTrue(res_for_first_transaction, f'res_for_first_transaction = {res_for_first_transaction},'
                                                   f'res[0][0] = {res[0][0]}, res[0][1] = {res[0][1]}')

        for j in range(1, len(res)):
            diff: bool = (res[j][1] - res[j][0] == res[j - 1][1])
            self.assertTrue(diff, f'The amount in the transaction does not match #{j}, '
                                  f'res[j][1] = {res[j][1]}, res[j][0] = {res[j][0]}, '
                                  f'res[j-1][1] = {res[j - 1][1]} => '
                                  f'res[j][1] - res[j][0] = {res[j][1] - res[j][0]}')

    def test_026_transaction_cycle_3(self):
        """
        In this test case we check the correctness of deleting records within one date
        """
        group_id: int = 3
        test_date: str = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%d/%m/%Y")
        random_records_to_delete: tuple = tuple({
            randint(1, NUMBER_OF_TRANSACTION_CYCLE_FOR_ONE_DAY)
            for _ in range(NUMBER_OF_TRANSACTION_CYCLE_FOR_ONE_DAY // 2)
        })

        # check that the group table is empty
        res_1: tuple = self.test_db.select_data_for_household_table(group_id, 0)
        self.assertTrue(len(res_1) == 0)

        for i in range(1, NUMBER_OF_TRANSACTION_CYCLE_FOR_ONE_DAY):
            res_2: bool = self.test_db.add_transaction_to_db(
                randint(1_000, 10_000), test_date, get_salt()[:randint(1, 25)], str(i)[:randint(1, 50)],
                telegram_id=TestDbQueries._data.get_user_data(group_id,
                                                              randint(1, TestDbQueries._number_of_users_group_4),
                                                              'telegram_id')
            )
            self.assertTrue(res_2, f'Iteration number = {i}')

        for transaction_id in range(1, NUMBER_OF_TRANSACTION_CYCLE_FOR_ONE_DAY):
            # we have already recorded and deleted n = (NUMBER_OF_TRANSACTION_CYCLE) transactions from the table
            res_3: bool = self.test_db.check_record_id_is_exist(group_id, transaction_id)
            self.assertTrue(res_3, f'Iteration number = {transaction_id}')

        # delete randomly selected records
        for transaction_id in random_records_to_delete:
            res_4: bool = self.test_db.process_delete_transaction_record(group_id, transaction_id)
            self.assertTrue(res_4, f'Iteration number = {transaction_id}')

        # checking that records have been deleted
        for transaction_id in random_records_to_delete:
            res_5: bool = self.test_db.check_record_id_is_exist(group_id, transaction_id)
            self.assertFalse(res_5, f'Iteration number = {transaction_id}')

        # check that the calculation of the "total" fields is correct:
        req: tuple = self.test_db.select_data_for_household_table(group_id, 0)
        res: tuple = tuple((i[2], i[3]) for i in req[::-1])  # (transfer, total)

        res_for_first_transaction: bool = (res[0][0] == res[0][1])
        self.assertTrue(res_for_first_transaction, f'res_for_first_transaction = {res_for_first_transaction},'
                                                   f'res[0][0] = {res[0][0]}, res[0][1] = {res[0][1]}')

        for j in range(1, len(res)):
            diff: bool = (res[j][1] - res[j][0] == res[j - 1][1])
            self.assertTrue(diff, f'The amount in the transaction does not match #{j}, '
                                  f'res[j][1] = {res[j][1]}, res[j][0] = {res[j][0]}, '
                                  f'res[j-1][1] = {res[j - 1][1]} => '
                                  f'res[j][1] - res[j][0] = {res[j][1] - res[j][0]}')

    # TODO -> get_group_users_data
    # TODO -> update_user_last_login_by_telegram_id
    # TODO -> update_group_owner
    # TODO -> delete_username_from_group_by_telegram_id
    # TODO -> delete_group_with_users


class TestRegistrationServiceData:
    def __init__(self):
        self.__users_data: dict = {
                                      1:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10] + str(randint(10, 1000)),
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 30)]),
                                           'group_id': 5,  # owner
                                           'telegram_id': randint(10, 100000000000) * randint(1, 9)
                                           },
                                      2:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 10)]),
                                           'group_id': 5,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      3:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(10, 100)]),
                                           'group_id': 5,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      4:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:10],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()[:randint(1, 50)]),
                                           'group_id': 5,
                                           'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                           },
                                      5: {'language': LANGUAGES[randrange(LANG_LEN)],
                                          'username': str(randint(100, 1000000000)),
                                          'psw_salt': get_salt(),
                                          'psw_hash': getting_hash(get_salt(), get_salt()[:randint(5, 25)]),
                                          'group_id': 5,
                                          'telegram_id': randint(100, 100000000000) * randint(1, 9)
                                          }

                                  }

    @cache
    def get_user_data(self, attribute_1: int, attribute_2: str) -> int | str:
        return self.__users_data[attribute_1][attribute_2]

    @cache
    def get_number_of_users(self) -> int:
        return len(self.__users_data)


class TestRegistrationService(unittest.TestCase):
    _data = TestRegistrationServiceData()
    token_5_group: str = ''

    def test_050_user_registration_1(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db,
                                     'None',
                                     TestRegistrationService._data.get_user_data(1, 'telegram_id'),
                                     TestRegistrationService._data.get_user_data(1, 'username'),
                                     TestRegistrationService._data.get_user_data(1, 'psw_salt'),
                                     TestRegistrationService._data.get_user_data(1, 'psw_hash'))
        self.assertTrue(res)
        self.assertEqual(len(msg), 32)
        TestRegistrationService.token_5_group = self.test_db.get_token_by_telegram_id(
            TestRegistrationService._data.get_user_data(1, 'telegram_id')
        )
        self.assertEqual(TestRegistrationService.token_5_group, msg)
        close_test_db(self.connection)

    def test_050_user_registration_2(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        for i in range(2, TestRegistrationService._data.get_number_of_users() + 1):
            res, msg = user_registration(self.test_db,
                                         TestRegistrationService.token_5_group,
                                         TestRegistrationService._data.get_user_data(i, 'telegram_id'),
                                         TestRegistrationService._data.get_user_data(i, 'username'),
                                         TestRegistrationService._data.get_user_data(i, 'psw_salt'),
                                         TestRegistrationService._data.get_user_data(i, 'psw_hash'))
            self.assertTrue(res, f'i = {i}')
            self.assertEqual(msg, '', f'i = {i}')
        close_test_db(self.connection)

    def test_050_user_registration_3(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db,
                                     'None',
                                     TestRegistrationService._data.get_user_data(1, 'telegram_id'),
                                     TestRegistrationService._data.get_user_data(1, 'username'),
                                     TestRegistrationService._data.get_user_data(1, 'psw_salt'),
                                     TestRegistrationService._data.get_user_data(1, 'psw_hash'))
        close_test_db(self.connection)
        self.assertFalse(res)
        self.assertEqual(msg, 'create_new_user_or_group_error', f'msg = {msg}')

    def test_050_user_registration_4(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db,
                                     TestRegistrationService.token_5_group,
                                     TestRegistrationService._data.get_user_data(3, 'telegram_id'),
                                     TestRegistrationService._data.get_user_data(3, 'username'),
                                     TestRegistrationService._data.get_user_data(3, 'psw_salt'),
                                     TestRegistrationService._data.get_user_data(3, 'psw_hash'))
        close_test_db(self.connection)
        self.assertFalse(res)
        self.assertEqual(msg, 'group_is_full', f'msg = {msg}')

    def test_050_user_registration_5(self):
        invalid_username: str = TestRegistrationService._data.get_user_data(1, 'username').swapcase()
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db,
                                     'None',
                                     TestRegistrationService._data.get_user_data(1, 'telegram_id'),
                                     invalid_username,
                                     TestRegistrationService._data.get_user_data(1, 'psw_salt'),
                                     TestRegistrationService._data.get_user_data(1, 'psw_hash'))
        close_test_db(self.connection)
        self.assertFalse(res)
        self.assertEqual(msg, 'create_new_user_or_group_error', f'msg = {msg}')

    def test_050_user_registration_6(self):
        invalid_token: str = TestRegistrationService.token_5_group.swapcase()
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db,
                                     invalid_token,
                                     TestRegistrationService._data.get_user_data(2, 'telegram_id'),
                                     TestRegistrationService._data.get_user_data(2, 'username'),
                                     TestRegistrationService._data.get_user_data(2, 'psw_salt'),
                                     TestRegistrationService._data.get_user_data(2, 'psw_hash'))
        close_test_db(self.connection)
        self.assertFalse(res)
        self.assertEqual(msg, 'invalid_token_format', f'msg = {msg}\nlen(invalid_token) = {len(invalid_token)}')

    def test_050_user_registration_7(self):
        invalid_token: str = TestRegistrationService.token_5_group[::-1]
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db,
                                     invalid_token,
                                     TestRegistrationService._data.get_user_data(3, 'telegram_id'),
                                     TestRegistrationService._data.get_user_data(3, 'username'),
                                     TestRegistrationService._data.get_user_data(3, 'psw_salt'),
                                     TestRegistrationService._data.get_user_data(3, 'psw_hash'))
        close_test_db(self.connection)
        self.assertFalse(res)
        self.assertEqual(msg, 'group_not_exist', f'msg = {msg}\nlen(invalid_token) = {len(invalid_token)}')

    def test_050_user_registration_8(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)
        res, msg = user_registration(self.test_db, '', 0, '', '', '')
        close_test_db(self.connection)
        self.assertFalse(res)
        self.assertEqual(msg, 'invalid_token_format', f'msg = {msg}')


if __name__ == '__main__':
    unittest.main()
