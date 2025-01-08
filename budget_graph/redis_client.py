"""
Client for working with the Redis database
"""

from os import getenv
from dotenv import load_dotenv
from redis import Redis, ConnectionPool, ConnectionError, TimeoutError


load_dotenv('redis.env')  # Load environment variables from redis.env file
redis_psw: str = getenv('REDIS_PSW')
redis_db: int = int(getenv('REDIS_DB'))
redis_host: str = getenv('REDIS_HOST')
redis_port: int = int(getenv('REDIS_PORT'))


class PyRedis:
    def __init__(self, host, port, psw, db=0, socket_timeout=None):
        self.redis = Redis(
            connection_pool=ConnectionPool(
                host=host,
                port=port,
                db=db,
                password=psw,
                socket_timeout=socket_timeout
            )
        )

    def ping(self) -> bool:
        try:
            return self.redis.ping()
        except (ConnectionError, TimeoutError):
            return False

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
            time_ms = PyRedis.compare_and_select_seconds_and_milliseconds(time_s, time_ms)
            time_s = None

        self.redis.set(key, value, nx=if_not_exist, xx=if_exist, ex=time_s, px=time_ms)

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

    @staticmethod
    def compare_and_select_seconds_and_milliseconds(time_s: float, time_ms: float) -> float:
        """
        If both seconds and milliseconds are specified,
        the time is converted to milliseconds and the smallest one is selected
        """
        return min(time_s * 1_000, time_ms)


r = PyRedis(redis_host, redis_port, redis_psw, db=redis_db, socket_timeout=.001)
print(r.ping())
