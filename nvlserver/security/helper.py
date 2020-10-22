#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
import ujson
from sanic.request import Request
from sanic.log import logger
from web_backend.config import SALT
from web_backend.nvlserver.module.user.service import get_user_by_id
from web_backend.nvlserver.module.permission.service import (
    get_permission_list_for_user, get_permission_module_list_by_user_id
)

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'generate_password', 'check_password',
    'update_password', 'remove_user_from_redis',
    'change_lock_state', 'check_unique_by_column_name',
    'update_user_in_redis', 'generate_new_access_token'
]


async def generate_password(
        request,
        plain_password: str,
        salt: str = SALT) -> object:
    """

    :param request:
    :param plain_password:
    :param salt:
    :return:
    """

    generate_pass_query = '''SELECT crypt((SELECT concat($1::VARCHAR, $2::VARCHAR) AS dta),
     gen_salt('bf', 8)) AS crypted_password;'''

    ret_val = None

    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(generate_pass_query, plain_password, salt)
            if row is not None:
                ret_val = row

    except Exception as guid_err:
        logger.error('user.generate_password erred with {}'.format(guid_err))

    return ret_val


async def check_password(
        request,
        user_ident,
        plain_pass: str,
        user_table: str = 'user',
        user_filter_column: str = 'email') -> bool:
    """

    :param request:
    :param plain_pass:
    :param user_table:
    :param user_ident:
    :param user_filter_column:
    :return:
    """

    # noinspection SqlResolve
    query_pass_checker = '''
        SELECT 1::bigint = (SELECT count(*) FROM public.{} WHERE {} = $1::VARCHAR
         AND password = crypt($2::VARCHAR, password)) AS pass_correct;
    '''.format(user_table, user_filter_column)

    ret_val = False

    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_pass_checker, user_ident, plain_pass + SALT)
            if row is not None:
                ret_val = row

    except Exception as guid_err:
        logger.error('user.check_password erred with {}'.format(guid_err))

    # print('THIS IS THE DATA CHECK PASSWORD: {}'.format(ret_val))
    return ret_val


async def update_password(
        request,
        user_ident,
        crypted_password: str,
        user_table: str = 'user',
        user_filter_column: str = 'email') -> bool:
    """ Update password method.

    :param request:
    :param user_ident:
    :param crypted_password:
    :param user_table:
    :param user_filter_column:
    :return:
    """

    # noinspection SqlResolve
    query_update_password = '''
        UPDATE public.{} 
            SET password = $2
            WHERE {} = $1 RETURNING TRUE;
        '''.format(user_table, user_filter_column)

    ret_val = False

    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_update_password, user_ident, crypted_password)
            if row is not None:
                ret_val = row

    except Exception as guid_err:
        logger.error('user.update_password erred with {}'.format(guid_err))

    # print('THIS IS THE DATA CHECK PASSWORD: {}'.format(ret_val))
    return ret_val


async def remove_user_from_redis(
        request,
        user_id: int = 0) -> bool:
    """ Update user element in redis.

    :param request:
    :param user_id:
    :return:
    """
    ret_val = False

    db_user = await get_user_by_id(request, user_id)
    if db_user:

        await request.app.redis.delete('user:{}'.format(db_user.get('user_id')))
        ret_val = True

    return ret_val


async def change_lock_state(
        request,
        user_ident,
        lock_state: bool = False,
        user_table: str = 'user',
        user_filter_column: str = 'id') -> bool:
    """ Update password method.

    :param request:
    :param user_ident:
    :param lock_state:
    :param user_table:
    :param user_filter_column:
    :return:
    """

    # noinspection SqlResolve
    query_change_lock_state = '''
        UPDATE public.{} 
            SET locked = $2
            WHERE {} = $1 RETURNING *;
        '''.format(user_table, user_filter_column)

    ret_val = False

    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_change_lock_state, user_ident, lock_state)
            if row is not None:
                if lock_state is False:
                    await remove_user_from_redis(request, row.get('id'))
                ret_val = row

    except Exception as guid_err:
        logger.error('user.update_password erred with {}'.format(guid_err))

    # print('THIS IS THE DATA CHECK PASSWORD: {}'.format(ret_val))
    return ret_val


async def check_unique_by_column_name(
        request,
        user_ident: object = None,
        user_table: str = 'user',
        user_filter_column: str = 'email') -> bool:
    """ Check if the value in column is unique in table.

    :param request:
    :param user_ident:
    :param user_table:
    :param user_filter_column:
    :return:
    """

    # noinspection SqlResolve
    unique_column_value_query = '''
        SELECT COUNT(*)
         FROM public.{} WHERE {} = $1::VARCHAR AND deleted is FALSE;
    '''.format(user_table, user_filter_column)

    ret_val = False

    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(unique_column_value_query, user_ident)
            if row is not None and row == 0:
                ret_val = True

    except Exception as guid_err:
        logger.error('user.check_unique_by_column_name erred with {}'.format(guid_err))

    return ret_val


async def update_user_in_redis(
        request, user_id: int = 0) -> bool:
    """ Update user element in redis.

    :param request:
    :param user_id:
    :return:
    """
    ret_val = False

    db_user = await get_user_by_id(request, user_id)
    if db_user:
        scopes = await get_permission_list_for_user(request, db_user.get('user_id'))
        module_list = await get_permission_module_list_by_user_id(request, user_id=db_user.get('user_id'))
        # logger.info('THESE ARE SCOPES: {}'.format(scopes))
        if scopes:
            db_user.update({'scopes': [x.get('permission') for x in scopes]})
        if module_list:
            db_user.update({'acl': [x.get('module_name') for x in module_list]})

        await request.app.redis.set('user:{}'.format(
            db_user.get('user_id')), ujson.dumps(db_user))
        ret_val = True

    return ret_val


async def generate_new_access_token(
        request: Request,
        user_id: int = 0):
    """

    :param request:
    :param user_id:
    :return:
    """

    user = await get_user_by_id(request, user_id=user_id)
    scopes = await get_permission_list_for_user(request, user_id=user_id)
    module_list = await get_permission_module_list_by_user_id(
        request, user_id=user_id)
    if scopes:
        user.update({'scopes': [x.get('permission') for x in scopes]})
    if module_list:
        user.update({'acl': [x.get('module_name') for x in module_list]})
    token = await request.app.auth.generate_access_token(user)

    return token
