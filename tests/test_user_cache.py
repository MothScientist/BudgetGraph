import unittest
from budget_graph.user_cache_structure import UserLanguageCache, UserRegistrationStatusCache
from budget_graph.dictionary import get_list_languages


class TestUserLanguageCache(unittest.TestCase):
    lang: tuple = get_list_languages()

    def test_language_cache_1(self):
        # getting access to a private attribute of a class
        obj_1 = UserLanguageCache()
        # clear the cache after the last test
        obj_1._UserLanguageCache__telegram_language_cache.clear()  # noqa
        """
        since the class attribute is not bound to the object, it will have a common state in different objects;
        this is done on purpose - since in this case the cache will be consistent between different modules.

        therefore, for our tests, it should be cleared, because we would try to test its initial state.
        """
        for i in range(50):
            UserLanguageCache.input_cache_data(i + 1, TestUserLanguageCache.lang[i % 6])
        res = len(obj_1._UserLanguageCache__telegram_language_cache)  # noqa
        self.assertEqual(res, 50)

    def test_language_cache_2(self):
        obj_2 = UserLanguageCache()
        obj_2._UserLanguageCache__telegram_language_cache.clear()  # noqa
        for i in range(50):
            UserLanguageCache.input_cache_data(i + 1, TestUserLanguageCache.lang[i % 6])
        UserLanguageCache.input_cache_data(1, 'de')
        UserLanguageCache.input_cache_data(2, 'fr')
        UserLanguageCache.input_cache_data(3, 'is')
        res = len(obj_2._UserLanguageCache__telegram_language_cache)  # noqa
        self.assertEqual(res, 50)

    def test_language_cache_3(self):
        obj_3 = UserLanguageCache()
        obj_3._UserLanguageCache__telegram_language_cache.clear()  # noqa
        for i in range(51):
            UserLanguageCache.input_cache_data(i + 1, TestUserLanguageCache.lang[i % 6])
        res = len(obj_3._UserLanguageCache__telegram_language_cache)  # noqa
        self.assertEqual(res, 51)

    def test_language_cache_4(self):
        obj_4 = UserLanguageCache()
        obj_4._UserLanguageCache__telegram_language_cache.clear()  # noqa
        for i in range(52):
            UserLanguageCache.input_cache_data(i + 1, TestUserLanguageCache.lang[i % 6])
        res = len(obj_4._UserLanguageCache__telegram_language_cache)  # noqa
        self.assertEqual(res, 46)

    def test_language_cache_5(self):
        obj_5 = UserLanguageCache()
        obj_5._UserLanguageCache__telegram_language_cache.clear()  # noqa
        for i in range(52):
            UserLanguageCache.input_cache_data(i + 1, TestUserLanguageCache.lang[i % 6])
        for i in range(52, 54):
            UserLanguageCache.input_cache_data(i + 1, TestUserLanguageCache.lang[i % 6])
        res = len(obj_5._UserLanguageCache__telegram_language_cache)  # noqa
        self.assertEqual(res, 48)

    def test_language_cache_6(self):
        obj_6 = UserLanguageCache()
        obj_6._UserLanguageCache__telegram_language_cache.clear()  # noqa

        UserLanguageCache.input_cache_data(12345, 'en')
        UserLanguageCache.input_cache_data(54321, 'is')
        UserLanguageCache.input_cache_data(10000, 'es')

        res_1 = UserLanguageCache.get_cache_data(12345)
        res_2 = UserLanguageCache.get_cache_data(54321)
        res_3 = UserLanguageCache.get_cache_data(10000)
        res_4 = UserLanguageCache.get_cache_data(0)
        res_5 = UserLanguageCache.get_cache_data(12346)

        self.assertEqual(res_1, 'en')
        self.assertEqual(res_2, 'is')
        self.assertEqual(res_3, 'es')
        self.assertEqual(res_4, '')
        self.assertEqual(res_5, '')

    def test_language_cache_7(self):
        obj_7 = UserLanguageCache()
        obj_7._UserLanguageCache__telegram_language_cache.clear()  # noqa
        UserLanguageCache.input_cache_data(12345, 'en')
        UserLanguageCache.input_cache_data(54321, 'is')
        UserLanguageCache.input_cache_data(10000, 'es')

        UserLanguageCache.delete_data_from_cache(10000)
        UserLanguageCache.delete_data_from_cache(12345)

        res_1 = UserLanguageCache.get_cache_data(12345)
        res_2 = UserLanguageCache.get_cache_data(54321)
        res_3 = UserLanguageCache.get_cache_data(10000)

        self.assertEqual(res_1, '')
        self.assertEqual(res_2, 'is')
        self.assertEqual(res_3, '')

    # test to check if the relevant and required data is retained in the cache when it is constantly refreshed
    def test_language_cache_8(self):
        obj_8 = UserLanguageCache()
        obj_8._UserLanguageCache__telegram_language_cache.clear()  # noqa
        for i in range(1, 25_000):
            UserLanguageCache.input_cache_data(i * 10, TestUserLanguageCache.lang[i % 6])
            if i % 25 == 0:
                UserLanguageCache.update_data_position(50)
        res_1: str = UserLanguageCache.get_cache_data(50)
        self.assertEqual(res_1, 'kk')
        # and additionally check that the old data has been deleted
        res_2: str = UserLanguageCache.get_cache_data(10)
        self.assertEqual(res_2, '')


class TestUserRegistrationStatusCache(unittest.TestCase):
    def test_user_registration_cache_1(self):
        # getting access to a private attribute of a class
        obj_1 = UserRegistrationStatusCache()
        # clear the cache after the last test
        obj_1._UserRegistrationStatusCache__users.clear()  # noqa
        """
        since the class attribute is not bound to the object, it will have a common state in different objects;
        this is done on purpose - since in this case the cache will be consistent between different modules.

        therefore, for our tests, it should be cleared, because we would try to test its initial state.
        """
        for i in range(1024):
            UserRegistrationStatusCache.input_cache_data(i + 1)
        res = len(obj_1._UserRegistrationStatusCache__users)  # noqa
        self.assertEqual(res, 46)

    def test_user_registration_cache_2(self):
        obj_2 = UserRegistrationStatusCache()
        obj_2._UserRegistrationStatusCache__users.clear()  # noqa
        for i in range(1025):
            UserRegistrationStatusCache.input_cache_data(i + 10)
        res = len(obj_2._UserRegistrationStatusCache__users)  # noqa
        self.assertEqual(res, 47)

    def test_user_registration_cache_3(self):
        obj_3 = UserRegistrationStatusCache()
        obj_3._UserRegistrationStatusCache__users.clear()  # noqa
        for i in range(1027):
            UserRegistrationStatusCache.input_cache_data(i + 15)
        res = len(obj_3._UserRegistrationStatusCache__users)  # noqa
        self.assertEqual(res, 49)

    def test_user_registration_cache_4(self):
        obj_4 = UserRegistrationStatusCache()
        obj_4._UserRegistrationStatusCache__users.clear()  # noqa
        for i in range(50):
            UserRegistrationStatusCache.input_cache_data(i + 15)
        res = len(obj_4._UserRegistrationStatusCache__users)  # noqa
        self.assertEqual(res, 50)

    def test_user_registration_cache_5(self):
        obj_5 = UserRegistrationStatusCache()
        obj_5._UserRegistrationStatusCache__users.clear()  # noqa
        for i in range(51):
            UserRegistrationStatusCache.input_cache_data(i + 999)
        res = len(obj_5._UserRegistrationStatusCache__users)  # noqa
        self.assertEqual(res, 51)

    def test_user_registration_cache_6(self):
        obj_6 = UserRegistrationStatusCache()
        obj_6._UserRegistrationStatusCache__users.clear()  # noqa
        for i in range(52):
            UserRegistrationStatusCache.input_cache_data(i + 123)
        res = len(obj_6._UserRegistrationStatusCache__users)  # noqa
        self.assertEqual(res, 46)

    # test to check if the relevant and required data is retained in the cache when it is constantly refreshed
    def test_user_registration_cache_7(self):
        obj_7 = UserRegistrationStatusCache()
        obj_7._UserRegistrationStatusCache__users.clear()  # noqa
        for i in range(1, 25_000):
            UserRegistrationStatusCache.input_cache_data(i + 10_000)
            if i % 25 == 0:
                UserRegistrationStatusCache.update_data_position(10_005)
        res_1 = UserRegistrationStatusCache.get_cache_data(10_005)
        self.assertEqual(res_1, True)
        # and additionally check that the old data has been deleted
        res_2 = UserRegistrationStatusCache.get_cache_data(10_006)
        self.assertEqual(res_2, False)


if __name__ == '__main__':
    unittest.main()
