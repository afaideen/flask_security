import asyncio
import time


async def task1():
    while True:
        print("%d:Hello say_boo" %(time.time()))
        # sleep for a moment
        # time.sleep(0.5)
        await asyncio.sleep(1)


async def task2():
    while True:
        print("%d:Hello say_baa" %(time.time()))
        # sleep for a moment
        # time.sleep(2)
        await asyncio.sleep(5)



async def main():
    await asyncio.gather(task1(), task2())


asyncio.run(main())
