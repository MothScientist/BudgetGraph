from log_settings import setup_logger
import time
from functools import wraps

logger_time = setup_logger("logs/TimeLog.log", "time_logger")


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _start = time.perf_counter()
        result = func(*args, **kwargs)
        _end = time.perf_counter()
        logger_time.info(f'{func.__name__}: {_end - _start:.6f} sec.')
        return result

    return wrapper
