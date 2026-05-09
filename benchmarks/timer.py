import time
from functools import wraps


def timed(fn):
    """
    Decorator that measures execution time of a function.
    Prints elapsed time in milliseconds.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = fn(*args, **kwargs)

        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        print(f"{fn.__name__} took {elapsed_ms:.3f} ms")

        return result

    return wrapper


def benchmark(fn, *args, repeats=5, **kwargs) -> float:
    """
    Run a function multiple times and return average execution time in milliseconds.

    Parameters
    ----------
    fn : callable
        Function to benchmark
    repeats : int
        Number of repetitions

    Returns
    -------
    float
        Mean execution time in milliseconds
    """

    times = []

    for _ in range(repeats):
        start = time.perf_counter()

        fn(*args, **kwargs)

        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        times.append(elapsed_ms)

    mean_time = sum(times) / len(times)

    return mean_time