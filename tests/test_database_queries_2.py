import unittest
from random import randint, randrange
from functools import cache
# from datetime import datetime, timedelta, timezone

from budget_graph.db_manager import DatabaseQueries
from budget_graph.dictionary import get_list_languages
# from budget_graph.registration_service import user_registration
from budget_graph.encryption import getting_hash, get_salt, get_token

from tests.build_test_infrastructure import connect_test_db, close_test_db

LANGUAGES: tuple = get_list_languages()
LANG_LEN: int = len(LANGUAGES)


class DatabaseTestData1:
    """
    Data class, interaction only through methods to avoid data modification
    """
    def __init__(self):
        self.__users_data_1: dict = {
                                      1:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:3],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 1,  # owner
                                           'telegram_id': randint(100, 1000)
                                           },
                                      2:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:4],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 1,
                                           'telegram_id': randint(10000, 100000)
                                           },
                                      3:  {'language': LANGUAGES[randrange(LANG_LEN)],
                                           'username': get_token()[:5],
                                           'psw_salt': get_salt(),
                                           'psw_hash': getting_hash(get_salt(), get_salt()),
                                           'group_id': 1,
                                           'telegram_id': randint(1000000, 10000000)
                                           }
                                     }

        self.__users_data_2: dict = {
                                    1: {'language': LANGUAGES[randrange(LANG_LEN)],
                                        'username': get_token()[:5],
                                        'psw_salt': get_salt(),
                                        'psw_hash': getting_hash(get_salt(), get_salt()),
                                        'group_id': 2,  # owner
                                        'telegram_id': randint(1000, 10000) * randint(3, 9)
                                        }
                                }

    @cache
    def get_user_data(self, group_id: int, attribute_1: int, attribute_2: str) -> int | str:
        if group_id == 1:
            return self.__users_data_1[attribute_1][attribute_2]
        return self.__users_data_2[attribute_1][attribute_2]

    @cache
    def get_number_of_users(self, group_id: int) -> int:
        if group_id == 1:
            return len(self.__users_data_1)
        return len(self.__users_data_2)


class TestDbQueries1(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    _data = DatabaseTestData1()
    _number_of_users_group_1: int = _data.get_number_of_users(1)
    _number_of_users_group_2: int = _data.get_number_of_users(2)

    group_1_token: str = ''
    group_2_token: str = ''

    def test_001_add_users_to_db_1(self):
        for i in range(1, TestDbQueries1._number_of_users_group_1 + 1):
            group_id: int | None = None if i == 1 else TestDbQueries1._data.get_user_data(1, i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                TestDbQueries1._data.get_user_data(1, i, 'telegram_id'),
                TestDbQueries1._data.get_user_data(1, i, 'username'),
                TestDbQueries1._data.get_user_data(1, i, 'psw_salt'),
                TestDbQueries1._data.get_user_data(1, i, 'psw_hash'),
                group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f'Failed at iteration: {i}')
                TestDbQueries1.group_1_token = res
            else:
                self.assertEqual(res, True, f'Failed at iteration: {i}')

    def test_001_add_users_to_db_2(self):
        for i in range(1, TestDbQueries1._number_of_users_group_2 + 1):
            group_id: int | None = None if i == 1 else TestDbQueries1._data.get_user_data(2, i, 'group_id')
            res: bool | str = self.test_db.registration_new_user(
                TestDbQueries1._data.get_user_data(2, i, 'telegram_id'),
                TestDbQueries1._data.get_user_data(2, i, 'username'),
                TestDbQueries1._data.get_user_data(2, i, 'psw_salt'),
                TestDbQueries1._data.get_user_data(2, i, 'psw_hash'),
                group_id=group_id)
            if group_id is None:
                self.assertEqual(len(res), 32, f'Failed at iteration: {i}')
                TestDbQueries1.group_2_token = res
            else:
                self.assertTrue(res, f'Failed at iteration: {i}')

    def test_002_add_feature_1_to_db_1(self):
        group_id: int = 1
        # False -> True
        self.test_db.change_feature_status_del_msg_after_transaction(
            TestDbQueries1._data.get_user_data(group_id, 1, 'telegram_id')
        )
        res: bool = self.test_db.get_feature_status_del_msg_after_transaction(
            TestDbQueries1._data.get_user_data(group_id, 1, 'telegram_id')
        )
        self.assertTrue(res)

    def test_002_add_feature_1_to_db_2(self):
        group_id: int = 1
        res: bool = self.test_db.get_feature_status_del_msg_after_transaction(
            TestDbQueries1._data.get_user_data(group_id, 2, 'telegram_id')
        )
        self.assertFalse(res)

    def test_002_add_feature_1_to_db_3(self):
        group_id: int = 2
        res: bool = self.test_db.get_feature_status_del_msg_after_transaction(
            TestDbQueries1._data.get_user_data(group_id, 1, 'telegram_id')
        )
        self.assertFalse(res)

    def test_003_add_user_timezone_to_db_1(self):
        group_id: int = 1

    def test_003_add_user_timezone_to_db_2(self):
        group_id: int = 1

    def test_003_add_user_timezone_to_db_3(self):
        group_id: int = 2

