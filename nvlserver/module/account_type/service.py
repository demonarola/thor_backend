#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

from sanic.log import logger
from sanic.request import Request

from .specification.get_account_type_specification import (
    get_account_type_list_query, get_account_type_list_count_query, get_account_type_list_dropdown_query
)

__all__ = [
    # SERVICES WORKING ON ACCOUNT TYPE TABLE
    'get_account_type_list', 'get_account_type_list_count', 'get_account_type_dropdown_list'
]


async def get_account_type_list(request: Request, name=None, limit: int = 0, offset: int = 0) -> list:
    """ Get account_type list ordered by account_type id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_account_type_list_query

    try:
        if limit > 0:
            query_str += ' LIMIT $2 OFFSET $3 ORDER BY atc.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY atc.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_account_type_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_account_type_list_count(request: Request, name=None) -> int:
    """ Get city list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_account_type_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
        if row is not None:
            ret_val = row
    except Exception as gclcerr:
        logger.error('get_account_type_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_account_type_dropdown_list(request: Request, name=None) -> list:
    """ Get account_type list ordered by account_type id desc.

    :param request:
    :param name:
    :return:
    """

    ret_val = []

    query_str = get_account_type_list_dropdown_query

    try:
        query_str += ' ORDER BY atc.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_account_type_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val
