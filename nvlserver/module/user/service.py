#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic.log import logger
from sanic.request import Request
from .specification.get_user_specification import (
    user_login_by_email_query, user_data_by_id_query, get_user_list_count_query,
    get_user_element_query, get_user_list_query, get_user_list_by_fullname_query
)
from .specification.delete_user_specification import delete_user_element_query
from .specification.update_user_specification import (
    update_user_element_query, update_user_element_language_query,
    update_user_element_map_pool_time_query, update_user_element_timezone_query
)
from .specification.create_user_specification import create_user_element_query

from web_backend.nvlserver.module.permission.service import (
    update_user_permission_list, delete_user_permission_list_by_user_id
)
from web_backend.nvlserver.module.timezone.service import get_timezone_element

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_user_login_by_email', 'get_user_by_id',
    'get_user_list', 'get_user_list_count',
    'get_user_list_by_fullname', 'get_user_element',
    'create_user_element', 'update_user_element',
    'update_user_element_timezone', 'update_user_element_map_pool_time',
    'update_user_element_language', 'delete_user_element'
]


async def get_user_login_by_email(
        request, email: str) -> object:
    """

    :param request:
    :param email:
    :return:
    """
    ret_val = None
    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(user_login_by_email_query, email)
            if row is not None:
                ret_val = dict(row)

    except Exception as guid_err:
        logger.error('user.get_user_login_by_email erred with {}'.format(guid_err))

    return ret_val


async def get_user_by_id(
        request,
        user_id: int) -> dict:
    """

    :param request:
    :param user_id:
    :return:
    """
    ret_val = {}

    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(user_data_by_id_query, user_id)
            if row is not None:
                ret_val = dict(row)

    except Exception as guid_err:
        logger.error('user.get_user_by_id erred with {}'.format(guid_err))

    return ret_val


async def get_user_list(
        request: Request,
        email=None,
        fullname=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get user list ordered by user id desc.

    :param request:
    :param email:
    :param fullname:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_user_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY usr.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, email, fullname, limit, offset)
        else:
            query_str += ' ORDER BY usr.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, email, fullname)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_user_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_user_list_count(
        request: Request,
        email=None,
        fullname=None) -> int:
    """ Get user list count.

    :param request:
    :param email:
    :param fullname:
    :return:
    """

    ret_val = 0
    query_str = get_user_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, email, fullname)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_user_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_user_list_by_fullname(
        request: Request,
        fullname=None) -> list:
    """ Get user list by fullname

    :param request:
    :param fullname:
    :return:
    """
    ret_val = []

    query_str = get_user_list_by_fullname_query

    try:
        query_str += ' ORDER BY usr.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, fullname)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_user_list_by_fullname service erred with: {}'.format(gclerr))

    return ret_val


async def get_user_element(
        request: Request,
        user_id: int = 0) -> dict:
    """ Get user element by user id.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_user_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id)
            if row is not None:
                ret_val = dict(row)

    except Exception as gccerr:
        logger.error('get_user_element service erred with: {}'.format(gccerr))

    return ret_val


# CREATE CUSTOMER SERVICE
async def create_user_element(
        request: Request,
        email: str = '',
        password: str = '',
        fullname: str = '',
        locked: bool = False,
        language_id: int = 0,
        timezone: int = 0,
        map_pool_time: int = 900,
        account_type_id: int = 0,
        active: bool = True) -> dict:
    """

    :param request:
    :param email:
    :param password:
    :param fullname:
    :param language_id:
    :param timezone:
    :param map_pool_time:
    :param account_type_id:
    :param locked:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_user_element_query
    try:
        async with request.app.pg.acquire() as connection:
            timezone_element = await get_timezone_element(request, timezone_id=timezone)

            row = await connection.fetchrow(
                query_str, email, password, fullname,
                locked, language_id, ujson.dumps(
                    {
                        'timezone_id': timezone_element.get('id'),
                        'timezone_name': timezone_element.get('name'),
                        'map_pool_time': map_pool_time
                    }
                ),
                account_type_id, active)
            if row is not None:
                temp_dta = dict(row)
                await update_user_permission_list(
                    request, temp_dta.get('id'), temp_dta.get('account_type_id'))
                ret_val = temp_dta
    except Exception as ccerr:
        logger.error('create_user_element service erred with: {}'.format(ccerr))

    return ret_val


# UPDATE CUSTOMER SERVICE
async def update_user_element(
        request: Request,
        user_id: int = 0,
        email: str = '',
        password: str = '',
        fullname: str = '',
        locked: bool = False,
        language_id: int = 0,
        timezone: int = 0,
        map_pool_time: int = 900,
        account_type_id: int = 0,
        active: bool = True) -> dict:
    """ Update user element by id.

    :param request:
    :param user_id:
    :param email:
    :param password:
    :param fullname:
    :param timezone:
    :param language_id:
    :param map_pool_time:
    :param account_type_id:
    :param locked:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_user_element_query
    try:

        old_user_data = await get_user_by_id(request, user_id)

        if old_user_data:
            user_email = old_user_data.get('email') if email == '' else email
            user_password = old_user_data.get('password') if password == '' else password
            user_fullname = old_user_data.get('fullname') if fullname == '' else fullname
            user_language_id = old_user_data.get('language_id') if language_id == 0 else language_id
            user_timezone = old_user_data.get('timezone_id') if timezone is None else timezone
            user_map_pool_time = old_user_data.get('map_pool_time') if map_pool_time == 0 else map_pool_time

            async with request.app.pg.acquire() as connection:
                timezone_element = await get_timezone_element(request, timezone_id=user_timezone)
                row = await connection.fetchrow(
                    query_str, user_id, user_email, user_password, user_fullname,
                    locked, user_language_id,
                    ujson.dumps(
                        {
                            'timezone_id': timezone_element.get('id'),
                            'timezone_name': timezone_element.get('name'),
                            'map_pool_time': user_map_pool_time
                        }
                    ),
                    account_type_id, active
                )
                if row is not None:
                    temp_dta = dict(row)
                    if temp_dta:
                        await update_user_permission_list(
                            request, temp_dta.get('id'), temp_dta.get('account_type_id'))

                    ret_val = temp_dta

    except Exception as dccerr:
        logger.error('update_user_element service erred with: {}'.format(dccerr))

    return ret_val


async def update_user_element_timezone(
        request: Request,
        user_id: int = 0,
        timezone_id: int = 0) -> dict:
    """ Update user element timezone by id.

    :param request:
    :param user_id:
    :param timezone_id:
    :return:
    """

    ret_val = {}
    query_str = update_user_element_timezone_query
    try:

        old_user_data = await get_user_by_id(request, user_id)

        if old_user_data:
            user_timezone = old_user_data.get('timezone_id') if timezone_id == 0 else timezone_id
            user_map_pool_time = old_user_data.get('map_pool_time')

            async with request.app.pg.acquire() as connection:
                timezone_element = await get_timezone_element(request, timezone_id=user_timezone)
                row = await connection.fetchrow(
                    query_str,
                    user_id,
                    ujson.dumps(
                        {
                            'timezone_id': timezone_element.get('id'),
                            'timezone_name': timezone_element.get('name'),
                            'map_pool_time': user_map_pool_time
                        }
                    )
                )

                if row is not None:
                    ret_val = dict(row)

    except Exception as dccerr:
        logger.error('update_user_element_timezone service erred with: {}'.format(dccerr))

    return ret_val


async def update_user_element_map_pool_time(
        request: Request,
        user_id: int = 0,
        map_pool_time: int = 5) -> dict:
    """ Update user element map pool time.

    :param request:
    :param user_id:
    :param map_pool_time:
    :return:
    """

    ret_val = {}
    query_str = update_user_element_map_pool_time_query
    try:

        old_user_data = await get_user_by_id(request, user_id)

        if old_user_data:
            user_timezone_id = old_user_data.get('timezone_id')
            user_timezone_name = old_user_data.get('timezone_name')
            user_map_pool_time = old_user_data.get('map_pool_time') if map_pool_time == 0 else map_pool_time

            async with request.app.pg.acquire() as connection:
                row = await connection.fetchrow(
                    query_str,
                    user_id,
                    ujson.dumps(
                        {
                            'timezone_id': user_timezone_id,
                            'timezone_name': user_timezone_name,
                            'map_pool_time': user_map_pool_time
                        }
                    )
                )

                if row is not None:
                    ret_val = dict(row)

    except Exception as dccerr:
        logger.error('update_user_element_map_pool_time service erred with: {}'.format(dccerr))

    return ret_val


async def update_user_element_language(
        request: Request,
        user_id: int = 0,
        language_id: int = 0):
    """ Update language for user element

    :param request:
    :param user_id:
    :param language_id:
    :return:
    """

    ret_val = {}
    query_str = update_user_element_language_query
    try:

        async with request.app.pg.acquire() as connection:
            dta = await connection.fetchrow(query_str, user_id, language_id)

            if dta is not None:
                user_element = await get_user_by_id(request, dta.get('id'))
                ret_val = user_element
    except Exception as dccerr:
        logger.error('update_user_element_language service erred with: {}'.format(dccerr))

    return ret_val


# DELETE CUSTOMER SERVICE
async def delete_user_element(
        request: Request,
        user_id: int = 0) -> dict:
    """ Delete user element by user id.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = delete_user_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id)
            if row is not None:
                await delete_user_permission_list_by_user_id(request, user_id)
                ret_val = dict(row)
    except Exception as dccerr:
        logger.error('delete_user_element service erred with: {}'.format(dccerr))

    return ret_val
