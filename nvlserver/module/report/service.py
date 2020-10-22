#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
import time
from sanic.log import logger
# from decimal import Decimal
from sanic.request import Request
# from shapely.geometry import Point, LineString, Polygon

# NVL POINT IMPORTS
from .specification.get_nvl_position_specification import (
    get_nvl_position_list_query, get_nvl_position_list_count_query,
    get_nvl_distance_query
)

from web_backend.nvlserver.helper.asyncpg_types import decode_geometry, encode_geometry


__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_nvl_position_list', 'get_nvl_position_list_count', 'get_nvl_distance'
]


# NVL POINT SERVICES
async def get_nvl_position_list(
        request: Request,
        user_id: int = 0,
        traceable_object_id: int = 0,
        date_from: object = None,
        date_to: object = None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get get_nvl_position_list .

    :param request:
    :param user_id:
    :param traceable_object_id:
    :param date_from:
    :param date_to:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_nvl_position_list_query

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

            # print('--------------------------------------------------------------')
            # print(user_id, traceable_object_id, date_from, date_to, limit, offset)
            # print('--------------------------------------------------------------')
            # print(time.time())
            # print(user_id, traceable_object_id, date_from, date_to, limit, offset)
            if limit > 0:
                # print('--------------------------------------------------------------')
                query_str += ' ORDER BY hmup.id DESC LIMIT $5 OFFSET $6;'
                # print('đđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđđ')
                # print(query_str)
                rows = await connection.fetch(
                    query_str, user_id, traceable_object_id, date_from, date_to, limit, offset)
                # print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                # print(rows, type(rows))
                # print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
            else:
                # print('-----------++++++++++++++++++++++++++++++++++++++++++++--------')
                query_str += ' ORDER BY hmup.id DESC'
                rows = await connection.fetch(query_str, user_id, traceable_object_id, date_from, date_to)
            # print(rows)
            if rows:
                ret_val = [dict(x) for x in rows]
                # print(ret_val)
            # print(time.time())

    except Exception as gclerr:
        logger.error('get_nvl_position_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_nvl_position_list_count(
        request: Request,
        user_id: int = 0,
        traceable_object_id: int = 0,
        date_from: object = None,
        date_to: object = None) -> int:
    """ Get nvl_point list count.

    :param request:
    :param user_id:
    :param traceable_object_id:
    :param date_from:
    :param date_to:
    :return:
    """

    ret_val = 0
    query_str = get_nvl_position_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str,  user_id, traceable_object_id, date_from, date_to)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_nvl_position_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_distance(
        request: Request,
        user_id: int = 0,
        traceable_object_id: int = 0,
        date_from: object = None,
        date_to: object = None) -> float:
    """ Get get_nvl_position_list .

    :param request:
    :param user_id:
    :param traceable_object_id:
    :param date_from:
    :param date_to:
    :return:
    """
    ret_val = 0.0

    query_str = get_nvl_distance_query

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

            row = await connection.fetchval(query_str, user_id, traceable_object_id, date_from, date_to)

            if row is not None:
                # print('THIS IS DISTANCE : {}'.format(row))
                ret_val = row

    except Exception as gclerr:
        logger.error('get_nvl_distance service erred with: {}'.format(gclerr))

    return ret_val
