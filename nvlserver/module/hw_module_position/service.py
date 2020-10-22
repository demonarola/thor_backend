#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from geojson import Feature, loads
from sanic.log import logger
from sanic.request import Request
from web_backend.nvlserver.helper.asyncpg_types import decode_geometry, encode_geometry

from .specification.create_hw_module_position_specification import (
    create_hw_module_position_element_query
)
from .specification.delete_hw_module_position_specification import (
    delete_hw_module_position_element_query, delete_hw_module_position_all_query
)
from .specification.get_hw_module_position_specification import (
    get_hw_module_position_list_query, get_hw_module_position_list_count_query, get_hw_module_position_element_query,
    get_hw_module_linestring_list_query, get_hw_module_last_point_list_query
)

from .specification.update_hw_module_position_specification import (
    update_hw_module_position_element_query
)


__all__ = [
    # SERVICES WORKING ON HW MODULE POSITION TABLE
    'get_hw_module_position_list', 'get_hw_module_position_last_point_list', 'get_hw_module_position_linestring_list',
    'get_hw_module_position_list_count', 'get_hw_module_position_element', 'create_hw_module_position_element',
    'update_hw_module_position_element', 'delete_hw_module_position_element', 'delete_hw_module_all_positions'
]


async def get_hw_module_position_list(
        request: Request,
        hw_module_id=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get get_hw_module_position list.

    :param request:
    :param hw_module_id:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_hw_module_position_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY hmp.id DESC LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                await connection.set_type_codec(
                    'geometry',
                    encoder=encode_geometry,
                    decoder=decode_geometry,
                    format='binary',
                )
                rows = await connection.fetch(query_str, hw_module_id, limit, offset)
        else:
            query_str += ' ORDER BY hmp.id DESC;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                await connection.set_type_codec(
                    'geometry',
                    encoder=encode_geometry,
                    decoder=decode_geometry,
                    format='binary',
                )
                rows = await connection.fetch(query_str, hw_module_id)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_hw_module_position_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_position_last_point_list(
        request: Request,
        user_id=None,
        hw_module_id=None) -> list:
    """ Get hw_module_position list ordered by country id desc.

    :param request:
    :param hw_module_id:
    :param user_id:
    :return:
    """
    ret_val = []

    query_str = get_hw_module_last_point_list_query

    try:
        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            rows = await connection.fetch(query_str, user_id, hw_module_id)

            if rows:

                layer_list = [dict(x) for x in rows]

                transcribed_list = []
                for row in layer_list:
                    tmp_pos = loads(ujson.dumps(row.get('pos')))

                    transcribed_list.append(
                        Feature(geometry=tmp_pos,
                                properties={'hw_module_id': row.get('hw_module_id')})
                    )

                ret_val = transcribed_list

    except Exception as gclerr:
        logger.error('get_hw_module_position_last_point_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_position_linestring_list(
        request: Request,
        hw_module_id=None) -> list:
    """ Get hw_module_position_linestring list ordered by created_on desc.

    :param request:
    :param hw_module_id:
    :return:
    """
    ret_val = []

    query_str = get_hw_module_linestring_list_query

    try:
        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            rows = await connection.fetch(query_str, hw_module_id)

            if rows is not None:
                layer_list = [dict(x) for x in rows]

                transcribed_list = []
                for row in layer_list:
                    tmp_line = loads(ujson.dumps(row.get('line')))

                    transcribed_list.append(
                        Feature(geometry=tmp_line,
                                properties={'hw_module_id': row.get('hw_module_id')})
                    )

                ret_val = transcribed_list

    except Exception as gclerr:
        logger.error('get_hw_module_position_linestring_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_position_list_count(
        request: Request,
        hw_module_id=None) -> int:
    """ Get get_hw_module_position list count.

    :param request:
    :param hw_module_id:
    :return:
    """

    ret_val = 0
    query_str = get_hw_module_position_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, hw_module_id)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_hw_module_position_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_hw_module_position_element(
        request: Request,
        hw_module_position_id: int = 0) -> dict:
    """ Get hw_module_position element

    :param request:
    :param hw_module_position_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            row = await connection.fetchrow(query_str, hw_module_position_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_hw_module_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_hw_module_position_element(
        request: Request, name: str = '',
        hw_module_position_type_id: int = 0,
        user_id: int = 0,
        note: str = '',
        show_on_map: bool = False,
        action: bool = False,
        active: bool = True) -> dict:
    """ Create hw_module_position element

    :param request:
    :param name:
    :param hw_module_position_type_id:
    :param user_id:
    :param note:
    :param show_on_map:
    :param action:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_hw_module_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, name, hw_module_position_type_id, user_id, note, show_on_map, action, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('create_hw_module_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_position_element(
        request: Request,
        hw_module_position_id: int = 0,
        name: str = '',
        hw_module_position_type_id: int = 0,
        user_id: int = 0,
        note: str = '',
        show_on_map: bool = False,
        action: bool = False,
        active: bool = True) -> dict:
    """ Update hw_module_position element

    :param request:
    :param hw_module_position_id:
    :param name:
    :param hw_module_position_type_id:
    :param user_id:
    :param note:
    :param show_on_map:
    :param action:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_hw_module_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_position_id, name, hw_module_position_type_id,
                user_id, note, show_on_map, action, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('update_hw_module_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_hw_module_position_element(
        request: Request,
        hw_module_id: int = 0) -> dict:
    """ Delete hw_module_position element

    :param request:
    :param hw_module_id:
    :return:
    """

    ret_val = {}
    query_str = delete_hw_module_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, hw_module_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_hw_module_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_hw_module_all_positions(
        request: Request) -> bool:
    """ Delete hw_module_position element

    :param request:
    :return:
    """

    ret_val = False
    query_str = delete_hw_module_position_all_query
    try:

        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str)
            if rows is not None:
                ret_val = True
    except Exception as cleerr:
        logger.error('delete_hw_module_all_positions service erred with: {}'.format(cleerr))

    return ret_val
