#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '0.1.0'


import uvloop
import asyncio
from copy import deepcopy
from asyncpg import create_pool

from web_backend.config import DEBUG, DEFAULT_LOOP_TIMEOUT
from web_backend.config import DATABASE as DATABASE_CONFIG
from web_backend.backend_services.nvl_tracker_service.expire_old_command_specification import (
    update_expired_commands_state_query
)


db_conf = deepcopy(DATABASE_CONFIG)
conn_uri = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
    'postgres',
    db_conf['user'], db_conf['password'], db_conf['host'],
    db_conf['port'], db_conf['database'])
pool = None


async def configure_pool():
    global pool
    pool = await create_pool(conn_uri, min_size=2, max_size=5)


async def detect_end_expire_commands() -> bool:
    ret_val = True
    while True:
        async with pool.acquire() as connection:
            try:
                await connection.fetch(update_expired_commands_state_query)
            except Exception as ftc_exc:
                if DEBUG:
                    print('Exception on fetch row: {}'.format(ftc_exc))
                    print(dir(connection))
                    ret_val = False
                    if ret_val is False:
                        break

            await asyncio.sleep(DEFAULT_LOOP_TIMEOUT)

    return ret_val


async def runner():
    global pool
    if pool is None:
        await configure_pool()
        await detect_end_expire_commands()
    else:
        await detect_end_expire_commands()


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(runner())
