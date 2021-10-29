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


def status():
    """Print the runtime of the decorated function"""
    def decorator_status(func):
        @functools.wraps(func)
        def wrapper_status(*args, **kwargs):
            logging.info(f"In module {func.__qualname__}")
            value = func(*args, **kwargs)
            logging.info(f"Finished module {func.__qualname__}")
            return value
        return wrapper_status
    return decorator_status
