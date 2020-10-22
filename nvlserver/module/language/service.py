#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from sanic.log import logger
from sanic.request import Request

from .specification.get_language_specification import (
    get_language_list_query, get_language_list_count_query,
    get_language_element_query, get_language_count_by_name_query,
    get_language_element_by_name_query, get_language_element_by_short_code_query,
    get_language_list_dropdown_query
)

from .specification.delete_language_specification import delete_language_element_query
from .specification.create_language_specification import create_language_element_query
from .specification.update_language_specification import update_language_element_query


__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'create_language_element', 'get_language_list', 'get_language_list_count',
    'get_language_element', 'get_language_element_by_name', 'get_language_element_by_short_code',
    'update_language_element', 'delete_language_element', 'check_if_language_name_is_free',
    'get_language_dropdown_list'
]


# CREATE CUSTOMER SERVICE
async def create_language_element(
        request: Request,
        name=None,
        short_code=None,
        default_language=False,
        active=True) -> dict:
    """ Create language element.

    :param request:
    :param name:
    :param short_code:
    :param default_language:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_language_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name, short_code, default_language, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('create_language_element service erred with: {}'.format(cleerr))

    return ret_val


# GET LANGUAGE LIST
async def get_language_list(
        request: Request,
        name=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get language list ordered by language id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_language_list_query

    try:
        if limit > 0:
            query_str += ' LIMIT $2 OFFSET $3 ORDER BY lng.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY lng.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gllerr:
        logger.error('get_language_list service erred with: {}'.format(gllerr))

    return ret_val


async def get_language_list_count(
        request: Request,
        name=None) -> int:
    """ Get language list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_language_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
            if row is not None:
                ret_val = row
    except Exception as gllcerr:
        logger.error('get_language_list_count service erred with: {}'.format(gllcerr))

    return ret_val


async def get_language_element(
        request: Request,
        language_id: int = 0) -> dict:
    """ Get language element by language id.

    :param request:
    :param language_id:
    :return:
    """

    ret_val = {}
    query_str = get_language_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, language_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gleerr:
        logger.error('get_language_element service erred with: {}'.format(gleerr))

    return ret_val


async def get_language_element_by_name(
        request: Request,
        name: str = '') -> dict:
    """ Get language element by language name.

    :param request:
    :param name:
    :return:
    """

    ret_val = {}
    query_str = get_language_element_by_name_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
            if row is not None:
                ret_val = dict(row)
    except Exception as gleerr:
        logger.error('get_language_element_by_name service erred with: {}'.format(gleerr))

    return ret_val


async def get_language_element_by_short_code(
        request: Request,
        short_code: str = '') -> dict:
    """ Get language element by short_code.

    :param request:
    :param short_code:
    :return:
    """

    ret_val = {}
    query_str = get_language_element_by_short_code_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, short_code)
            if row is not None:
                ret_val = dict(row)
    except Exception as gleerr:
        logger.error('get_language_element_by_short_code service erred with: {}'.format(gleerr))

    return ret_val


# UPDATE CUSTOMER SERVICE
async def update_language_element(
        request: Request,
        language_id: int = 0,
        name=None,
        short_code=None,
        default_language=False,
        active=True) -> dict:
    """ Update language element

    :param request:
    :param language_id:
    :param name:
    :param short_code:
    :param default_language:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_language_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, language_id, name, short_code, default_language, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as uleerr:
        logger.error('update_language_elements service erred with: {}'.format(uleerr))

    return ret_val


# DELETE CUSTOMER SERVICE
async def delete_language_element(
        request: Request,
        language_id: int = 0) -> dict:
    """ Delete language element by language id.

    :param request:
    :param language_id:
    :return:
    """

    ret_val = {}
    query_str = delete_language_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, language_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as dleerr:
        logger.error('delete_language_element service erred with: {}'.format(dleerr))

    return ret_val


# CHECK IF LANGUAGE NAME IS FREE TO USE
async def check_if_language_name_is_free(
        request: Request,
        name=None,
        language_id=None) -> bool:
    """ Delete language element by language id.

    :param request:
    :param name:
    :param language_id:
    :return:
    """

    ret_val = False
    query_str = get_language_count_by_name_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name, language_id)
            if row is not None:
                if row == 0:
                    ret_val = True
    except Exception as cilniserr:
        logger.error('check_if_language_name_is_free service erred with: {}'.format(cilniserr))

    return ret_val


async def get_language_dropdown_list(
        request: Request,
        name=None) -> list:
    """ Get timezone list ordered by country id desc.

    :param request:
    :param name:
    :return:
    """

    ret_val = []

    query_str = get_language_list_dropdown_query

    try:
        query_str += ' ORDER BY lng.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_language_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val
