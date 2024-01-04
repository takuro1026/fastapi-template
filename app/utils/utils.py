import time
from functools import wraps

from app.utils.logger import logger


def time_fn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        logger.info(f"@time_fn: {fn.__name__} took {t2 - t1} seconds")
        return result

    return measure_time

def async_time_fn(fn):
    @wraps(fn)
    async def measure_time(*args, **kwargs):
        t1 = time.time()
        result = await fn(*args, **kwargs)
        t2 = time.time()
        logger.info(f"@time_fn: {fn.__name__} took {t2 - t1} seconds")
        return result

    return measure_time