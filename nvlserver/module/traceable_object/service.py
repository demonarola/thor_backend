#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic.log import logger
from sanic.request import Request

from .specification.get_traceable_object_specification import (
    get_traceable_object_list_query, get_traceable_object_list_count_query, get_traceable_object_element_query,
    get_traceable_object_list_dropdown_query,
)

from .specification.get_traceable_object_type_specification import (
    get_traceable_object_type_list_query, get_traceable_object_type_list_count_query,
    get_traceable_object_type_list_dropdown_query, get_traceable_object_type_element_query
)
from .specification.get_traceable_object_brand_specification import get_traceable_object_brand_list_dropdown_query
from .specification.get_traceable_object_model_specification import get_traceable_object_model_list_dropdown_query
from .specification.create_traceable_object_specification import create_traceable_object_element_query
from .specification.create_traceable_object_type_specification import create_traceable_object_type_element_query
from .specification.update_traceable_object_specification import update_traceable_object_element_query
from .specification.update_traceable_object_type_specification import update_traceable_object_type_element_query
from .specification.delete_traceable_object_specification import delete_traceable_object_element_query
from .specification.delete_traceable_object_type_specification import delete_traceable_object_type_element_query

from web_backend.nvlserver.module.hw_action.service import get_hw_action_list_user_type

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_traceable_object_list', 'get_traceable_object_dropdown_list',
    'get_traceable_object_list_count', 'get_traceable_object_element',
    'generate_traceable_object_element_actions', 'create_traceable_object_element',
    'update_traceable_object_element', 'delete_traceable_object_element',
    'get_traceable_object_type_list', 'get_traceable_object_type_dropdown_list',
    'get_traceable_object_type_list_count', 'get_traceable_object_type_element',
    'create_traceable_object_type_element', 'update_traceable_object_type_element',
    'delete_traceable_object_type_element', 'get_traceable_object_brand_dropdown_list',
    'get_traceable_object_model_dropdown_list'
]


async def get_traceable_object_list(
        request: Request,
        user_id: object = None,
        name=None, limit: int = 1,
        offset: int = 0) -> list:
    """ Get traceable_object list ordered by traceable_object id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :param user_id:
    :return:
    """
    ret_val = []

    query_str = get_traceable_object_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY tob.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, user_id, name, limit, offset)
        else:
            query_str += ' ORDER BY tob.id DESC;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, user_id, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_traceable_object_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_traceable_object_dropdown_list(
        request: Request,
        user_id: object = None,
        name=None) -> list:
    """ Get traceable_object list ordered by traceable_object id desc filtered by name.

    :param request:
    :param name:
    :param user_id:
    :return:
    """
    ret_val = []

    query_str = get_traceable_object_list_dropdown_query

    try:
        query_str += ' ORDER BY tob.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, user_id, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_traceable_object_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_traceable_object_list_count(
        request: Request,
        user_id=None,
        name=None) -> int:
    """ Get traceable object list count.

    :param request:
    :param name:
    :param user_id:
    :return:
    """

    ret_val = 0
    query_str = get_traceable_object_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_traceable_object_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_traceable_object_element(
        request: Request,
        user_id: object = None,
        traceable_object_id: int = 0) -> dict:
    """ Get traceable_object element

    :param request:
    :param user_id:
    :param traceable_object_id:
    :return:
    """

    ret_val = {}
    query_str = get_traceable_object_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, traceable_object_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_traceable_object_element service erred with: {}'.format(cleerr))

    return ret_val


async def generate_traceable_object_element_actions(
        request: Request) -> list:
    """ Generate traceable object element action

    :param request:
    :return:
    """

    ret_val = []
    action_list = await get_hw_action_list_user_type(request)
    if action_list:
        # print('generate_traceable_object_element_actions')
        ret_val = [dict(x) for x in action_list]
        # print(ret_val)

    return ret_val


async def create_traceable_object_element(
        request: Request,
        user_id: object = None,
        name: str = '',
        traceable_object_type_id: object = None,
        note: str = '',
        meta_information: dict = {},
        show_on_map: bool = False,
        action: bool = False,
        collision_avoidance_system: bool = False,
        active: bool = True) -> dict:
    """ Create traceable_object element

    :param request:
    :param name:
    :param traceable_object_type_id:
    :param user_id:
    :param note:
    :param meta_information:
    :param show_on_map:
    :param action:
    :param collision_avoidance_system:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_traceable_object_element_query
    try:
        # IF CREATING NEW TRACEABLE OBJECT COPY ALL USER TYPE ACTIONS TO OBJECT META INFORMATION
        action_list = await generate_traceable_object_element_actions(request)
        if action_list:
            meta_information.update({'action_list': action_list})

        # print('THIS IS META ON CREATE: {}'.format(meta_information))
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, name, traceable_object_type_id,
                note, ujson.dumps(meta_information),
                show_on_map, action, collision_avoidance_system,
                active)
            if row is not None:
                x = dict(row)
                # print('THIS IS CREATED OBJECT: {}'.format(x))
                ret_val = await get_traceable_object_element(request, user_id=user_id, traceable_object_id=x.get('id'))
    except Exception as cleerr:
        logger.error('create_traceable_object_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_traceable_object_element(
        request: Request,
        user_id: object = None,
        traceable_object_id: int = 0,
        name: str = '',
        traceable_object_type_id: int = 0,
        note: str = '',
        meta_information: dict = {},
        show_on_map: bool = False,
        action: bool = False,
        collision_avoidance_system: bool = False,
        active: bool = True) -> dict:
    """ Update traceable_object element

    :param request:
    :param traceable_object_id:
    :param name:
    :param meta_information:
    :param traceable_object_type_id:
    :param user_id:
    :param note:
    :param show_on_map:
    :param action:
    :param collision_avoidance_system:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_traceable_object_element_query
    try:

        action_list = await generate_traceable_object_element_actions(request)
        if action_list:
            meta_information.update({'action_list': action_list})

        # print('THIS IS META ON UPDATE: {}'.format(meta_information))
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, traceable_object_id, name, traceable_object_type_id,
                note, ujson.dumps(meta_information), show_on_map, action,
                collision_avoidance_system, active)

            if row is not None:
                # print(4)
                x = dict(row)
                ret_val = await get_traceable_object_element(
                    request, traceable_object_id=x.get('id'))

    except Exception as cleerr:
        logger.error('update_traceable_object_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_traceable_object_element(
        request: Request, user_id: object = None,
        traceable_object_id: int = 0) -> dict:
    """ Delete traceable_object element

    :param request:
    :param user_id:
    :param traceable_object_id:
    :return:
    """

    ret_val = {}
    query_str = delete_traceable_object_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, traceable_object_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_traceable_object_element service erred with: {}'.format(cleerr))

    return ret_val


# TRACEABLE OBJECT TYPE SERVICES
async def get_traceable_object_type_list(
        request: Request,
        name=None,
        limit: int = 1,
        offset: int = 0) -> list:
    """ Get traceable_object_type list ordered by traceable_object_type id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_traceable_object_type_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY tobt.id DESC LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY tobt.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_traceable_object_type_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_traceable_object_type_dropdown_list(
        request: Request,
        name=None) -> list:
    """ Get traceable_object_type list ordered by traceable_object_type id desc filtered by name.

    :param request:
    :param name:
    :return:
    """
    ret_val = []

    query_str = get_traceable_object_type_list_dropdown_query

    try:
        query_str += ' ORDER BY tobt.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_traceable_object_type_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_traceable_object_type_list_count(
        request: Request,
        name=None) -> int:
    """ Get city list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_traceable_object_type_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_traceable_object_type_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_traceable_object_type_element(
        request: Request,
        traceable_object_type_id: int = 0) -> dict:
    """ Get traceable_object element

    :param request:
    :param traceable_object_type_id:
    :return:
    """

    ret_val = {}
    query_str = get_traceable_object_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, traceable_object_type_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_traceable_object_type_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_traceable_object_type_element(
        request: Request,
        name: str = '',
        active: bool = True) -> dict:
    """ Create traceable_object element

    :param request:
    :param name:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_traceable_object_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, name, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('create_traceable_object_type_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_traceable_object_type_element(
        request: Request,
        user_id: object = None,
        traceable_object_id: int = 0,
        name: str = '',
        active: bool = True) -> dict:
    """ Update traceable_object_type element

    :param request:
    :param user_id:
    :param traceable_object_id:
    :param name:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_traceable_object_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, traceable_object_id, name, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('update_traceable_object_type_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_traceable_object_type_element(
        request: Request,
        traceable_object_id: int = 0) -> dict:
    """ Delete traceable_object_type element

    :param request:
    :param user_id:
    :param traceable_object_id:
    :return:
    """

    ret_val = {}
    query_str = delete_traceable_object_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, traceable_object_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_traceable_object_type_element service erred with: {}'.format(cleerr))

    return ret_val


# TRACEABLE OBJECT BRAND SERVICES
async def get_traceable_object_brand_dropdown_list(
        request: Request,
        name=None) -> list:
    """ Get traceable_object_brand dropdown.

    :param request:
    :param name:
    :return:
    """
    ret_val = []

    query_str = get_traceable_object_brand_list_dropdown_query

    try:
        query_str += ' ORDER BY tobb.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_traceable_object_brand_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_traceable_object_model_dropdown_list(
        request: Request, name=None,
        traceable_object_brand_id=None) -> list:
    """ Get traceable_object_model list dropdown.

    :param request:
    :param name:
    :param traceable_object_brand_id:
    :return:
    """
    ret_val = []

    query_str = get_traceable_object_model_list_dropdown_query

    try:
        query_str += ' ORDER BY tobm.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name, traceable_object_brand_id)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_traceable_object_model_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val
