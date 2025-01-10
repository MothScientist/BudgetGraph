from sys import path
from time import perf_counter
from functools import wraps
path.append('../')
from budget_graph.logger import setup_logger
from budget_graph.global_config import GlobalConfig

logger_time = setup_logger("logs/TimeLog.log", "time_logger")


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not GlobalConfig.timeit_enable:
            return func(*args, **kwargs)

        _start = perf_counter()
        result = func(*args, **kwargs)
        _end = perf_counter()
        logger_time.info(f'{func.__name__}: {_end - _start:.6f} s.')
        return result

    return wrapper
