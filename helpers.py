import time

start = None


def elapsed() -> float:
    global start
    try:
        return time.time() - start
    except TypeError:
        start = time.time()
        return .0
