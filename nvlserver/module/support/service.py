#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_support_specification import (
    get_support_list_query, get_support_list_count_query, get_support_element_query
)

from .specification.create_support_specification import create_support_element_query
from .specification.update_support_specification import update_support_element_query
from .specification.delete_support_specification import delete_support_element_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_support_list', 'get_support_list_count',
    'get_support_element', 'create_support_element', 'update_support_element',
    'delete_support_element'
]


async def get_support_list(
        request: Request,
        email=None,
        limit: int = 1,
        offset: int = 0) -> list:
    """ Get country list ordered by country id desc.

    :param request:
    :param email:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_support_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY supp.id DESC LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:

                rows = await connection.fetch(query_str, email, limit, offset)
        else:
            query_str += ' ORDER BY supp.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, email)

        if rows is not None:
            ret_list = []
            temp_list = [dict(x) for x in rows]
            for x in temp_list:
                x['created_on'] = x['created_on'].isoformat() if x['created_on'] is not None else ''
                x['updated_on'] = x['updated_on'].isoformat() if x['updated_on'] is not None else ''
                ret_list.append(x)
            ret_val = ret_list

    except Exception as gclerr:
        logger.error('get_support_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_support_list_count(
        request: Request,
        email=None) -> int:
    """ Get city list count.

    :param request:
    :param email:
    :return:
    """

    ret_val = 0
    query_str = get_support_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, email)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_support_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_support_element(
        request: Request,
        support_id: int = 0) -> dict:
    """ Get support element

    :param request:
    :param support_id:
    :return:
    """

    ret_val = {}
    query_str = get_support_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, support_id)
            if row is not None:
                x = dict(row)
                x['created_on'] = x['created_on'].isoformat() if x['created_on'] is not None else ''
                x['updated_on'] = x['updated_on'].isoformat() if x['updated_on'] is not None else ''
                ret_val = x
    except Exception as cleerr:
        logger.error('get_support_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_support_element(
        request: Request,
        email: str = '',
        user_id: object = None,
        subject: str = '',
        file_uuid: str = '',
        file_name: str = '',
        message: str = '',
        active: bool = True) -> dict:
    """ Create support element

    :param request:
    :param email:
    :param user_id:
    :param subject:
    :param file_name:
    :param file_uuid:
    :param message:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_support_element_query
    try:

        async with request.app.pg.acquire() as connection:

            row = await connection.fetchrow(
                query_str, email, user_id, subject, file_uuid, file_name,
                message, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_support_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('create_support_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_support_element(
        request: Request,
        support_id: int = 0,
        email: str = '',
        user_id: object = None,
        subject: str = '',
        file_uuid: str = '',
        file_name: str = '',
        message: str = '',
        active: bool = True) -> dict:
    """ Create support element

    :param request:
    :param support_id:
    :param email:
    :param user_id:
    :param subject:
    :param file_name:
    :param file_uuid:
    :param message:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_support_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, support_id, email, user_id, subject, file_uuid, file_name,
                message, active)
            if row is not None:
                saved_row = dict(row)
                dta = await get_support_element(request, saved_row.get('id'))
                if dta:
                    ret_val = dta
    except Exception as cleerr:
        logger.error('update_support_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_support_element(
        request: Request,
        support_id: int = 0) -> dict:
    """ Delete support element

    :param request:
    :param support_id:
    :return:
    """

    ret_val = {}
    query_str = delete_support_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, support_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_support_element service erred with: {}'.format(cleerr))

    return ret_val
