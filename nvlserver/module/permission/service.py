#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

from sanic.log import logger
from sanic.request import Request

from .specification.get_permission_specification import (
    get_permission_list_query, get_permission_list_count_query, get_permission_list_by_user_id_query,
    get_permission_module_list_by_user_id_query
)

from .specification.get_account_type_permission_association_specification import (
    get_permission_list_by_account_type_id_query
)

from .specification.delete_user_permission_association_specification import (
    delete_user_permission_association_by_user_id_query, delete_user_permission_association_query
)
from .specification.create_user_permission_association_specification import create_user_permission_association_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_permission_list', 'get_permission_list_count', 'get_permission_list_for_user',
    'get_permission_module_list_by_user_id', 'get_permission_list_for_account_type', 'update_user_permission_list',
    'delete_user_permission_list_by_user_id'
]


async def get_permission_list(
        request: Request,
        module=None, action=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get permission list ordered by permission id desc.

    :param request:
    :param module:
    :param action:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_permission_list_query

    try:
        if limit > 0:
            query_str += ' LIMIT $3 OFFSET $4 ORDER BY pmr.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, module, action, limit, offset)
        else:
            query_str += ' ORDER BY pmr.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, module, action)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_permission_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_permission_list_count(
        request: Request,
        module=None,
        action=None) -> int:
    """ Get city list count.

    :param request:
    :param module:
    :param action:
    :return:
    """

    ret_val = 0
    query_str = get_permission_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, module, action)
        if row is not None:
            ret_val = row
    except Exception as gclcerr:
        logger.error('get_permission_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_permission_list_for_user(
        request: Request,
        user_id: int = 0) -> list:
    """ Get permission list ordered by permission id desc.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = []

    query_str = get_permission_list_by_user_id_query

    try:

        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, user_id)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_permission_list_for_user service erred with: {}'.format(gclerr))

    return ret_val


async def get_permission_module_list_by_user_id(
        request: Request,
        user_id: int = 0) -> list:
    """ Get permission module list for user.

    :param request:
    :param user_id:
    :return:
    """
    ret_val = []

    query_str = get_permission_module_list_by_user_id_query

    try:
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, user_id)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_permission_module_list_by_user_id service erred with: {}'.format(gclerr))

    return ret_val


async def get_permission_list_for_account_type(
        request: Request,
        account_type_id: int = 0,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get permission list ordered by permission id desc.

    :param request:
    :param account_type_id:
    :param limit:
    :param offset:
    :return:
    """

    ret_val = []

    query_str = get_permission_list_by_account_type_id_query

    try:
        if limit > 0:
            query_str += ' LIMIT $2 OFFSET $3 ORDER BY act.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, account_type_id, limit, offset)
        else:
            query_str += ' ORDER BY act.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, account_type_id)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_permission_list_for_account_type service erred with: {}'.format(gclerr))

    return ret_val


async def update_user_permission_list(
        request: Request,
        user_id: int = 0,
        account_type_id: int = 0
        # permission_list: list = None
        ) -> bool:
    """ Transfer permission list from account to user. Currently user can only have the
    same permissions as account perms in future a subset of the perms could be passed.

    :param request:
    :param user_id:
    :param account_type_id:
    :return:
    """

    ret_val = False

    old_perm_list = await get_permission_list_for_user(request, user_id)
    account_perm_list = await get_permission_list_for_account_type(request, account_type_id)

    try:

        if old_perm_list:
            async with request.app.pg.acquire() as connection:
                for perm in old_perm_list:
                    await connection.fetchrow(
                        delete_user_permission_association_query, user_id, perm.get('permission_id'))

        if account_perm_list:
            async with request.app.pg.acquire() as connection:
                for perm in account_perm_list:
                    await connection.fetchrow(
                        create_user_permission_association_query, user_id, perm.get('permission_id'))
        ret_val = True
    except Exception as uup_err:
        logger.error('update_user_permission_list failed with: {}'.format(uup_err))

    return ret_val


async def delete_user_permission_list_by_user_id(
        request: Request,
        user_id: int = 0
        # permission_list: list = None
        ) -> bool:
    """ Delete user permission list

    :param request:
    :param user_id:
    :return:
    """

    ret_val = False

    query_str = delete_user_permission_association_by_user_id_query
    try:
        async with request.app.pg.acquire() as connection:
            await connection.fetchrow(query_str, user_id)
        ret_val = True
    except Exception as uup_err:
        logger.error('delete_user_permission_list_by_user_id failed with: {}'.format(uup_err))

    return ret_val
