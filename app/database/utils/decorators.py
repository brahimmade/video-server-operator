import threading

INSERTION_LOCK = threading.RLock()


def with_insertion_lock(func):
    def wrapper(*args, **kwargs):
        with INSERTION_LOCK:
            return func(*args, **kwargs)

    return wrapper
