import functools
import logging
import time


def timer(name=""):
    """Print the runtime of the decorated function"""
    def decorator_timer(func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()    # 1
            value = func(*args, **kwargs)
            end_time = time.perf_counter()      # 2
            run_time = end_time - start_time    # 3
            logging.info(f"Finished {name} in {run_time:.4f} secs")
            return value
        return wrapper_timer
    return decorator_timer
