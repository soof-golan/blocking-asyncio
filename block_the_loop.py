import asyncio
import time

from helpers import elapsed
from log import logger


async def a_coroutine(task_id: int):
    """Just a placeholder for a real coroutine"""
    start = elapsed()
    logger.info("[task:%d][elapsed:%.3f][a_coroutine] start", task_id, start)
    await asyncio.sleep(0.5)
    end = elapsed()
    logger.info("[task:%d][elapsed:%.3f][a_coroutine][took:%.3f] end", task_id, end, end - start)


def blocking_io(task_id: int):
    """make some blocking I/O thing"""
    start = elapsed()
    logger.info("[task:%d][elapsed:%.3f][blocking_io] start", task_id, start)
    time.sleep(0.5)
    end = elapsed()
    logger.info("[task:%d][elapsed:%.3f][blocking_io][took:%.3f] end", task_id, end, end - start)


async def mixed_async(task_id: int):
    """Demonstrate the accidental synchronous code"""
    start = elapsed()
    logger.info("[task:%d][elapsed:%.3f][mixed_async] start", task_id, start)
    await a_coroutine(task_id)
    blocking_io(task_id)
    end = elapsed()
    logger.info("[task:%d][elapsed:%.3f][mixed_async][took:%.3f] end", task_id, end, end - start)


async def fully_async(task_id: int):
    """Demonstrate the fully asynchronous code"""
    start = elapsed()
    logger.info("[task:%d][elapsed:%.3f][fully_async] start", task_id, start)
    await a_coroutine(task_id)
    await asyncio.to_thread(blocking_io, task_id)
    end = elapsed()
    logger.info("[task:%d][elapsed:%.3f][fully_async][took:%.3f] end", task_id, end, end - start)


async def main(num_tasks: int = 5):
    """Demonstrate the difference between mixed and fully asynchronous code"""
    end_sync, start_sync = await run_mixed(num_tasks)
    end_async, start_async = await run_full_async(num_tasks)

    logger.info("async tasks completed in %.3f seconds", end_async - start_async)
    logger.info("sync tasks completed in %.3f seconds", end_sync - start_sync)
    logger.info("all tasks completed. exiting")


async def run_mixed(num_tasks):
    start_sync = elapsed()
    logger.info("creating %d tasks", num_tasks)
    tasks = [mixed_async(task_id=i) for i in range(num_tasks)]
    logger.info("waiting for tasks to complete")
    await asyncio.gather(*tasks)
    end_sync = elapsed()
    return end_sync, start_sync


async def run_full_async(num_tasks):
    start_async = elapsed()
    async_tasks = [fully_async(task_id=i) for i in range(num_tasks)]
    logger.info("waiting for async tasks to complete")
    await asyncio.gather(*async_tasks)
    end_async = elapsed()
    return end_async, start_async


if __name__ == "__main__":
    asyncio.run(main())
