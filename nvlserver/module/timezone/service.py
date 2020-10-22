#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_timezone_specification import (
    get_timezone_list_query, get_timezone_list_count_query,
    get_timezone_list_dropdown_query, get_timezone_element_query,
    get_timezone_element_by_name_query
)

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_timezone_list', 'get_timezone_list_count',
    'get_timezone_dropdown_list', 'get_timezone_element', 'get_timezone_element_by_name'
]


# GET CUSTOMER SERVICES
async def get_timezone_list(request: Request, name=None, limit: int = 0, offset: int = 0) -> list:
    """ Get timezone list ordered by country id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_timezone_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY tmz.id DESC LIMIT $2 OFFSET $3 ;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY tmz.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_timezone_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_timezone_list_count(request: Request, name=None) -> int:
    """ Get timezone list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_timezone_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
        if row is not None:
            ret_val = row
    except Exception as gclcerr:
        logger.error('get_timezone_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_timezone_dropdown_list(request: Request, name=None) -> list:
    """ Get timezone list.

    :param request:
    :param name:
    :return:
    """

    ret_val = []

    query_str = get_timezone_list_dropdown_query

    try:
        query_str += ' ORDER BY tmz.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_timezone_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_timezone_element(request: Request, timezone_id: int = 0) -> dict:
    """ Get timezone element by timezone id desc.

    :param request:
    :param timezone_id:
    :return:
    """

    ret_val = {}

    query_str = get_timezone_element_query

    try:
        query_str += ' ORDER BY tmz.id DESC;'
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, timezone_id)

            if row is not None:
                ret_val = dict(row)

    except Exception as gclerr:
        logger.error('get_timezone_element service erred with: {}'.format(gclerr))

    return ret_val


async def get_timezone_element_by_name(request: Request, name: str = 'Europe/Zagreb') -> dict:
    """ Get timezone element by name.

    :param request:
    :param name:
    :return:
    """

    ret_val = {}

    query_str = get_timezone_element_by_name_query

    try:
        query_str += ' ORDER BY tmz.id DESC LIMIT 1;'
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, name)

            if row is not None:
                ret_val = dict(row)

    except Exception as gclerr:
        logger.error('get_timezone_element_by_name service erred with: {}'.format(gclerr))

    return ret_val
