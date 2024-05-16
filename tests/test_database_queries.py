# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import unittest
from budget_graph.db_manager import DatabaseQueries
from tests.manage_test_db import connect_test_db, close_test_db


class TestSelectQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    def test_get_username_by_telegram_id_1(self):
        res = self.test_db.get_username_by_telegram_id()
        self.assertEqual(res, "")


class TestUserAuthentication(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    def test_auth_by_username_1(self):
        _username = ""
        _psw_hash = ""
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()
