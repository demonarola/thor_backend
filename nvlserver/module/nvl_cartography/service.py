#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic.log import logger
from decimal import Decimal
from sanic.request import Request
from geojson import Feature
from shapely.geometry import Point, LineString, Polygon

# NVL POINT IMPORTS
from .specification.get_nvl_point_specification import (
    get_nvl_point_list_query, get_nvl_point_list_count_query,
    get_nvl_point_element_query, get_nvl_point_element_by_location_id_query,
    get_nvl_point_list_by_user_id_query
)
from .specification.delete_nvl_point_specification import (
    delete_nvl_point_element_query, delete_nvl_point_element_by_location_id_query
)
from .specification.update_nvl_point_specification import (
    update_nvl_point_element_query,
    update_nvl_point_element_partial_query
)
from .specification.create_nvl_point_specification import create_nvl_point_element_query

# NVL LINESTRING IMPORTS
from .specification.get_nvl_linestring_specification import (
    get_nvl_linestring_list_query, get_nvl_linestring_list_count_query,
    get_nvl_linestring_element_query, get_nvl_linestring_element_by_location_id_query,
    get_nvl_linestring_list_by_user_id_query
)
from .specification.delete_nvl_linestring_specification import (
    delete_nvl_linestring_element_query, delete_nvl_linestring_element_by_location_id_query
)
from .specification.update_nvl_linestring_specification import (
    update_nvl_linestring_element_query,
    update_nvl_linestring_element_partial_query
)
from .specification.create_nvl_linestring_specification import create_nvl_linestring_element_query

# NVL CIRCLE IMPORTS
from .specification.get_nvl_circle_specification import (
    get_nvl_circle_element_query, get_nvl_circle_list_count_query,
    get_nvl_circle_list_query, get_nvl_circle_element_by_location_id_query,
    get_nvl_circle_list_by_user_id_query
)
from .specification.delete_nvl_circle_specification import (
    delete_nvl_circle_element_query, delete_nvl_circle_element_by_location_id_query
)
from .specification.update_nvl_circle_specification import (
    update_nvl_circle_element_query, update_nvl_circle_element_partial_query
)
from .specification.create_nvl_circle_specification import create_nvl_circle_element_query

# NVL POLYGON IMPORTS
from .specification.get_nvl_polygon_specification import (
    get_nvl_polygon_element_query, get_nvl_polygon_list_count_query,
    get_nvl_polygon_list_query, get_nvl_polygon_element_by_location_id_query,
    get_nvl_polygon_list_by_user_id_query
)
from .specification.delete_nvl_polygon_specification import (
    delete_nvl_polygon_element_query, delete_nvl_polygon_element_by_location_id_query
)
from .specification.update_nvl_polygon_specification import update_nvl_polygon_element_query
from .specification.create_nvl_polygon_specification import create_nvl_polygon_element_query
from web_backend.nvlserver.helper.asyncpg_types import decode_geometry, encode_geometry

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_nvl_point_list', 'get_nvl_point_list_count', 'get_nvl_point_feature_list_by_user_id',
    'get_nvl_point_element', 'get_nvl_point_element_by_location_id', 'create_nvl_point_element',
    'update_nvl_point_element', 'delete_nvl_point_element', 'delete_nvl_point_element_by_location_id',
    'get_nvl_linestring_list', 'get_nvl_linestring_list_count', 'get_nvl_linestring_element',
    'get_nvl_linestring_element_by_location_id', 'get_nvl_linestring_feature_list_by_user_id',
    'create_nvl_linestring_element', 'update_nvl_linestring_element', 'update_nvl_linestring_partial_element',
    'delete_nvl_linestring_element', 'delete_nvl_linestring_element_by_location_id', 'get_nvl_circle_list',
    'get_nvl_circle_list_count', 'get_nvl_circle_element', 'get_nvl_circle_element_by_location_id',
    'get_nvl_circle_feature_list_by_user_id', 'create_nvl_circle_element', 'update_nvl_circle_element',
    'update_nvl_circle_partial_element', 'delete_nvl_circle_element_by_location_id',
    'delete_nvl_circle_element', 'get_nvl_polygon_list', 'get_nvl_polygon_list_count',
    'get_nvl_polygon_element', 'get_nvl_polygon_feature_list_by_user_id', 'get_nvl_polygon_element_by_location_id',
    'create_nvl_polygon_element', 'update_nvl_polygon_element', 'update_nvl_polygon_partial_element',
    'delete_nvl_polygon_element', 'delete_nvl_polygon_element_by_location_id', 'update_nvl_point_partial_element'
]


# NVL POINT SERVICES
async def get_nvl_point_list(
        request: Request,
        user_id: object = None,
        label=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get nvl_point list ordered by nvl_point id desc.

    :param request:
    :param label:
    :param limit:
    :param user_id:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_nvl_point_list_query

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
            if limit > 0:
                query_str += ' ORDER BY npt.id DESC LIMIT $3 OFFSET $4;'
                rows = await connection.fetch(query_str, user_id, label, limit, offset)
            else:
                query_str += ' ORDER BY npt.id DESC'
                rows = await connection.fetch(query_str, user_id, label)

            if rows is not None:
                ret_val = [dict(x) for x in rows]
                # for x in p_list:
                #     x['geom'] = mapping(x.get('geom')) if x.get('geom') is not None else None
                #    ret_val.append(x)

    except Exception as gclerr:
        logger.error('nvl_point service erred with: {}'.format(gclerr))

    return ret_val


async def get_nvl_point_list_count(
        request: Request,
        user_id: object = None,
        label=None) -> int:
    """ Get nvl_point list count.

    :param request:
    :param label:
    :param user_id:
    :return:
    """

    ret_val = 0
    query_str = get_nvl_point_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, label)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_nvl_point_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_point_feature_list_by_user_id(
        request: Request,
        user_id: object = None) -> list:
    """ Get all polygon with show on map set to true for user.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = []
    query_str = get_nvl_point_list_by_user_id_query
    try:

        async with request.app.pg.acquire() as connection:

            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            rows = await connection.fetch(query_str, user_id)
            if rows is not None:
                ret_val = [Feature(
                    geometry=x.get('geom'),
                    properties={
                        'label': x.get('label'),
                        'color': x.get('color'),
                        'icon': x.get('icon'),
                        'id': x.get('location_id'),
                        'name': x.get('location_name')
                    }) for x in rows]
    except Exception as gclcerr:
        logger.error('get_nvl_point_feature_list_by_user_id service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_point_element(
        request: Request,
        user_id: object = None,
        nvl_point_id: int = 0) -> dict:
    """ Get nvl_point element by nvl_point id.

    :param request:
    :param nvl_point_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_point_element_query
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
            row = await connection.fetchrow(query_str, user_id, nvl_point_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_nvl_point_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_point_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Get nvl_point element by nvl_point id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_point_element_by_location_id_query
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
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                ret_val = dict(row)

    except Exception as gclcerr:
        logger.error('get_nvl_point_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def create_nvl_point_element(
        request: Request,
        user_id: object = None,
        geom: object = None,
        label: str = '',
        color: str = '',
        icon: str = '',
        location_id: object = None,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Create nvl_point element

    :param request:
    :param geom:
    :param label:
    :param color:
    :param icon:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_nvl_point_element_query
    try:
        # print(
        #     Point((x.get('lng'), x.get('lat')) for x in geom), label, color, icon,
        #     location_id, user_id, ujson.dumps(meta_information), active)
        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )

            row = await connection.fetchrow(
                query_str, user_id, Point((x.get('lng'), x.get('lat')) for x in geom), label, color, icon,
                location_id, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('create_nvl_point_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_point_element(
        request: Request,
        user_id: object = None,
        nvl_point_id: int = 0,
        geom: object = None,
        label: str = '',
        color: str = '',
        icon: str = '',
        location_id: object = None,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Update nvl_point element by nvl_point id.

    :param request:
    :param nvl_point_id:
    :param geom:
    :param label:
    :param color:
    :param icon:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_point_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, nvl_point_id, Point(geom), label, color, icon,
                location_id, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_point_element_read service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_point_partial_element(
        request: Request,
        location_id: object = None,
        user_id: object = None,
        label: str = '',
        color: str = '',
        icon: str = '',
        active: bool = True) -> dict:
    """ Update nvl_point element by nvl_circle id.

    :param request:
    :param label:
    :param color:
    :param icon:
    :param location_id:
    :param user_id:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_point_element_partial_query
    query_append = ''
    params = []
    param_count = 3

    try:
        if label != '':
            query_append += 'label = ${}::VARCHAR,'.format(param_count)
            params.append(label)
            param_count += 1

        if color != '':
            query_append += 'color = ${}::VARCHAR,'.format(param_count)
            params.append(color)
            param_count += 1

        if icon != '':
            query_append += 'icon = ${}::VARCHAR,'.format(param_count)
            params.append(icon)
            param_count += 1

        if active is not None:
            query_append += 'active = ${}::BOOLEAN,'.format(param_count)
            params.append(active)
            param_count += 1

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str.format(query_append), location_id, user_id, *params)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_linestring_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_point_partial_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_point_element(
        request: Request,
        user_id: object = None,
        nvl_point_id: int = 0) -> dict:
    """ Delete nvl_point element by nvl_point id.

    :param request:
    :param user_id:
    :param nvl_point_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_point_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, nvl_point_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_point_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_point_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Delete nvl_point element by location id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_point_element_by_location_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_point_element(request, user_id=user_id, nvl_point_id=dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_point_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


# NVL LINESTRING SERVICES
async def get_nvl_linestring_list(
        request: Request,
        user_id: object = None,
        label=None, limit: int = 0,
        offset: int = 0) -> list:
    """ Get nvl_linestring list ordered by nvl_linestring id desc.

    :param request:
    :param user_id:
    :param label:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_nvl_linestring_list_query

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
            if limit > 0:
                query_str += ' ORDER BY nls.id DESC LIMIT $3 OFFSET $4;'
                rows = await connection.fetch(query_str, user_id, label, limit, offset)
            else:
                query_str += ' ORDER BY nls.id DESC;'
                rows = await connection.fetch(query_str, user_id, label)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('nvl_linestring service erred with: {}'.format(gclerr))

    return ret_val


async def get_nvl_linestring_list_count(
        request: Request,
        user_id: object = None,
        label: str = '') -> int:
    """ Get nvl_linestring list count.

    :param request:
    :param label:
    :param user_id:
    :return:
    """

    ret_val = 0
    query_str = get_nvl_linestring_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, label)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_nvl_linestring_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_linestring_element(
        request: Request,
        user_id: object = None,
        nvl_linestring_id: int = 0) -> dict:
    """ Get nvl_linestring element by nvl_linestring id.

    :param request:
    :param nvl_linestring_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_linestring_element_query
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
            row = await connection.fetchrow(query_str, user_id, nvl_linestring_id)
            if row is not None:
                ret_val = dict(row)

    except Exception as gclcerr:
        logger.error('get_nvl_linestring_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_linestring_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Get nvl_linestring element by nvl_linestring id.

    :param request:
    :param location_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_linestring_element_by_location_id_query
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
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_nvl_linestring_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_linestring_feature_list_by_user_id(
        request: Request,
        user_id: object = None) -> list:
    """ Get all linestring with show on map set to true for user.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = []
    query_str = get_nvl_linestring_list_by_user_id_query
    try:

        async with request.app.pg.acquire() as connection:

            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            import time

            rows = await connection.fetch(query_str, user_id)

            if rows is not None:

                ret_val = [Feature(
                    geometry=x.get('geom'),
                    properties={
                        'label': x.get('label'),
                        'color': x.get('color'),
                        'id': x.get('location_id'),
                        'name': x.get('location_name')
                    }) for x in rows]
    except Exception as gclcerr:
        logger.error('get_nvl_linestring_feature_list_by_user_id service erred with: {}'.format(gclcerr))

    return ret_val


async def create_nvl_linestring_element(
        request: Request,
        user_id: object = None,
        geom: object = None,
        label: str = '',
        color: str = '',
        location_id: object = None,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """  Create nvl_linestring element

    :param request:
    :param geom:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_nvl_linestring_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            row = await connection.fetchrow(
                query_str, user_id, LineString([(x.get('lng'), x.get('lat')) for x in geom]), label, color,
                location_id, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('create_nvl_linestring_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_linestring_element(
        request: Request,
        user_id: object = None,
        nvl_linestring_id: int = 0,
        geom: object = None,
        label: str = '',
        color: str = '',
        location_id: object = None,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """  Update read status on nvl_linestring element by nvl_point id.

    :param request:
    :param nvl_linestring_id:
    :param geom:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_linestring_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, nvl_linestring_id, LineString(geom), label, color,
                location_id, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_linestring_element_read service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_linestring_partial_element(
        request: Request,
        location_id: object = None,
        user_id: object = None,
        label: str = '',
        color: str = '',
        active: bool = True) -> dict:
    """ Update nvl_linestring element by nvl_circle id.

    :param request:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_linestring_element_partial_query
    query_append = ''
    params = []
    param_count = 3

    try:
        if label != '':
            query_append += 'label = ${}::VARCHAR,'.format(param_count)
            params.append(label)
            param_count += 1

        if color != '':
            query_append += 'color = ${}::VARCHAR,'.format(param_count)
            params.append(color)
            param_count += 1

        if active is not None:
            query_append += 'active = ${}::BOOLEAN,'.format(param_count)
            params.append(active)
            param_count += 1

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str.format(query_append), location_id, user_id, *params)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_linestring_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_linestring_partial_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_linestring_element(
        request: Request,
        user_id: object = None,
        nvl_linestring_id: int = 0) -> dict:
    """ Delete nvl_linestring element by nvl_linestring id.

    :param request:
    :param nvl_linestring_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_linestring_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, nvl_linestring_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_linestring_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_linestring_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Delete nvl_point element by location id.

    :param request:
    :param location_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_linestring_element_by_location_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_linestring_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


# NVL CIRCLE SERVICES
async def get_nvl_circle_list(
        request: Request,
        user_id: object = None,
        label=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get nvl_circle list ordered by nvl_circle id desc.

    :param request:
    :param label:
    :param limit:
    :param user_id:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_nvl_circle_list_query

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
            if limit > 0:
                query_str += ' ORDER BY ncr.id DESC LIMIT $3 OFFSET $4;'
                rows = await connection.fetch(query_str, user_id, label, limit, offset)
            else:
                query_str += ' ORDER BY ncr.id DESC;'
                rows = await connection.fetch(query_str, user_id, label)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('nvl_circle service erred with: {}'.format(gclerr))

    return ret_val


async def get_nvl_circle_list_count(
        request: Request,
        user_id: object = None,
        label=None) -> int:
    """ Get nvl_circle list count.

    :param request:
    :param user_id:
    :param label:
    :return:
    """

    ret_val = 0
    query_str = get_nvl_circle_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, label)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_nvl_circle_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_circle_element(
        request: Request,
        user_id: object = None,
        nvl_circle_id: int = 0) -> dict:
    """ Get nvl_circle element by nvl_circle id.

    :param request:
    :param nvl_circle_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_circle_element_query
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
            row = await connection.fetchrow(query_str, user_id, nvl_circle_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_nvl_circle_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_circle_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Get nvl_circle element by nvl_circle id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_circle_element_by_location_id_query
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
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_nvl_circle_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_circle_feature_list_by_user_id(
        request: Request,
        user_id: object = None) -> list:
    """ Get all linestring with show on map set to true for user.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = []
    query_str = get_nvl_circle_list_by_user_id_query
    try:
        # print(user_id)
        # print('HMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')
        async with request.app.pg.acquire() as connection:

            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            await connection.set_type_codec(
                'numeric', encoder=str, decoder=float,
                schema='pg_catalog', format='text'
            )
            rows = await connection.fetch(query_str, user_id)
            # print('MMMMMHHHH: {}'.format(rows))
            if rows is not None:

                ret_val = [Feature(
                    geometry=x.get('geom'),
                    properties={
                        'label': x.get('label'),
                        'color': x.get('color'),
                        'radius': x.get('radius'),
                        'id': x.get('location_id'),
                        'name': x.get('location_name')
                    }) for x in rows]
    except Exception as gclcerr:
        logger.error('get_nvl_circle_feature_list_by_user_id service erred with: {}'.format(gclcerr))

    return ret_val


async def create_nvl_circle_element(
        request: Request,
        user_id: object = None,
        geom: object = None,
        radius: Decimal = Decimal('0.0'),
        location_id: object = None,
        label: str = '', color: str = '',
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Create nvl_circle element

    :param request:
    :param geom:
    :param radius:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_nvl_circle_element_query
    try:
        print('create circle ', user_id, geom, radius, location_id, label, color, meta_information, active)
        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            row = await connection.fetchrow(
                query_str, user_id, Point((x.get('lng'), x.get('lat')) for x in geom), label, color,
                location_id, radius, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_circle_element(request, user_id=user_id, nvl_circle_id=dta.get('id'))
    except Exception as gclcerr:
        logger.error('create_nvl_circle_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_circle_element(
        request: Request,
        circle_id: object = None,
        user_id: object = None,
        geom: object = None,
        radius: Decimal = Decimal('0.0'),
        location_id: object = None,
        label: str = '', color: str = '',
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Update nvl_circle element

    :param request:
    :param circle_id:
    :param geom:
    :param radius:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_circle_element_query
    try:
        print('update circle ', user_id, geom, radius, location_id, label, color, meta_information, active)
        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            row = await connection.fetchrow(
                query_str, circle_id, user_id,
                Point((x.get('lng'), x.get('lat')) for x in geom), label, color,
                location_id, radius, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_circle_element(request, user_id=user_id, nvl_circle_id=dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_circle_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_circle_partial_element(
        request: Request,
        location_id: object = None,
        user_id: object = None,
        label: str = '',
        color: str = '',
        active: bool = True) -> dict:
    """ Update nvl_circle element by nvl_circle id.

    :param request:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_circle_element_partial_query
    query_append = ''
    params = []
    param_count = 3

    try:
        if label != '':
            query_append += 'label = ${}::VARCHAR,'.format(param_count)
            params.append(label)
            param_count += 1

        if color != '':
            query_append += 'color = ${}::VARCHAR,'.format(param_count)
            params.append(color)
            param_count += 1

        if active is not None:
            query_append += 'active = ${}::BOOLEAN,'.format(param_count)
            params.append(active)
            param_count += 1

        # print(query_str.format(query_append))
        # print(location_id, user_id, *params)
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str.format(query_append), location_id, user_id, *params)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_circle_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_circle_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_circle_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Delete nvl_circle element by location id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_circle_element_by_location_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_circle_element(request, user_id=user_id, nvl_circle_id=dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_circle_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_circle_element(
        request: Request,
        user_id: object = None,
        nvl_circle_id: int = 0) -> dict:
    """ Delete nvl_circle element by nvl_circle id.

    :param request:
    :param nvl_circle_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_circle_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, nvl_circle_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, user_id, dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_circle_element service erred with: {}'.format(gclcerr))

    return ret_val


# NVL POLYGON SERVICES
async def get_nvl_polygon_list(
        request: Request,
        user_id: object = None,
        label=None, limit: int = 0,
        offset: int = 0) -> list:
    """ Get nvl_polygon list ordered by nvl_polygon id desc.

    :param request:
    :param label:
    :param user_id:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_nvl_polygon_list_query

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
            if limit > 0:
                query_str += ' ORDER BY npg.id DESC LIMIT $3 OFFSET $4;'
                rows = await connection.fetch(query_str, user_id, label, limit, offset)
            else:
                query_str += ' ORDER BY npg.id DESC;'
                rows = await connection.fetch(query_str, user_id, label)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('nvl_polygon service erred with: {}'.format(gclerr))

    return ret_val


async def get_nvl_polygon_list_count(
        request: Request,
        user_id: object = None,
        label=None) -> int:
    """ Get nvl_polygon list count.

    :param request:
    :param label:
    :param user_id:
    :return:
    """

    ret_val = 0
    query_str = get_nvl_polygon_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, label)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_nvl_polygon_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_polygon_element(
        request: Request,
        user_id: object = None,
        nvl_polygon_id: int = 0) -> dict:
    """ Get nvl_polygon element by nvl_polygon id.

    :param request:
    :param nvl_polygon_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_polygon_element_query
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
            row = await connection.fetchrow(query_str, user_id, nvl_polygon_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_nvl_polygon_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_polygon_feature_list_by_user_id(
        request: Request,
        user_id: object = None) -> list:
    """ Get all polygon with show on map set to true for user.

    :param request:
    :param user_id:
    :return:
    """

    ret_val = []
    query_str = get_nvl_polygon_list_by_user_id_query
    try:

        async with request.app.pg.acquire() as connection:

            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )
            rows = await connection.fetch(query_str, user_id)
            if rows is not None:
                ret_val = [Feature(
                    geometry=x.get('geom'),
                    properties={
                        'label': x.get('label'),
                        'color': x.get('color'),
                        'id': x.get('location_id'),
                        'name': x.get('location_name')
                    }) for x in rows]
    except Exception as gclcerr:
        logger.error('get_nvl_polygon_feature_list_by_user_id service erred with: {}'.format(gclcerr))

    return ret_val


async def get_nvl_polygon_element_by_location_id(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Get nvl_polygon element by nvl_polygon id.

    :param request:
    :param location_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_nvl_polygon_element_by_location_id_query
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
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_nvl_polygon_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val


async def create_nvl_polygon_element(
        request: Request,
        user_id: object = None,
        geom: object = None,
        label: str = '',
        color: str = '',
        location_id: object = None,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Create nvl_polygon element

    :param request:
    :param geom:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_nvl_polygon_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )

            row = await connection.fetchrow(
                query_str, user_id, Polygon([(x.get('lng'), x.get('lat')) for x in geom]), label, color,
                location_id, ujson.dumps(meta_information), active)
            # print('THIS IS THE POLY : {}'.format(row))

            if row is not None:
                dta = dict(row)
                # print('THIS IS DICT ROW: {}'.format(dta))
                if dta:
                    ret_val = await get_nvl_polygon_element(request, user_id=user_id, nvl_polygon_id=dta.get('id'))
                    # print('THIS IS RETVAL POLY {}'.format(ret_val))
    except Exception as gclcerr:
        logger.error('create_nvl_polygon_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_polygon_element(
        request: Request,
        polygon_id: object = None,
        user_id: object = None,
        geom: object = None,
        label: str = '',
        color: str = '',
        location_id: object = None,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Create nvl_polygon element

    :param request:
    :param polygon_id:
    :param geom:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_polygon_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'geometry',
                encoder=encode_geometry,
                decoder=decode_geometry,
                format='binary',
            )

            row = await connection.fetchrow(
                query_str, polygon_id, user_id,
                Polygon([(x.get('lng'), x.get('lat')) for x in geom]), label, color,
                location_id, ujson.dumps(meta_information), active)

            if row is not None:
                dta = dict(row)
                # print('THIS IS DICT ROW: {}'.format(dta))
                if dta:
                    ret_val = await get_nvl_polygon_element(request, user_id=user_id, nvl_polygon_id=dta.get('id'))
                    # print('THIS IS RETVAL POLY {}'.format(ret_val))
    except Exception as gclcerr:
        logger.error('update_nvl_polygon_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_nvl_polygon_partial_element(
        request: Request,
        location_id: object = None,
        user_id: object = None,
        label: str = '',
        color: str = '',
        active: bool = True) -> dict:
    """ Update nvl_polygon element by nvl_polygon id.

    :param request:
    :param label:
    :param color:
    :param location_id:
    :param user_id:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_nvl_polygon_element_query
    query_append = ''
    params = []
    param_count = 3

    try:

        if label != '':
            query_append += 'label = ${}::VARCHAR,'.format(param_count)
            params.append(label)
            param_count += 1

        if color != '':
            query_append += 'color = ${}::VARCHAR,'.format(param_count)
            params.append(color)
            param_count += 1

        if active is not None:
            query_append += 'active = ${}::BOOLEAN,'.format(param_count)
            params.append(active)
            param_count += 1

        # print(query_str.format(query_append))
        # print(location_id, user_id, *params, active)
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str.format(query_append), location_id, user_id, *params)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('update_nvl_polygon_partial_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_polygon_element(
        request: Request,
        user_id: object = None,
        nvl_polygon_id: int = 0) -> dict:
    """ Delete nvl_polygon element by nvl_polygon id.

    :param request:
    :param user_id:
    :param nvl_polygon_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_polygon_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, nvl_polygon_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, user_id=user_id, nvl_polygon_id=dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_polygon_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_nvl_polygon_element_by_location_id(
        request: Request,
        user_id: int = 0,
        location_id: int = 0) -> dict:
    """ Delete nvl_polygon element by location id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = delete_nvl_polygon_element_by_location_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, location_id)
            if row is not None:
                dta = dict(row)
                if dta:
                    ret_val = await get_nvl_polygon_element(request, dta.get('id'))
    except Exception as gclcerr:
        logger.error('delete_nvl_polygon_element_by_location_id service erred with: {}'.format(gclcerr))

    return ret_val
