#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_notification_type_specification import get_notification_type_list_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_notification_type_list'
]


async def get_notification_type_list(
        request: Request) -> list:
    """ Get notification list ordered by notification id desc.

    :param request:
    :return:
    """
    ret_val = []

    query_str = get_notification_type_list_query

    try:
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_notification_list service erred with: {}'.format(gclerr))

    return ret_val
