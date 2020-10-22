#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_country_specification import (
    get_country_list_query, get_country_list_count_query
    #  , get_country_element_query
)


async def get_country_list(request: Request, name=None, limit: int = 0, offset: int = 0) -> list:
    """ Get country list ordered by country id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_country_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY cnt.id DESC LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY cnt.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_country_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_country_list_count(request: Request, name=None) -> int:
    """ Get city list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_country_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
        if row is not None:
            ret_val = row
    except Exception as gclcerr:
        logger.error('get_country_list_count service erred with: {}'.format(gclcerr))

    return ret_val
