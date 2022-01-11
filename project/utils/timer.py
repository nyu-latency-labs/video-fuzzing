import functools
import logging
import time


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        logging.info(f"Started executing module {func.__qualname__}")
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        logging.info(f"Finished executing module {func.__qualname__} in {run_time:.4f} secs")
        return value

    return wrapper_timer
