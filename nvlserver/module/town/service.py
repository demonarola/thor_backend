#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_town_specification import (
    get_town_list_query, get_town_list_count_query, get_town_element_query
)

from .specification.create_town_specification import create_town_element_query
from .specification.update_town_specification import update_town_element_query
from .specification.delete_town_specification import delete_town_element_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_town_list', 'get_town_list_count',
    'get_town_element', 'create_town_element', 'update_town_element', 'delete_town_element'
]


async def get_town_list(
        request: Request,
        name=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get country list ordered by country id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_town_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY twn.id DESC LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY twn.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_town_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_town_list_count(
        request: Request,
        name=None) -> int:
    """ Get city list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_town_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_town_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_town_element(
        request: Request,
        town_id: int = 0) -> dict:
    """ Get town element

    :param request:
    :param town_id:
    :return:
    """

    ret_val = {}
    query_str = get_town_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, town_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_town_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_town_element(
        request: Request,
        name: str = '',
        country_id: int = 0,
        active: bool = True) -> dict:
    """ Create town element

    :param request:
    :param name:
    :param country_id:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_town_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, country_id, name, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('create_town_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_town_element(
        request: Request,
        lift_id: int = 0,
        name: str = '',
        country_id: int = 0,
        active: bool = True) -> dict:
    """ Update town element

    :param request:
    :param lift_id:
    :param name:
    :param country_id:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_town_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, lift_id, country_id, name, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('update_town_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_town_element(
        request: Request,
        lift_id: int = 0) -> dict:
    """ Delete town element

    :param request:
    :param lift_id:
    :return:
    """

    ret_val = {}
    query_str = delete_town_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, lift_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_town_element service erred with: {}'.format(cleerr))

    return ret_val
