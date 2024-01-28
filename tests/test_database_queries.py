import unittest
from app.database_control import DatabaseQueries
from app.encryption import getting_hash
from .manage_test_db import connect_test_db, close_test_db


class TestSelectQueries(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    def test_get_username_by_telegram_id_1(self):
        res = self.test_db.get_username_by_telegram_id(12345)
        self.assertEqual(res, "")

    def test_get_username_by_telegram_id_2(self):
        res = self.test_db.get_username_by_telegram_id(123456793)
        self.assertEqual(res, "Valentina")

    def test_get_username_by_telegram_id_3(self):
        res = self.test_db.get_username_by_telegram_id(1111111)
        self.assertEqual(res, "Kennedy")

    def test_get_username_by_telegram_id_4(self):
        res = self.test_db.get_username_by_telegram_id(11111111)
        self.assertEqual(res, "")

    def test_get_username_by_telegram_id_5(self):
        res = self.test_db.get_username_by_telegram_id(1234562)
        self.assertEqual(res, "Alessandro")

    def test_get_telegram_id_by_username_1(self):
        res = self.test_db.get_telegram_id_by_username("")
        self.assertEqual(res, 0)

    def test_get_telegram_id_by_username_2(self):
        res = self.test_db.get_telegram_id_by_username("Francesca")
        self.assertEqual(res, 123456797)

    def test_get_telegram_id_by_username_3(self):
        res = self.test_db.get_telegram_id_by_username("Alex1234")
        self.assertEqual(res, 0)

    def test_get_telegram_id_by_username_4(self):
        res = self.test_db.get_telegram_id_by_username("Aria")
        self.assertEqual(res, 123456785)

    def test_get_telegram_id_by_username_5(self):
        res = self.test_db.get_telegram_id_by_username("Hug0")
        self.assertEqual(res, 0)

    def test_get_group_id_by_token_1(self):
        res = self.test_db.get_group_id_by_token("3cf060bde115a4b3a3c29e7459150673")
        self.assertEqual(res, 1)

    def test_get_group_id_by_token_2(self):
        res = self.test_db.get_group_id_by_token("e00a6e6d1d1a54b017d5fa348534b7e8")
        self.assertEqual(res, 2)

    def test_get_group_id_by_token_3(self):
        res = self.test_db.get_group_id_by_token("3c376424479c9a92649721e23ff9cc9b")
        self.assertEqual(res, 10)

    def test_get_group_id_by_token_4(self):
        res = self.test_db.get_group_id_by_token("3c876424479c9b95379721e23ff9cc96")
        self.assertEqual(res, 0)

    def test_get_group_id_by_token_5(self):
        res = self.test_db.get_group_id_by_token("e00a6e6d1d1a54b01")
        self.assertEqual(res, 0)

    def test_get_group_id_by_token_6(self):
        res = self.test_db.get_group_id_by_token("")
        self.assertEqual(res, 0)

    def test_get_group_id_by_telegram_id_1(self):
        res = self.test_db.get_group_id_by_telegram_id(245386535)
        self.assertEqual(res, 0)

    def test_get_group_id_by_telegram_id_2(self):
        res = self.test_db.get_group_id_by_telegram_id(123456797)
        self.assertEqual(res, 1)

    def test_get_group_id_by_telegram_id_3(self):
        res = self.test_db.get_group_id_by_telegram_id(123456788)
        self.assertEqual(res, 1)

    def test_get_group_id_by_telegram_id_4(self):
        res = self.test_db.get_group_id_by_telegram_id(1234563)
        self.assertEqual(res, 2)

    def test_get_group_id_by_telegram_id_5(self):
        res = self.test_db.get_group_id_by_telegram_id(2222222)
        self.assertEqual(res, 3)

    def test_get_group_id_by_telegram_id_6(self):
        res = self.test_db.get_group_id_by_telegram_id(1111111)
        self.assertEqual(res, 10)

    def test_get_group_id_by_telegram_id_7(self):
        res = self.test_db.get_group_id_by_telegram_id(0)
        self.assertEqual(res, 0)

    def test_get_group_id_by_username_1(self):
        res = self.test_db.get_group_id_by_username("")
        self.assertEqual(res, 0)

    def test_get_group_id_by_username_2(self):
        res = self.test_db.get_group_id_by_username("Pierre")
        self.assertEqual(res, 0)

    def test_get_group_id_by_username_3(self):
        res = self.test_db.get_group_id_by_username("Stella")
        self.assertEqual(res, 1)

    def test_get_group_id_by_username_4(self):
        res = self.test_db.get_group_id_by_username("Kennedy")
        self.assertEqual(res, 10)

    def test_get_group_id_by_username_5(self):
        res = self.test_db.get_group_id_by_username("_Hugo")
        self.assertEqual(res, 0)

    def test_get_group_id_by_username_6(self):
        res = self.test_db.get_group_id_by_username("Alex_Alex12345")
        self.assertEqual(res, 1)

    def test_get_group_id_by_username_7(self):
        res = self.test_db.get_group_id_by_username("Alex12345")
        self.assertEqual(res, 0)

    def test_get_token_by_username_1(self):
        res = self.test_db.get_token_by_username("Giovanni")
        self.assertEqual(res, "3cf060bde115a4b3a3c29e7459150673")

    def test_get_token_by_username_2(self):
        res = self.test_db.get_token_by_username("Juliette_Juliette2")
        self.assertEqual(res, "3cf060bde115a4b3a3c29e7459150673")

    def test_get_token_by_username_3(self):
        res = self.test_db.get_token_by_username("Alessandro")
        self.assertEqual(res, "e00a6e6d1d1a54b017d5fa348534b7e8")

    def test_get_token_by_username_4(self):
        res = self.test_db.get_token_by_username("Nathan")
        self.assertEqual(res, "e00a6e6d1d1a54b017d5fa348534b7e8")

    def test_get_token_by_username_5(self):
        res = self.test_db.get_token_by_username("Francesca_1")
        self.assertEqual(res, "")

    def test_get_token_by_username_6(self):
        res = self.test_db.get_token_by_username("")
        self.assertEqual(res, "")

    def test_get_token_by_username_7(self):
        res = self.test_db.get_token_by_username("0livier")
        self.assertEqual(res, "")

    def test_get_token_by_telegram_id_1(self):
        res = self.test_db.get_token_by_telegram_id(0)
        self.assertEqual(res, "")

    def test_get_token_by_telegram_id_2(self):
        res = self.test_db.get_token_by_telegram_id(123456797)
        self.assertEqual(res, "3cf060bde115a4b3a3c29e7459150673")

    def test_get_token_by_telegram_id_3(self):
        res = self.test_db.get_token_by_telegram_id(123456792)
        self.assertEqual(res, "3cf060bde115a4b3a3c29e7459150673")

    def test_get_token_by_telegram_id_4(self):
        res = self.test_db.get_token_by_telegram_id(987654)
        self.assertEqual(res, "")

    def test_get_token_by_telegram_id_5(self):
        res = self.test_db.get_token_by_telegram_id(1111111)
        self.assertEqual(res, "3c376424479c9a92649721e23ff9cc9b")

    def test_get_salt_by_username_1(self):
        res = self.test_db.get_salt_by_username("Elena")
        self.assertEqual(res, "NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U")

    def test_get_salt_by_username_2(self):
        res = self.test_db.get_salt_by_username("Carter")
        self.assertEqual(res, "NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U")

    def test_get_salt_by_username_3(self):
        res = self.test_db.get_salt_by_username("")
        self.assertEqual(res, "")

    def test_get_salt_by_username_4(self):
        res = self.test_db.get_salt_by_username("Alex_Alex12345")
        self.assertEqual(res, "71Zwm1hvnlyD7eQUJK0RlfOBqF3lYhYY")

    def test_get_salt_by_username_5(self):
        res = self.test_db.get_salt_by_username("Kennedy")
        self.assertEqual(res, "NFqP8q7QrCZbBv6X4vfzf5Wxu3pjTU3T")

    def test_get_salt_by_username_6(self):
        res = self.test_db.get_salt_by_username("Inga")
        self.assertEqual(res, "")

    def test_get_salt_by_username_7(self):
        res = self.test_db.get_salt_by_username("Elsa")
        self.assertEqual(res, "")

    def test_select_data_for_household_table_1(self):
        res = len(self.test_db.select_data_for_household_table(1, 1))
        self.assertEqual(res, 1)

    def test_select_data_for_household_table_2(self):
        res = len(self.test_db.select_data_for_household_table(1, 4))
        self.assertEqual(res, 4)

    def test_select_data_for_household_table_3(self):
        res = self.test_db.select_data_for_household_table(1, 4)[0][2]
        self.assertEqual(res, "Hugo")

    def test_select_data_for_household_table_4(self):
        res = self.test_db.select_data_for_household_table(1, 3)[2][3]
        self.assertEqual(res, -500)

    def test_select_data_for_household_table_5(self):
        res = self.test_db.select_data_for_household_table(2, 2)
        self.assertEqual(res, [[3, 0, 'Alessandro', -240000, 'Other', '01/01/2021', None],
                               [2, 240000, 'Alessandro', 120000, 'Other', '01/01/2021', None]])

    def test_get_username_group_owner_by_group_id_1(self):
        res = self.test_db.get_group_owner_username_by_group_id(1)
        self.assertEqual(res, "Alex_Alex12345")

    def test_get_username_group_owner_by_group_id_2(self):
        res = self.test_db.get_group_owner_username_by_group_id(3)
        self.assertEqual(res, "Lincoln")

    def test_get_username_group_owner_by_group_id_3(self):
        res = self.test_db.get_group_owner_username_by_group_id(10)
        self.assertEqual(res, "Kennedy")

    def test_get_group_users_data_1(self):
        res = self.test_db.get_group_users_data(2)
        self.assertEqual(res, [['Grayson', '01/10/2023'], ['Alessandro', '01/10/2023'], ['Nathan', '01/10/2023']])

    def test_get_group_users_data_2(self):
        res = self.test_db.get_group_users_data(3)
        self.assertEqual(res, [['Lincoln', '01/10/2023']])

    def test_get_group_users_1(self):
        res = set(self.test_db.get_group_users(1))
        self.assertEqual(res, {'Alex_Alex12345', 'Thomas_Thomas1', 'Juliette_Juliette2', 'Alexandre_Alexandre0',
                                      'Hugo', 'Marco', 'Francesca', 'Giovanni', 'Isabella',
                                      'Giorgio', 'Valentina', 'Lorenzo', 'Elena', 'Vincenzo',
                                      'Bianca', 'Carter', 'Stella', 'Jackson', 'Aria', 'Olivier'})

    def test_get_group_users_2(self):
        res = set(self.test_db.get_group_users(2))
        self.assertEqual(res, {'Grayson', 'Alessandro', 'Nathan'})

    def test_get_group_users_3(self):
        res = self.test_db.get_group_users(10)
        self.assertEqual(res, ['Kennedy'])

    def test_check_record_id_is_exist_1(self):
        res = self.test_db.check_record_id_is_exist(1, 4)
        print(res)
        self.assertEqual(res, True)

    def test_check_record_id_is_exist_2(self):
        res = self.test_db.check_record_id_is_exist(1, 10)
        self.assertEqual(res, False)

    def test_check_record_id_is_exist_3(self):
        res = self.test_db.check_record_id_is_exist(10, 90)
        self.assertEqual(res, False)

    def test_check_record_id_is_exist_4(self):  # non-existent group
        res = self.test_db.check_record_id_is_exist(90, 90)
        self.assertEqual(res, False)

    def test_check_record_id_is_exist_5(self):
        res = self.test_db.check_record_id_is_exist(1, 1)
        self.assertEqual(res, True)

    def test_check_username_is_exist_1(self):
        res = self.test_db.check_username_is_exist("Lorenzo")
        self.assertEqual(res, True)

    def test_check_username_is_exist_2(self):
        res = self.test_db.check_username_is_exist("Andrey")
        self.assertEqual(res, False)

    def test_check_username_is_exist_3(self):
        res = self.test_db.check_username_is_exist("Stella")
        self.assertEqual(res, True)

    def test_check_token_is_unique_1(self):
        res = self.test_db.check_token_is_unique("3cf060bde115a4b3a3c29e7459150673")
        self.assertEqual(res, False)

    def test_check_token_is_unique_2(self):
        res = self.test_db.check_token_is_unique("3c37dhq447974592649721e23ff9cc9b")
        self.assertEqual(res, True)

    def test_check_token_is_unique_3(self):  #
        # the length will not pass validation, but the function only looks for presence in the database
        res = self.test_db.check_token_is_unique("")
        self.assertEqual(res, True)

    def test_check_telegram_id_is_exist_1(self):  #
        res = self.test_db.check_telegram_id_is_exist(123456791)
        self.assertEqual(res, True)

    def test_check_telegram_id_is_exist_2(self):  #
        res = self.test_db.check_telegram_id_is_exist(22222221)
        self.assertEqual(res, False)

    def test_check_telegram_id_is_exist_3(self):  #
        res = self.test_db.check_telegram_id_is_exist(123456780)
        self.assertEqual(res, True)

    def test_check_username_is_group_owner_1(self):
        res = self.test_db.check_username_is_group_owner("Grayson", 2)
        self.assertEqual(res, True)

    def test_check_username_is_group_owner_2(self):
        res = self.test_db.check_username_is_group_owner("Alex_Alex12345", 1)
        self.assertEqual(res, True)

    def test_check_username_is_group_owner_3(self):  # Non-existent group and existing user
        res = self.test_db.check_username_is_group_owner("Alex_Alex12345", 20)
        self.assertEqual(res, False)

    def test_check_username_is_group_owner_4(self):  # Non-existent group and non-existent user
        res = self.test_db.check_username_is_group_owner("Lucia", 50)
        self.assertEqual(res, False)

    def test_check_limit_users_in_group_1(self):
        res = self.test_db.check_limit_users_in_group(1)
        self.assertEqual(res, False)

    def test_check_limit_users_in_group_2(self):
        res = self.test_db.check_limit_users_in_group(2)
        self.assertEqual(res, True)

    def test_check_limit_users_in_group_3(self):  # A group with this id does not exist - the except block will work
        res = self.test_db.check_limit_users_in_group(15)
        self.assertEqual(res, False)

    def test_get_user_language_1(self):
        res = self.test_db.get_user_language(123456783)
        self.assertEqual(res, "en")

    def test_get_user_language_2(self):
        res = self.test_db.get_user_language(123456780)
        self.assertEqual(res, "ru")

    def test_get_user_language_3(self):
        res = self.test_db.get_user_language(123456793)
        self.assertEqual(res, "es")

    def test_get_user_language_4(self):
        res = self.test_db.get_user_language(123456786)
        self.assertEqual(res, "is")

    def test_get_user_language_5(self):
        res = self.test_db.get_user_language(1234563)
        self.assertEqual(res, "de")

    def test_get_user_language_6(self):  # This user does not exist
        res = self.test_db.get_user_language(22222220)
        self.assertEqual(res, "en")

    def test_get_last_sum_in_group_1(self):  # non-existent group
        res = self.test_db.get_last_sum_in_group(99)
        self.assertEqual(res, 0)

    def test_get_last_sum_in_group_2(self):
        res = self.test_db.get_last_sum_in_group(1)
        self.assertEqual(res, 37500)

    def test_get_last_sum_in_group_3(self):
        res = self.test_db.get_last_sum_in_group(2)
        self.assertEqual(res, 0)

    def test_get_last_sum_in_group_4(self):  # Table budget_10 is empty
        res = self.test_db.get_last_sum_in_group(10)
        self.assertEqual(res, 0)


class TestUserAuthentication(unittest.TestCase):
    def setUp(self):
        self.connection = connect_test_db()
        self.test_db = DatabaseQueries(self.connection)

    def tearDown(self):
        close_test_db(self.connection)

    def test_auth_by_username_1(self):
        _username = "Francesca"
        _psw_hash = "7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_2(self):
        _username = "Alex_Alex12345"
        _psw_hash = "c20b735096a231a491d94fe15de5cfefd181c82ae8cef38f3abb9174feddf98d"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_3(self):
        _username = "Lincoln"
        _psw_hash = "65c70178e16b2fb28667f10fdab320fc128e0dc71bf1f5725e29e145972e0cdd"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_4(self):  # non-existent user
        _username = "Emily"
        _psw_hash = "7755b9530865376123985c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_5(self):  # non-existent user
        _username = "Alex"
        _psw_hash = "7755b984ia86bf1468005c6ef04a1fa7f0516a7e22nd91efac91b19e4cl2b879"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_6(self):  # non-existent user
        _username = "Greta"
        _psw_hash = "7755b9530865376123985c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_7(self):  # correct username and incorrect hash
        _username = "Marco"
        _psw_hash = "7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b879"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_8(self):  # correct username and incorrect hash
        _username = "Kennedy"
        _psw_hash = "9aa93aa6aeb222654c3deb2f5e6e004db066a972cb2a08b7038926fd45f99f05"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_9(self):  # correct username and incorrect hash
        _username = "Alex_Alex12345"
        _psw_hash = "c20b735096a231a491d64fe15de5cfefd181c82ae8cef38f3abb9174feddf98d"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_10(self):  # incorrect username and correct hash
        _username = ""
        _psw_hash = "7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_11(self):  # incorrect username and correct hash
        _username = "Alex"
        _psw_hash = "c20b735096a231a491d94fe15de5cfefd181c82ae8cef38f3abb9174feddf98d"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_12(self):  # incorrect username and correct hash
        _username = "elena"
        _psw_hash = "7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_13(self):  # correct username and incorrect hash
        _username = "Alex_Alex12345"
        _psw_hash = "c20b735096a231a491d94fe15de5cfefd181c82ae8cef38f3abb9174feddf98"
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_14(self):
        _username = "Alex_Alex12345"
        _psw = "Alex12345"
        _psw_salt = "71Zwm1hvnlyD7eQUJK0RlfOBqF3lYhYY"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_15(self):
        _username = "Thomas_Thomas1"
        _psw = "Thomas1"
        _psw_salt = "eFrt7GqNHlFHLMbmcE2U8Fc1x0ysMMQJ"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_16(self):
        _username = "Giorgio"
        _psw = "qwerty"
        _psw_salt = "NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_17(self):
        _username = "Nathan"
        _psw = "qwerty"
        _psw_salt = "Shvugemj43TFPcnyIQ4MWPnKhdo7q3Ee"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_18(self):
        _username = "Kennedy"
        _psw = "qwerty"
        _psw_salt = "NFqP8q7QrCZbBv6X4vfzf5Wxu3pjTU3T"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, True)

    def test_auth_by_username_19(self):  # incorrect username
        _username = "Inga"
        _psw = "qwerty"
        _psw_salt = "NFqP8q7QrCZbBv6X4vfzf5Wxu3pjTU3T"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_20(self):  # incorrect username
        _username = "Alex12345"
        _psw = "Alex12345"
        _psw_salt = "71Zwm1hvnlyD7eQUJK0RlfOBqF3lYhYY"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_21(self):  # incorrect salt
        _username = "Alex"
        _psw = "Alex12345"
        _psw_salt = "81Zwm1hvnlyD7eQUJK0RlfOBqF3lYhYY"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)

    def test_auth_by_username_22(self):  # incorrect username and salt
        _username = "Alex123"
        _psw = "Alex12345"
        _psw_salt = "81Zwm1hvnlyD7eQUJK0RlfOBqF3lYhYY"
        _psw_hash = getting_hash(_psw, _psw_salt)
        res = self.test_db.auth_by_username(_username, _psw_hash)
        self.assertEqual(res, False)


if __name__ == '__main__':
    unittest.main()
