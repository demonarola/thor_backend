#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
import time
# import asyncio
from geojson import Feature, loads
from sanic.log import logger
from sanic.request import Request
from typing import List
from web_backend.nvlserver.helper.asyncpg_types import decode_geometry, encode_geometry

from .specification.create_hw_module_position_specification import (
    create_hw_module_user_position_element_query
)
from .specification.delete_hw_module_position_specification import (
    delete_hw_module_user_position_element_query,
    delete_hw_module_user_position_all_query
)
from .specification.get_hw_module_position_specification import (
    get_hw_module_user_position_list_query, get_hw_module_user_position_element_query,
    get_hw_module_user_position_list_count_query,
    get_hw_module_user_linestring_list_query, get_hw_module_list_user_linestring_list_query,
    get_hw_module_user_last_point_element_query,
    get_hw_module_user_last_point_element_by_traceable_object_id_query,
    get_hw_module_list_user_linestring_list_timed_query,
    get_hw_module_user_linestring_list_timed_query
)

from .specification.update_hw_module_position_specification import (
    update_hw_module_user_position_element_query
)
from web_backend.nvlserver.module.hw_module.service import get_hw_module_list_by_user_hw_id_list
from web_backend.nvlserver.helper.geo_coloring import color_scheme


__all__ = [
    # SERVICES WORKING ON HW MODULE POSITION TABLE
    'get_hw_module_user_position_list', 'get_hw_module_user_position_list_count',
    'get_hw_module_user_position_last_point_element',
    'get_hw_module_user_position_last_point_list', 'get_hw_module_user_position_linestring_list',
    'get_hw_module_user_position_element', 'create_hw_module_user_position_element',
    'update_hw_module_user_position_element', 'delete_hw_module_user_position_element',
    'delete_hw_module_user_position_all', 'get_hw_module_user_position_last_point_element_by_traceable_object_id',
    'get_hw_module_user_position_linestring_list_timed'
]


# HW MODULE USER POSITION

async def get_hw_module_user_position_list(
        request: Request, user_id=None,
        hw_module_id=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get get_hw_module_user_position list.

    :param request:
    :param user_id:
    :param hw_module_id:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_hw_module_user_position_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY hmup.id DESC LIMIT $3 OFFSET $4;'
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
                rows = await connection.fetch(query_str, user_id, hw_module_id, limit, offset)
        else:
            query_str += ' ORDER BY hmup.id DESC;'
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

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_hw_module_user_position_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_user_position_list_count(
        request: Request,
        user_id=None,
        hw_module_id=None) -> int:
    """ Get hardware module user position list count.

    :param request:
    :param user_id:
    :param hw_module_id:
    :return:
    """

    ret_val = 0
    query_str = get_hw_module_user_position_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, hw_module_id)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_hw_module_user_position_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_hw_module_user_position_last_point_element(
        request: Request,
        user_id=None,
        hw_module_id=None) -> list:
    """ Return last point for module

    :param request:
    :param user_id:
    :param hw_module_id:
    :return:
    """

    ret_val = []
    query_str = get_hw_module_user_last_point_element_query

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
            # t1 = time.time()
            rows = await connection.fetch(query_str, hw_module_id, user_id)

            if rows is not None:
                ret_val = [dict(row) for row in rows]
                # t2 = time.time()
                # print('get_hw_module_user_position_last_point_element: {}'.format(t2 - t1))
    except Exception as gclerr:
        logger.error('get_hw_module_user_position_last_point_element service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_user_position_last_point_element_by_traceable_object_id(
        request: Request,
        user_id=None,
        traceable_object_id=None) -> dict:
    """ Return last point for module

    :param request:
    :param user_id:
    :param traceable_object_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_user_last_point_element_by_traceable_object_id_query

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
            t1 = time.time()
            row = await connection.fetchrow(query_str, user_id, traceable_object_id)

            if row is not None:
                ret_val = dict(row)
                t2 = time.time()
                print('get_hw_module_user_position_last_point_element_by_traceable_object_id: {}'.format(t2 - t1))
    except Exception as gclerr:
        logger.error(
            'get_hw_module_user_position_last_point_element_by_traceable_object_id service erred with: {}'.format(
                gclerr))

    return ret_val


async def create_feature_list(feature_list: List) -> List:
    """ Create feature list.

    :param feature_list:
    :return:
    """

    transcribed_list = []
    for row in feature_list:
        transcribed_list.append(
            Feature(geometry=row.get('position'),
                    properties={
                        'hw_module_id': row.get('hw_module_id'),
                        'gprs_active': row.get('gprs_active'),
                        'data': row.get('data'),
                        'vehicle_name': row.get('vehicle_name'),
                        'vehicle_data': row.get('vehicle_data')})
        )

    return transcribed_list


async def get_hw_module_user_position_last_point_list(
        request: Request,
        user_id=None,
        hw_module_id_list=()) -> list:
    """ Get hw_module_position list ordered by country id desc.

    :param request:
    :param hw_module_id_list:
    :param user_id:
    :return:
    """
    ret_val = []

    try:

        hw_ids = await get_hw_module_list_by_user_hw_id_list(
            request, user_id=user_id, hw_module_id_list=hw_module_id_list)

        if hw_ids:
            # TODO: locking
            t = time.time()
            # data = []
            # for x in hw_ids:
            #     chunk = await get_hw_module_user_position_last_point_element(request, user_id, x.get('id'))
            #     data.append(chunk)

            data = await get_hw_module_user_position_last_point_element(
                request, user_id, [x.get('id') for x in hw_ids])

            t1 = time.time()
            logger.info('GET ALL LAST POINTS: {}'.format(t1-t))

            if data:
                filtered_data = [x for x in data if len(x) > 0]

                # TODO: REMOVE AFTER TESTING
                # ret_val = await create_feature_list(filtered_data)

                transcribed_list = []
                for row in filtered_data:

                    transcribed_list.append(
                        Feature(geometry=row.get('position'),
                                properties={
                                    'hw_module_id': row.get('hw_module_id'),
                                    'gprs_active': row.get('gprs_active'),
                                    'data': row.get('data'),
                                    'vehicle_name': row.get('vehicle_name'),
                                    'vehicle_data': row.get('vehicle_data')})
                    )
                ret_val = transcribed_list
    except Exception as gclerr:
        logger.error('get_hw_module_user_position_last_point_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_user_position_linestring_list(
        request: Request,
        user_id=None,
        map_pool_time=900,
        hw_module_id=None) -> list:
    """ Get hw_module_position_linestring list ordered by created_on desc.

    :param request:
    :param hw_module_id:
    :param user_id:
    :param map_pool_time:
    :return:
    """
    ret_val = []

    query_str_module = get_hw_module_list_user_linestring_list_query
    query_str = get_hw_module_user_linestring_list_query

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

            if hw_module_id:
                rows = await connection.fetch(query_str_module, user_id, hw_module_id, map_pool_time)
            else:
                rows = await connection.fetch(query_str, user_id, map_pool_time)

            if rows is not None:
                layer_list = [dict(x) for x in rows]

                transcribed_list = []
                for row in layer_list:
                    tmp_line = loads(ujson.dumps(row.get('line')))

                    transcribed_list.append(
                        Feature(geometry=tmp_line,
                                properties={
                                    'hw_module_id': row.get('hw_module_id'),
                                    'color': color_scheme[
                                        (int(row.get('hw_module_id', 1)) % len(color_scheme))-1]
                                })
                    )

                ret_val = transcribed_list

    except Exception as gclerr:
        logger.error('get_hw_module_user_position_linestring_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_user_position_linestring_list_timed(
        request: Request,
        user_id=None,
        date_from=None,
        date_to=None,
        hw_module_id=None) -> list:
    """ Get hw_module_position_linestring list ordered by created_on desc.

    :param request:
    :param hw_module_id:
    :param user_id:
    :param date_from:
    :param date_to:
    :return:
    """
    ret_val = []

    query_str_module = get_hw_module_list_user_linestring_list_timed_query
    query_str = get_hw_module_user_linestring_list_timed_query

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

            if hw_module_id:
                rows = await connection.fetch(query_str_module, user_id, hw_module_id, date_from, date_to)
            else:
                rows = await connection.fetch(query_str, user_id, date_from, date_to)

            if rows is not None:
                layer_list = [dict(x) for x in rows]

                transcribed_list = []
                for row in layer_list:
                    tmp_line = loads(ujson.dumps(row.get('line')))

                    transcribed_list.append(
                        Feature(geometry=tmp_line,
                                properties={
                                    'hw_module_id': row.get('hw_module_id'),
                                    'color': color_scheme[
                                        (int(row.get('hw_module_id', 1)) % len(color_scheme))-1]
                                })
                    )

                ret_val = transcribed_list

    except Exception as gclerr:
        logger.error('get_hw_module_user_position_linestring_list_timed service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_module_user_position_element(
        request: Request,
        user_id: object = None,
        hw_module_position_id: int = 0) -> dict:
    """ Get hw_module_position element

    :param request:
    :param hw_module_position_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_user_position_element_query

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
            row = await connection.fetchrow(query_str, user_id, hw_module_position_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_hw_module_user_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_hw_module_user_position_element(
        request: Request,
        name: str = '',
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
    query_str = create_hw_module_user_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, name, hw_module_position_type_id, user_id, note, show_on_map, action, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('create_hw_module_user_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_user_position_element(
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
    query_str = update_hw_module_user_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_position_id, name, hw_module_position_type_id,
                user_id, note, show_on_map, action, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('update_hw_module_user_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_hw_module_user_position_element(
        request: Request,
        hw_module_id: int = 0) -> dict:
    """ Delete hw_module_position element

    :param request:
    :param hw_module_id:
    :return:
    """

    ret_val = {}
    query_str = delete_hw_module_user_position_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, hw_module_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_hw_module_user_position_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_hw_module_user_position_all(
        request: Request) -> bool:
    """ Delete hw_module_user_position all elements

    :param request:
    :return:
    """

    ret_val = False
    query_str = delete_hw_module_user_position_all_query
    try:

        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str)
            if rows is not None:
                ret_val = True
    except Exception as cleerr:
        logger.error('delete_hw_module_user_position_all service erred with: {}'.format(cleerr))

    return ret_val
