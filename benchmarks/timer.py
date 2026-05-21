import time
import functools
from typing import Callable, Any


def timed(fn: Callable) -> Callable:
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"{fn.__name__} ran in {elapsed_ms:.2f} ms")
        return result
    return wrapper


def benchmark(fn: Callable, *args, repeats: int = 5, **kwargs) -> dict:
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn(*args, **kwargs)
        times.append(time.perf_counter() - start)
    return {
        "mean_ms": (sum(times) / len(times)) * 1000,
        "min_ms": min(times) * 1000,
        "max_ms": max(times) * 1000,
        "repeats": repeats,
    }
