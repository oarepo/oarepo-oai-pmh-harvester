import functools
import threading
import time

threadLocal = threading.local()


class TIM:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        self.level = getattr(threadLocal, "level", "")
        threadLocal.level = self.level + "  "

    def __exit__(self, type, value, traceback):
        stop = time.time()
        threadLocal.level = self.level
        print("%s%s: %s ms" % (self.level, self.name, (stop - self.start) * 1000))


def timeit(f):
    if callable(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            with TIM(f.__name__):
                return f(*args, **kwargs)

        return wrapper

    # otherwise it is a context manager
    return TIM(f)
