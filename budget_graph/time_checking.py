import sys
from time import perf_counter
from functools import wraps
sys.path.append('../')
from budget_graph.logger import setup_logger

logger_time = setup_logger("logs/TimeLog.log", "time_logger")


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _start = perf_counter()
        result = func(*args, **kwargs)
        _end = perf_counter()
        logger_time.info(f'{func.__name__}: {_end - _start:.6f} s.')
        return result
    return wrapper
