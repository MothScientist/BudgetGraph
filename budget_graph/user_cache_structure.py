"""
This module is designed to save us from unnecessary queries to the database,
since it will store information about the current user authorization status and the language used.

It is assumed that dictionaries will be stored for the last 50-100 users who performed actions.

If the user deletes the account or changes the language, the trigger will be called and the cache value will change.

Caching is based on the LRU algorithm:

New dictionary keys are always placed "at the end",
so to clear out the old values we will remove the "at the beginning" values.

To update the value: remove it from the current position and insert “at the end”.

Starting from version 3.7, the keys in the dictionary maintain order, so we will use a key-value implementation.
"""

from budget_graph.logger import setup_logger
from budget_graph.encryption import logging_hash

logger_cache = setup_logger("logs/CacheLog.log", "cache_logger")


class UserLanguageCache:
    """ This class caches the user's language value """
    __telegram_language_cache: dict = {}
    __maximum_dict_size: int = 50

    @staticmethod
    def get_cache_data(telegram_id: int) -> str:
        """ Getting a value from the dictionary, if it is not there, then we give a negative answer """
        if telegram_id in UserLanguageCache.__telegram_language_cache:
            UserLanguageCache.update_data_position(telegram_id)
            logger_cache.info(f"<Language> Data from cache (SUCCESS): telegram_id={logging_hash(telegram_id)}")
            return UserLanguageCache.__telegram_language_cache[telegram_id]
        logger_cache.info(f"<Language> There is no data in the cache: telegram_id={logging_hash(telegram_id)}")
        return ''

    @staticmethod
    def input_cache_data(telegram_id: int, user_language: str) -> None:
        """ Adding a new key to the dictionary """
        _len_dict: int = len(UserLanguageCache.__telegram_language_cache)
        if _len_dict > UserLanguageCache.__maximum_dict_size:
            # If the dictionary is full, then we clear 10% of its space, removing the "oldest" values.
            i: int = 0  # counter to avoid calculating dictionary keys at each iteration
            _dict_keys: tuple = tuple(UserLanguageCache.__telegram_language_cache.keys())
            # Adjusting the hysteresis width to clear the dictionary
            _limit: int = UserLanguageCache.__maximum_dict_size - (UserLanguageCache.__maximum_dict_size // 10)  # 10%
            while _len_dict > _limit:
                UserLanguageCache.__telegram_language_cache.pop(_dict_keys[i])
                i += 1
                _len_dict -= 1
            logger_cache.info(f"<Language> Removed {i} keys from cache")
        UserLanguageCache.__telegram_language_cache[telegram_id] = user_language
        logger_cache.info(f"<Language> New cache entry: telegram_id={logging_hash(telegram_id)}")

    @staticmethod
    def update_data_position(telegram_id: int) -> None:
        """ Move the key to the "end" of the dictionary """
        _data = UserLanguageCache.__telegram_language_cache.pop(telegram_id)
        UserLanguageCache.__telegram_language_cache[telegram_id] = _data
        logger_cache.info(f"<Language> New cache priority set: telegram_id={logging_hash(telegram_id)}")

    @staticmethod
    def delete_data_from_cache(telegram_id: int) -> None:
        """ Removing a key from the cache """
        if telegram_id in UserLanguageCache.__telegram_language_cache:
            UserLanguageCache.__telegram_language_cache.pop(telegram_id)
            logger_cache.info(f"<Language> [OK] Data removed from cache (trigger): "
                              f"telegram_id={logging_hash(telegram_id)}")
        else:
            logger_cache.info(f"<Language> [No data] (trigger): telegram_id={logging_hash(telegram_id)}")


"""
When deleting a group or user, a bulk cache deletion is not triggered, 
since there is no system at all for deleting data from the table that stores user languages.
"""


class UserRegistrationStatusCache:
    """
    This class contains a list of telegram_ids whose status has been confirmed as registered.
    The principle of operation is similar to the user language caching class, but only based on a list.

    “Old data” will be at the beginning of the list, and current data at the very end.
    """
    __users: list = []
    __maximum_list_size: int = 50

    @staticmethod
    def get_cache_data(telegram_id: int) -> bool:
        if telegram_id in UserRegistrationStatusCache.__users:
            UserRegistrationStatusCache.update_data_position(telegram_id)
            logger_cache.info(f"<RegistrationStatus> Data from cache (SUCCESS): "
                              f"telegram_id={logging_hash(telegram_id)}")
            return True
        logger_cache.info(f"<RegistrationStatus> There is no data in the cache: "
                          f"telegram_id={logging_hash(telegram_id)}")
        return False  # either the user is not in the cache or he is not registered

    @staticmethod
    def input_cache_data(telegram_id: int) -> None:
        _len_list: int = len(UserRegistrationStatusCache.__users)
        # if the list is full
        if _len_list > UserRegistrationStatusCache.__maximum_list_size:
            _del_limit: int = UserRegistrationStatusCache.__maximum_list_size // 10  # 10%
            del UserRegistrationStatusCache.__users[0:_del_limit]
            logger_cache.info(f"<RegistrationStatus> Removed {_del_limit} keys from cache")

        # checking that the user is not yet in the cache
        if telegram_id not in UserRegistrationStatusCache.__users:
            UserRegistrationStatusCache.__users.append(telegram_id)
            logger_cache.info(f"<RegistrationStatus> New cache entry: telegram_id={logging_hash(telegram_id)}")
        else:
            logger_cache.warning(f"<RegistrationStatus> Trying to add data that is already in the cache: "
                                 f"telegram_id={logging_hash(telegram_id)}")

    @staticmethod
    def update_data_position(telegram_id: int) -> None:
        UserRegistrationStatusCache.__users.remove(telegram_id)  # delete from current position
        UserRegistrationStatusCache.__users.append(telegram_id)  # put it at the “beginning” of the cache list
        logger_cache.info(f"<RegistrationStatus> New cache priority set: telegram_id={logging_hash(telegram_id)}")

    @staticmethod
    def delete_data_from_cache(telegram_id: int) -> None:
        if telegram_id in UserRegistrationStatusCache.__users:
            UserRegistrationStatusCache.__users.remove(telegram_id)
            logger_cache.info(f"<RegistrationStatus> [OK] Data removed from cache (trigger): "
                              f"telegram_id={logging_hash(telegram_id)}")
        else:
            logger_cache.info(f"<RegistrationStatus> [No data] (trigger): telegram_id={logging_hash(telegram_id)}")

    @staticmethod
    def delete_group_trigger(telegram_ids: tuple) -> None:
        """ The function is called when an entire group is deleted to avoid cache read errors """
        for telegram_id in telegram_ids:
            UserRegistrationStatusCache.delete_data_from_cache(telegram_id)
        logger_cache.info(f"<RegistrationStatus> Trigger - SUCCESS. "
                          f"Number of items removed from cache: {len(telegram_ids)}")
