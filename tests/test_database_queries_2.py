import unittest
from random import randint, randrange
from functools import cache
from datetime import datetime

from budget_graph.db_manager import DatabaseQueries
from budget_graph.dictionary import get_list_languages
from budget_graph.registration_service import user_registration
from budget_graph.encryption import getting_hash, get_salt, get_token

from tests.build_test_infrastructure import connect_test_db, close_test_db, prepare_db_tables_for_tests

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
                group_id=group_id
            )
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
                group_id=group_id
            )
            if group_id is None:
                self.assertEqual(len(res), 32, f'Failed at iteration: {i}')
                TestDbQueries1.group_2_token = res
            else:
                self.assertTrue(res, f'Failed at iteration: {i}')

    def test_002_add_feature_1_to_db_1(self):
        """ OFF -> ON """
        group_id: int = 1
        user_id_in_group: int = TestDbQueries1._number_of_users_group_1

        old_res: bool = self.test_db.get_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        # change status
        self.test_db.change_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        new_res: bool = self.test_db.get_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        self.assertTrue(
            (
                    (old_res is False) and (new_res is True)
            ),
            f'1. old_res is False = {old_res is False}\n'
            f'2. new_res is True = {new_res is True}')

    def test_002_add_feature_1_to_db_2(self):
        group_id: int = 1
        res: bool = self.test_db.get_feature_status(
            TestDbQueries1._data.get_user_data(group_id, 2, 'telegram_id'), 'del_msg_after_transaction'
        )
        self.assertFalse(res)

    def test_002_add_feature_1_to_db_3(self):
        """ OFF -> ON -> OFF """
        group_id: int = 2
        user_id_in_group: int = randint(1, TestDbQueries1._number_of_users_group_2)

        off_feature: bool = self.test_db.get_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        # change status
        self.test_db.change_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        on_feature: bool = self.test_db.get_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        # change status
        self.test_db.change_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        new_off_feature: bool = self.test_db.get_feature_status(
            TestDbQueries1._data.get_user_data(group_id, user_id_in_group, 'telegram_id'), 'del_msg_after_transaction'
        )

        self.assertTrue(
            (
                (off_feature is False) and (on_feature is True) and (new_off_feature is False)
            ),
            f'1. off_feature is False = {off_feature is False}\n'
            f'2. on_feature is True = {on_feature is True}\n'
            f'3. new_off_feature is False = {new_off_feature is False}')

    def test_003_user_timezone_to_db_1(self):
        """
        SELECT #1
        """
        group_id: int = 1
        telegram_id: int = TestDbQueries1._data.get_user_data(
            group_id,
            randint(1, TestDbQueries1._number_of_users_group_1),
            'telegram_id'
        )
        res: int = self.test_db.get_user_timezone_by_telegram_id(telegram_id)
        self.assertEqual(res, 0)

    def test_003_user_timezone_to_db_2(self):
        """
        SELECT #2
        """
        group_id: int = 2
        telegram_id: int = TestDbQueries1._data.get_user_data(
            group_id,
            TestDbQueries1._number_of_users_group_2,
            'telegram_id'
        )
        res: int = self.test_db.get_user_timezone_by_telegram_id(telegram_id)
        self.assertEqual(res, 0)

    def test_003_user_timezone_to_db_3(self):
        """
        SELECT -> UPDATE/SET -> SELECT
        """
        group_id: int = 1
        telegram_id: int = TestDbQueries1._data.get_user_data(
            group_id,
            randint(1, TestDbQueries1._number_of_users_group_1),
            'telegram_id'
        )
        timezone: int = randint(-12, 12)
        self.test_db.add_user_timezone(telegram_id, timezone)
        res: int | None = self.test_db.get_user_timezone_by_telegram_id(telegram_id)
        self.assertEqual(res, timezone)

    def test_003_user_timezone_to_db_4(self):
        """
        SELECT -> UPDATE/SET -> SELECT
        """
        group_id: int = 1
        telegram_id: int = TestDbQueries1._data.get_user_data(
            group_id,
            randint(1, TestDbQueries1._number_of_users_group_2),
            'telegram_id'
        )
        timezone: int = randint(-12, 12)
        self.test_db.add_user_timezone(telegram_id, timezone)
        res: int | None = self.test_db.get_user_timezone_by_telegram_id(telegram_id)
        self.assertEqual(res, timezone)

    def test_003_user_timezone_to_db_5(self):
        """
        double changes
        """
        group_id: int = 1
        telegram_id: int = TestDbQueries1._data.get_user_data(
            group_id,
            randint(1, TestDbQueries1._number_of_users_group_2),
            'telegram_id'
        )

        timezone_1: int = randint(0, 12)
        self.test_db.add_user_timezone(telegram_id, timezone_1)
        res_1: int | None = self.test_db.get_user_timezone_by_telegram_id(telegram_id)
        self.assertEqual(res_1, timezone_1)

        timezone_2: int = randint(-12, -1)
        self.test_db.add_user_timezone(telegram_id, timezone_2)
        res_2: int | None = self.test_db.get_user_timezone_by_telegram_id(telegram_id)
        self.assertEqual(res_2, timezone_2)

    def test_003_user_timezone_to_db_6(self):
        """
        id = 0
        """
        res: int | None = self.test_db.get_user_timezone_by_telegram_id(0)
        self.assertIsNone(res)

    def test_003_user_timezone_to_db_7(self):
        """
        negative integers
        """
        for i in range(-100, 0):
            res: int = self.test_db.get_user_timezone_by_telegram_id(i)
            self.assertIsNone(res, f'i = {i}')

    def test_004_update_group_uuid_after_transaction_1(self):
        """
        check that the new group has uuid = null
        """
        group_id: int = 1
        res: str = self.test_db.get_group_transaction_uuid(group_id)
        self.assertEqual(res, '')

    def test_004_update_group_uuid_after_transaction_2(self):
        """
        check that the new group has uuid = null
        """
        group_id: int = 2
        res: str = self.test_db.get_group_transaction_uuid(group_id)
        self.assertEqual(res, '')

    def test_004_update_group_uuid_after_transaction_3(self):
        """
        check that uuid changes during transactions
        """
        group_id: int = 1
        current_year: int = int(datetime.now().strftime('%Y'))

        self.test_db.add_transaction_to_db(
            randint(10, 100_000),
            f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 9, current_year - 1)}',
            get_salt()[:randint(1, 25)],
            'qwerty',
            telegram_id=TestDbQueries1._data.get_user_data(group_id, 1, 'telegram_id')
        )

        res_1: str = self.test_db.get_group_transaction_uuid(group_id)

        self.assertEqual(len(res_1), 36, f'len = {len(res_1)}')

        self.test_db.add_transaction_to_db(
            randint(1_000, 1_000_000),
            f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 5, current_year - 1)}',
            get_salt()[:randint(1, 25)],
            '',
            telegram_id=TestDbQueries1._data.get_user_data(group_id, 2, 'telegram_id')
        )

        res_2: str = self.test_db.get_group_transaction_uuid(group_id)

        self.assertEqual(len(res_2), 36, f'len = {len(res_2)}')

        self.assertNotEqual(res_1, res_2, f'res_1 = {res_1}\n'
                                          f'res_2 = {res_2}')

    def test_004_update_group_uuid_after_transaction_4(self):
        """
        check that after a transaction in one group, the uuid in the other has not changed
        """
        group_id: int = 2
        group_id_for_check: int = 1
        current_year: int = int(datetime.now().strftime('%Y'))

        res_1: str = self.test_db.get_group_transaction_uuid(group_id_for_check)

        group_2_uuid_1: str = self.test_db.get_group_transaction_uuid(group_id)

        self.test_db.add_transaction_to_db(
            randint(10, 100_000),
            f'{randint(1, 28)}/{randint(1, 12)}/{randint(current_year - 5, current_year - 3)}',
            get_salt()[:randint(1, 20)],
            'qwerty',
            telegram_id=TestDbQueries1._data.get_user_data(
                group_id,
                TestDbQueries1._number_of_users_group_2,
                'telegram_id'
            )
        )

        group_2_uuid_2: str = self.test_db.get_group_transaction_uuid(group_id)

        self.assertNotEqual(group_2_uuid_1, group_2_uuid_2, f'group_2_uuid_1 = {group_2_uuid_1}\n'
                                                            f'group_2_uuid_2 = {group_2_uuid_2}')

        res_2: str = self.test_db.get_group_transaction_uuid(group_id_for_check)

        self.assertEqual(res_1, res_2, f'res_1 = {res_1}\n'
                                       f'res_2 = {res_2}')

    def test_005_get_group_users_data_1(self):
        group_id: int = 1

        res = self.test_db.get_group_users_data(group_id)

        self.assertEqual(len(res), 3, f'len(res) = {len(res)}')
        self.assertTrue(isinstance(res[0], list), f'type(res[0]) = {type(res[0])}')
        self.assertTrue(isinstance(res[0][0], str), f'type(res[0]) = {type(res[0][0])}')
        self.assertTrue(isinstance(res[0][1], datetime), f'type(res[0]) = {type(res[0][1])}')

    def test_005_get_group_users_data_2(self):
        group_id: int = 2

        res = self.test_db.get_group_users_data(group_id)

        self.assertEqual(len(res), 1, f'len(res) = {len(res)}')
        self.assertTrue(isinstance(res[0], list), f'type(res[0]) = {type(res[0])}')
        self.assertTrue(isinstance(res[0][0], str), f'type(res[0]) = {type(res[0][0])}')
        self.assertTrue(isinstance(res[0][1], datetime), f'type(res[0]) = {type(res[0][1])}')

    def test_005_get_group_users_data_3(self):
        group_id: int = 3

        res = self.test_db.get_group_users_data(group_id)

        self.assertEqual(len(res), 0, f'len(res) = {len(res)}')
        self.assertTrue(isinstance(res, list), f'type(res[0]) = {type(res)}')

    def test_005_get_group_users_data_4(self):
        group_id: int = 0

        res = self.test_db.get_group_users_data(group_id)

        self.assertEqual(len(res), 0, f'len(res) = {len(res)}')
        self.assertTrue(isinstance(res, list), f'type(res[0]) = {type(res)}')

    def test_005_get_group_users_data_5(self):
        group_id: int = -1

        res = self.test_db.get_group_users_data(group_id)

        self.assertEqual(len(res), 0, f'len(res) = {len(res)}')
        self.assertTrue(isinstance(res, list), f'type(res[0]) = {type(res)}')

    def test_006_delete_user_from_group_by_telegram_id_1(self):
        """ First we create a new one - then we delete it """
        # let's use the universal registration service
        telegram_id: int = randint(10000, 1000000) * randint(5, 7)
        res: tuple[bool, str] = user_registration(
            self.test_db,
            TestDbQueries1.group_1_token,
            telegram_id,
            get_token()[:8],
            get_salt(),
            getting_hash(get_salt(), get_salt())

        )

        # check the registration status
        self.assertTrue(res[0])
        self.assertEqual(res[1], '', f'res = {res}')

        res: list = self.test_db.get_group_users_data(1)
        self.assertEqual(len(res), 4, f'len(res) = {len(res)}')

        # we check that such a user is in the group
        group_id: int = self.test_db.get_group_id_by_telegram_id(telegram_id)
        self.assertEqual(group_id, 1, f'group_id = {group_id}')

        exists_res: bool = self.test_db.check_telegram_id_is_exist(telegram_id)
        self.assertTrue(exists_res)

        # delete user
        del_res: bool = self.test_db.delete_user_from_group_by_telegram_id(telegram_id)
        self.assertTrue(del_res)

        res: list = self.test_db.get_group_users_data(1)
        self.assertEqual(len(res), 3, f'len(res) = {len(res)}')

        # check the user group again
        group_id: int = self.test_db.get_group_id_by_telegram_id(telegram_id)
        self.assertEqual(group_id, 0, f'group_id = {group_id}')

        exists_res: bool = self.test_db.check_telegram_id_is_exist(telegram_id)
        self.assertFalse(exists_res)

    def test_006_delete_user_from_group_by_telegram_id_2(self):
        """ Removing a non-existent user """
        telegram_id: int = randint(1000000, 100000000) * randint(8, 9)

        exists_res: bool = self.test_db.check_telegram_id_is_exist(telegram_id)
        self.assertFalse(exists_res)

        del_res: bool = self.test_db.delete_user_from_group_by_telegram_id(telegram_id)
        self.assertTrue(del_res)

        exists_res: bool = self.test_db.check_telegram_id_is_exist(telegram_id)
        self.assertFalse(exists_res)

    def test_006_delete_user_from_group_by_telegram_id_3(self):
        """ delete existing user """
        group_id: int = TestDbQueries1._data.get_user_data(1, 1, 'group_id')

        telegram_id: int = TestDbQueries1._data.get_user_data(
            group_id,
            3,
            'telegram_id'
        )

        group_id: int = self.test_db.get_group_id_by_telegram_id(telegram_id)
        self.assertEqual(group_id, 1, f'group_id = {group_id}')

        exists_res: bool = self.test_db.check_telegram_id_is_exist(telegram_id)
        self.assertTrue(exists_res)

        res: list = self.test_db.get_group_users_data(group_id)
        self.assertEqual(len(res), 3, f'len(res) = {len(res)}')

        # delete user
        del_res: bool = self.test_db.delete_user_from_group_by_telegram_id(telegram_id)
        self.assertTrue(del_res)

        # check the user group again
        group_id: int = self.test_db.get_group_id_by_telegram_id(telegram_id)
        self.assertEqual(group_id, 0, f'group_id = {group_id}')

        exists_res: bool = self.test_db.check_telegram_id_is_exist(telegram_id)
        self.assertFalse(exists_res)

        res: list = self.test_db.get_group_users_data(1)
        self.assertEqual(len(res), 2, f'len(res) = {len(res)}')


if __name__ == '__main__':
    prepare_db_tables_for_tests()  # clear the database (required for local running outside the test environment)
    unittest.main()
