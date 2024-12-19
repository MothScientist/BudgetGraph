"""
A module that manages the storage and processing of cache via Redis.
Works if a container with Redis has been deployed and is available, otherwise the user_cache_structure.py module is used
"""

from os import getenv
from dotenv import load_dotenv
from redis import Redis, ConnectionPool, ConnectionError, TimeoutError


def check_redis_server_is_available(host, port, psw, db=0, socket_timeout=0.001) -> bool:
    """
    The ping method checks the availability of the Redis server
    """
    try:
        return Redis(
            connection_pool=ConnectionPool(
                host=host,
                password=psw,
                port=port,
                db=db,
                socket_timeout=socket_timeout
            )
        ).ping()
    except (ConnectionError, TimeoutError):
        return False


class PyRedis:
    """
    The main class for working with the Redis database
    """
    def __init__(self, host, port, psw, db=0, socket_timeout=None):
        self.redis = Redis(
            connection_pool=ConnectionPool(
                host=host,
                password=psw,
                port=port,
                db=db,
                socket_timeout=socket_timeout
            )
        )

    def set(
            self,
            key: str,
            value,
            time_ms=None,
            time_s=None,
            if_exist: bool = None,
            if_not_exist: bool = None
    ) -> None:
        """
        Set a new key or override an existing one
        If both parameters (time_s, time_ms) are specified, the key will be deleted based on the smallest value.
        :param key:
        :param value:
        :param time_ms:
        :param time_s:
        :param if_exist:
        :param if_not_exist:
        :return: None
        """
        if time_s and time_ms:
            res_time = time_ms * 1_000 if time_s > time_ms * 1_000 else time_s
        else:
            res_time = (time_s or ((time_ms or 0) * 1_000)) or None

        self.redis.set(key, value, nx=if_not_exist, xx=if_exist, ex=res_time)

    def get(self, key, default_value=None):
        res = self.redis.get(key)
        return res if res else default_value

    def delete(self, key, returning: bool = False):
        """
        Delete a key
        :param key:
        :param returning: Should I return the value that the key had before deletion?
        :return: value or None
        """
        res = self.redis.get(key) if returning else None
        self.redis.delete(key)
        return res


load_dotenv()  # Load environment variables from .env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))

#r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db)
print(check_redis_server_is_available(redis_host, redis_port, redis_psw, db=redis_db))
