#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
import datetime
from sanic.log import logger
from sanic.request import Request

from .specification.get_console_specification import (
    get_console_list_query, get_console_list_count_query, get_console_element_query
)

from .specification.create_console_specification import create_console_element_query
from .specification.update_console_specification import update_console_element_query
from .specification.delete_console_specification import delete_console_element_query

__all__ = [
    # SERVICES WORKING ON CONSOLE TABLE
    'get_console_list', 'get_console_list_count', 'get_console_element',
    'create_console_element', 'update_console_element', 'delete_console_element'
]


async def get_console_list(request: Request, limit: int = 0, offset: int = 0) -> list:
    """ Get console list ordered by console id desc.

    :param request:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_console_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY cls.id DESC LIMIT $1 OFFSET $2;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, limit, offset)
        else:
            query_str += ' ORDER BY cls.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_console_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_console_list_count(request: Request) -> int:
    """ Get console list count.

    :param request:
    :return:
    """

    ret_val = 0
    query_str = get_console_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_console_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_console_element(request: Request, console_id: int = 0) -> dict:
    """ Get console element

    :param request:
    :param console_id:
    :return:
    """

    ret_val = {}
    query_str = get_console_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, console_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_console_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_console_element(
        request: Request, timestamp: object = datetime.datetime.now(),
        user_id: int = 0, message: str = '', active: bool = True) -> dict:
    """ Create console element
    
    :param request: 
    :param timestamp: 
    :param user_id: 
    :param message: 
    :param active: 
    :return: 
    """

    ret_val = {}
    query_str = create_console_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, timestamp, user_id, message, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_console_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('create_console_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_console_element(
        request: Request, console_id: int = 0, timestamp: object = datetime.datetime.now(),
        user_id: object = None, message: str = '', active: bool = True) -> dict:
    """ Update console element

    :param request:
    :param console_id:
    :param timestamp:
    :param user_id:
    :param message:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_console_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, console_id, timestamp, user_id, message, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_console_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_console_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_console_element(request: Request, console_id: int = 0) -> dict:
    """ Delete console element

    :param request:
    :param console_id:
    :return:
    """

    ret_val = {}
    query_str = delete_console_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, console_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_console_element service erred with: {}'.format(cleerr))

    return ret_val
