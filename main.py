import asyncio
import time
from typing import Awaitable, Literal

from helpers import elapsed
from log import logger


def blocking_io(task_id: int):
    """make some blocking I/O thing"""
    logger.info("[task:%d][elapsed:%.3f] starting blocking_io", task_id, elapsed())
    with open("/dev/urandom", "rb") as f:
        f.read(1000000000)
    logger.info("[task:%d][elapsed:%.3f] ending blocking_io", task_id, elapsed())


async def some_coroutine(task_id: int):
    """Just a placeholder for a real coroutine"""
    logger.info("[task:%d][elapsed:%.3f] starting coroutine", task_id, elapsed())
    await asyncio.sleep(1)
    logger.info("[task:%d][elapsed:%.3f] ending coroutine", task_id, elapsed())


async def accidental_mixed_sync_and_async(task_id: int):
    """Demonstrate the accidental synchronous code"""
    logger.info("[task:%d][elapsed:%.3f] starting accidental_sync_async", task_id, elapsed())
    await some_coroutine(task_id)
    blocking_io(task_id)
    logger.info("[task:%d][elapsed:%.3f] ending accidental_sync_async", task_id, elapsed())


def make_tasks(n: int, mode: Literal["async"] | Literal["accidental"]) -> list[Awaitable[None]]:
    """Create n tasks"""
    logger.info("creating %d tasks", n)
    if mode == "async":
        return [some_coroutine(task_id=i) for i in range(n)]
    elif mode == "accidental":
        return [accidental_mixed_sync_and_async(task_id=i) for i in range(n)]
    else:
        msg = f"unknown mode {mode}"
        raise ValueError(msg)


async def main():
    logger.info("scheduling tasks")
    # tasks = make_tasks(5, mode="async")
    tasks = make_tasks(5, mode="accidental")

    logger.info("waiting for tasks to complete")
    await asyncio.gather(*tasks)

    logger.info("exiting main")


if __name__ == "__main__":
    asyncio.run(main())
