#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from sanic.log import logger
from sanic.request import Request

# IMPORT USER HW ACTION TYPE SPECIFICATIONS
from .specification.get_user_hw_action_specification import (
    get_user_hw_action_list_query, get_user_hw_action_list_count_query,
    get_user_hw_action_element_query, get_user_hw_action_times_by_location_id_query
)

from .specification.delete_user_hw_action_specification import delete_user_hw_action_element_query
from .specification.update_user_hw_action_specification import update_user_hw_action_element_query
from .specification.create_user_hw_action_specification import create_user_hw_action_element_query

from .specification.user_hw_action_location_association_specification import (
    get_user_hw_action_location_element_query, create_user_hw_action_location_element_query,
    get_attached_user_hw_action_list_for_location_query,
    delete_user_hw_action_location_element_query, delete_attached_user_hw_action_list_for_location_query,
    get_attached_hw_action_id_list_for_location_query
)


__all__ = [
    # SERVICES WORKING ON USER HW ACTION TABLE
    'get_user_hw_action_list', 'get_user_hw_action_list_count', 'get_user_hw_action_dropdown_list',
    'get_user_hw_action_element', 'create_user_hw_action_element', 'update_user_hw_action_element',
    'delete_user_hw_action_element',
    # SERVICES WORKING ON USER HW ACTION LOCATION ASSOCIATION TABLES
    'get_user_hw_action_location_element',
    'create_user_hw_action_location_element', 'update_user_hw_action_location_element',
    'get_user_hw_action_list_by_location_id', 'delete_user_hw_action_list_by_location_id',
    # GET ACTION TIMES
    'get_user_hw_action_times_by_location_id'
]


async def get_user_hw_action_list(
        request: Request,
        user_id: object = None,
        name=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get user_hw_action list ordered by hw_action id desc.

    :param request:
    :param user_id:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_user_hw_action_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY uhwa.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, user_id, name, limit, offset)
        else:
            query_str += ' ORDER BY uhwa.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, user_id, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_user_hw_action_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_user_hw_action_list_count(
        request: Request,
        user_id: object = None,
        name=None) -> int:
    """ Get user_hw_action list count.

    :param request:
    :param user_id:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_user_hw_action_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_user_hw_action_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_user_hw_action_dropdown_list(
        request: Request,
        user_id: object = None,
        name=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get user_hw_action dropdown list.

    :param request:
    :param user_id:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_user_hw_action_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY uha.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, user_id, name, limit, offset)
        else:
            query_str += ' ORDER BY hwat.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_user_hw_action_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_user_hw_action_element(
        request: Request,
        user_id: object = None,
        user_hw_action_id: int = 0) -> dict:
    """ Get user_hw_action element by hw_action id.

    :param request:
    :param user_id:
    :param user_hw_action_id:
    :return:
    """

    ret_val = {}
    query_str = get_user_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, user_hw_action_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_user_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val


async def create_user_hw_action_element(
        request: Request,
        user_id: object = None,
        hw_action_id: object = None,
        value: str = '',
        date_from: object = None,
        date_to: object = None,
        active: bool = True) -> dict:
    """  Create user_hw_action element

    :param request:
    :param user_id:
    :param hw_action_id:
    :param value:
    :param date_from:
    :param date_to:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_user_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:

            row = await connection.fetchrow(
                query_str, user_id, hw_action_id, value,
                date_from, date_to, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('create_user_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_user_hw_action_element(
        request: Request,
        user_hw_action_id: int = 0,
        user_id: object = None,
        hw_action_id: object = None,
        value: str = '',
        date_from: object = None,
        date_to: object = None,
        active: bool = True) -> dict:
    """ Updated user hw action element.

    :param request:
    :param user_hw_action_id:
    :param user_id:
    :param hw_action_id:
    :param value:
    :param date_from:
    :param date_to:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_user_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_hw_action_id, user_id, hw_action_id, value,
                date_from, date_to, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('update_user_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_user_hw_action_element(
        request: Request,
        user_id: object = None,
        user_hw_action_id: int = 0) -> dict:
    """ Delete user_hw_action element.

    :param request:
    :param user_id:
    :param user_hw_action_id:
    :return:
    """

    ret_val = {}
    query_str = delete_user_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, user_hw_action_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_user_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val


# USER HW ACTION LOCATION SERVICES
async def get_user_hw_action_location_element(
        request: Request,
        user_hw_action_id: int = 0,
        location_id: int = 0) -> dict:
    """ Get user hw action location element

    :param request:
    :param user_hw_action_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = get_user_hw_action_location_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_hw_action_id, location_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_user_hw_action_location service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_user_hw_action_location_association(
        request: Request,
        user_hw_action_id: int = 0,
        location_id: int = 0) -> dict:
    """ Delete user hw action location element

    :param request:
    :param user_hw_action_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = delete_user_hw_action_location_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_hw_action_id, location_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_user_hw_action_location_element service erred with: {}'.format(gclcerr))

    return ret_val


async def create_user_hw_action_location_element(
        request: Request,
        user_hw_action_id: int = 0,
        location_id: int = 0) -> dict:
    """ Create user hw action location element

    :param request:
    :param user_hw_action_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = create_user_hw_action_location_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_hw_action_id, location_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('create_user_hw_action_location_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_user_hw_action_location_element(
        request: Request,
        user_hw_action_id: int = 0,
        location_id: int = 0) -> dict:
    """ Update user hw action location association.

    :param request:
    :param user_hw_action_id:
    :param location_id:
    :return:
    """

    ret_val = {}

    try:

        user_hw_action_location = await get_user_hw_action_location_element(
            request, user_hw_action_id=user_hw_action_id, location_id=location_id)

        if user_hw_action_location:
            ret_val = user_hw_action_location
        else:
            ret_val = await create_user_hw_action_location_element(
                request, user_hw_action_id=user_hw_action_id, location_id=location_id)
    except Exception as gclcerr:
        logger.error('update_user_hw_action_location_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_user_hw_action_list_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> []:
    """ Get user hw action location element

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = []
    query_str = get_attached_user_hw_action_list_for_location_query
    try:

        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(
                query_str, user_id, location_id)
            if rows is not None:
                ret_val = [dict(row) for row in rows]
                # print('THESE ARE ACTIONS ATTACHED: {}'.format(ret_val))
    except Exception as gclcerr:
        logger.error('get_user_hw_action_list_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def get_attached_user_hw_action_id_list(
        request: Request,
        location_id: int = 0) -> []:
    """ Get list of all user hw action ids attached on location.
     TU SAM
    :param request:
    :param location_id:
    :return:
    """

    ret_val = []
    query_str = get_attached_hw_action_id_list_for_location_query
    try:

        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, location_id)
            if rows is not None:
                # print(rows)
                ret_val = [dict(row).get('user_hw_action_id') for row in rows]
                # print('THESE ARE IDS OF ACTIONS ATTACHED: {}'.format(ret_val))
    except Exception as gclcerr:
        logger.error('get_attached_user_hw_action_id_list service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_user_hw_action_list_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> []:
    """ Delete user hw action list attached to location id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = []
    query_str = delete_attached_user_hw_action_list_for_location_query
    try:
        # print('THIS IS LOCATION ID: {}'.format(location_id))
        attached_hw_action_ids = await get_attached_user_hw_action_id_list(
            request, location_id=location_id)
        # print(
        # 'THESE ARE ATTACHED IDS IN delete_user_hw_action_list_by_location_id: {}'.format(attached_hw_action_ids))
        await delete_user_hw_action_location_association(
            request, user_hw_action_id=0, location_id=location_id)
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, attached_hw_action_ids)
            if rows is not None:
                ret_val = [dict(row) for row in rows]
                # print('THESE ARE ACTIONS ATTACHED: {}'.format(ret_val))
    except Exception as gclcerr:
        logger.error('delete_user_hw_action_list_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def get_user_hw_action_times_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> {}:
    """

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = get_user_hw_action_times_by_location_id_query
    try:
        # print('AAAAAAAAAAAAAAAAAAA')
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, location_id)
            if row is not None:
                ret_val = dict(row)
                # print('THESE ARE ACTION TIMES: {}'.format(ret_val))

    except Exception as gclcerr:
        logger.error('get_user_hw_action_times_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val
