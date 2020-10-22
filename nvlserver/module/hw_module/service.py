#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
import time
from sanic.log import logger
from sanic.request import Request

from .specification.get_hw_module_specification import (
    get_hw_module_list_query, get_hw_module_list_count_query, get_hw_module_element_query,
    get_hw_module_list_dropdown_query, get_hw_module_element_by_traceable_object_id_query,
    get_hw_module_list_user_id_hw_module_id_list_query
)

from .specification.create_hw_module_specification import create_hw_module_element_query
from .specification.update_hw_module_specification import (
    update_hw_module_element_query, update_user_hw_module_element_query
)
from .specification.delete_hw_module_specification import delete_hw_module_element_query
from .specification.get_hw_module_random_str_specification import (
    hw_module_random_str_unique_query, hw_module_random_str_unique_unassigned_list_query
)


__all__ = [
    # SERVICES WORKING ON HW MODULE TABLE
    'get_hw_module_list', 'get_hw_module_dropdown_list', 'get_hw_module_list_count',
    'get_hw_module_element', 'get_hw_module_element_by_traceable_object_id', 'get_hw_module_list_by_user_hw_id_list',
    'create_hw_module_element', 'update_hw_module_element', 'update_user_hw_module_element',
    'delete_hw_module_element', 'get_hw_module_random_unique_str_list', 'get_hw_module_random_unique_str',
]


async def get_hw_module_list(
        request: Request,
        user_id=None,
        name=None,
        limit: int = 1,
        offset: int = 0) -> list:
    """ Get country list ordered by country id desc.

    :param request:
    :param name:
    :param user_id:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_hw_module_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY hwm.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, user_id, name, limit, offset)
        else:
            query_str += ' ORDER BY hwm.id DESC;'
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
        logger.error('get_hw_module_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_dropdown_list(
        request: Request,
        user_id=None,
        name=None) -> list:
    """ Get HW MODULE list ordered by traceable_object id desc filtered by name.

    :param request:
    :param user_id:
    :param name:
    :return:
    """
    ret_val = []
    # print(request, name)
    query_str = get_hw_module_list_dropdown_query

    try:
        query_str += ' ORDER BY hwm.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, user_id, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_hw_module_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_list_count(
        request: Request,
        user_id=None,
        name=None) -> int:
    """ Get hw_module list count.

    :param request:
    :param name:
    :param user_id:
    :return:
    """

    ret_val = 0
    query_str = get_hw_module_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_hw_module_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_hw_module_element(
        request: Request,
        hw_module_id: int = 0) -> dict:
    """ Get hw_module element

    :param request:
    :param hw_module_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, hw_module_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def get_hw_module_element_by_traceable_object_id(
        request: Request,
        user_id: object = None,
        traceable_object_id: int = 0) -> dict:
    """ Get hw_module element by traceable object id

    :param request:
    :param user_id:
    :param traceable_object_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_element_by_traceable_object_id_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            t1 = time.time()
            row = await connection.fetchrow(query_str, user_id, traceable_object_id)
            t2 = time.time()
            if row is not None:
                print('get_hw_module_element_by_traceable_object_id: {}'.format(t2-t1))
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_hw_module_element_by_traceable_object_id service erred with: {}'.format(cleerr))

    return ret_val


async def get_hw_module_list_by_user_hw_id_list(
        request: Request,
        user_id: object = None,
        hw_module_id_list: object = ()) -> list:
    """ Get hw module list by user_id and hw_module_list

    :param request:
    :param user_id:
    :param hw_module_id_list:
    :return:
    """

    ret_val = []

    query_str = get_hw_module_list_user_id_hw_module_id_list_query

    try:
        async with request.app.pg.acquire() as connection:

            rows = await connection.fetch(query_str, user_id, hw_module_id_list)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_hw_module_list_by_user_hw_id_list service erred with: {}'.format(gclerr))

    return ret_val


async def create_hw_module_element(
        request: Request,
        name: str = '',
        module_id: str = '',
        user_id: object = None,
        traceable_object_id: object = None,
        meta_information: dict = {},
        show_on_map: bool = False,
        active: bool = True) -> dict:
    """ Create hw_module element

    :param request:
    :param name:
    :param module_id:
    :param user_id:
    :param traceable_object_id:
    :param show_on_map:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_hw_module_element_query
    try:

        async with request.app.pg.acquire() as connection:

            row = await connection.fetchrow(
                query_str, name, module_id, user_id, traceable_object_id,
                ujson.dumps(meta_information), show_on_map, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_hw_module_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('create_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_element(
        request: Request,
        hw_module_id: int = 0,
        name: str = '',
        module_id: str = '',
        user_id: object = None,
        traceable_object_id: object = None,
        meta_information: dict = {},
        show_on_map: bool = False,
        active: bool = True) -> dict:
    """ Update hw_module element

    :param request:
    :param hw_module_id:
    :param name:
    :param module_id:
    :param user_id:
    :param traceable_object_id:
    :param meta_information:
    :param show_on_map:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_hw_module_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_id, name, module_id, user_id, traceable_object_id,
                ujson.dumps(meta_information), show_on_map, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_hw_module_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_user_hw_module_element(
        request: Request,
        hw_module_id: int = 0,
        user_id: object = None,
        traceable_object_id: object = None,
        show_on_map: bool = False,
        active: bool = True) -> dict:
    """ Update hw_module element

    :param request:
    :param hw_module_id:
    :param user_id:
    :param traceable_object_id:
    :param show_on_map:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_user_hw_module_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_id, user_id, traceable_object_id, show_on_map, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_hw_module_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_user_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_hw_module_element(
        request: Request,
        lift_id: int = 0) -> dict:
    """ Delete hw_module element

    :param request:
    :param lift_id:
    :return:
    """

    ret_val = {}
    query_str = delete_hw_module_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, lift_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def get_hw_module_random_unique_str_list(
        request: Request,
        module_id: str = None) -> []:
    """ Get hw_module element unique element str

    :param request:
    :param module_id:
    :return:
    """

    ret_val = []
    query_str = hw_module_random_str_unique_unassigned_list_query
    try:

        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, module_id)
            if rows is not None:
                ret_val = [dict(x) for x in rows]
    except Exception as cleerr:
        logger.error('get_hw_module_random_unique_str_list service erred with: {}'.format(cleerr))

    return ret_val


async def get_hw_module_random_unique_str(
        request: Request) -> str:
    """ Get hw_module element unique element str

    :param request:
    :return:
    """

    ret_val = ''
    query_str = hw_module_random_str_unique_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str)
            if row is not None:
                ret_val = row
    except Exception as cleerr:
        logger.error('get_hw_module_random_unique_str service erred with: {}'.format(cleerr))

    return ret_val
