### file launch_dashboard.py ####
import os
import asyncio
import streamlit.bootstrap
from datetime import datetime
import nest_asyncio

nest_asyncio.apply()


async def do_some_iterations():
    for i in range(10):
        print(datetime.now().time())
        await asyncio.sleep(1)
    print('... Cool!')


async def main():
    task = asyncio.create_task(do_some_iterations())
    task2 = asyncio.create_task(load_dashboard())
    await task
    await task2

async def load_dashboard():
    print('Loading dashboard')
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Final-Stage-Router-Maths-Coding.py')
    args = []
    streamlit.bootstrap.run(filename, '', args, flag_options={})
    print('Loaded.')


if __name__ == "__main__":
    asyncio.run(main())
