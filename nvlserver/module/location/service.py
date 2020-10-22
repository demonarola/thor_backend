#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import asyncio
import ujson

from decimal import Decimal
from sanic.log import logger
from sanic.request import Request

# IMPORT LOCATION SPECIFICATIONS
from .specification.get_location_specification import (
    get_location_list_query, get_location_list_count_query,
    get_location_element_query
)
from .specification.delete_location_specification import delete_location_element_query
from .specification.update_location_specification import update_location_element_query
from .specification.create_location_specification import create_location_element_query

# IMPORT LOCATION TYPE SPECIFICATIONS
from .specification.get_location_type_specification import (
    get_location_type_list_query, get_location_type_list_count_query,
    get_location_type_element_query, get_location_type_list_dropdown_query,
    get_location_type_element_by_name_query
)
from .specification.delete_location_type_specification import delete_location_type_element_query
from .specification.update_location_type_specification import update_location_type_element_query
from .specification.create_location_type_specification import create_location_type_element_query

from web_backend.nvlserver.module.nvl_cartography.service import (
    get_nvl_polygon_element_by_location_id, get_nvl_linestring_element_by_location_id,
    get_nvl_point_element_by_location_id, get_nvl_circle_element_by_location_id,
    delete_nvl_circle_element_by_location_id, delete_nvl_linestring_element_by_location_id,
    delete_nvl_point_element_by_location_id, delete_nvl_polygon_element_by_location_id,
    create_nvl_circle_element, create_nvl_linestring_element,
    create_nvl_polygon_element, create_nvl_point_element,
    get_nvl_polygon_feature_list_by_user_id, get_nvl_point_feature_list_by_user_id,
    get_nvl_circle_feature_list_by_user_id, get_nvl_linestring_feature_list_by_user_id,
    update_nvl_polygon_element, update_nvl_circle_partial_element, update_nvl_linestring_partial_element,
    update_nvl_point_partial_element
)

from web_backend.nvlserver.module.user_hw_action.service import (
    update_user_hw_action_location_element, create_user_hw_action_element, get_user_hw_action_list_by_location_id,
    delete_user_hw_action_list_by_location_id, get_user_hw_action_times_by_location_id
)


__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_location_list', 'get_location_geography_list', 'get_location_list_count',
    'get_location_element', 'create_location_element', 'update_location_element',
    'delete_location_element', 'get_location_type_list', 'get_location_type_dropdown_list',
    'get_location_type_list_count', 'get_location_type_element', 'get_location_type_element_by_name',
    'create_location_type_element', 'update_location_type_element', 'delete_location_type_element',
    'process_location_action_list', 'process_location_point', 'process_location_linestring',
    'process_location_circle', 'process_location_polygon', 'process_location_geo_feature'
]


# LOCATION SERVICES
async def get_location_list(
        request: Request,
        name=None,
        user_id=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get location list ordered by location id desc.

    :param request:
    :param name:
    :param user_id:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_location_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY loc.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, user_id, limit, offset)

        else:
            query_str += ' ORDER BY loc.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, user_id)

        ret_val = [dict(x) for x in rows]
    except Exception as gclerr:
        logger.error('get_location_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_location_geography_list(
        request: Request,
        user_id=None) -> list:
    """ Get location list ordered by location id desc.

    :param request:
    :param user_id:
    :return:
    """
    ret_val = []

    try:

        transcribed_list = []

        data = await asyncio.gather(
            get_nvl_polygon_feature_list_by_user_id(request, user_id=user_id),
            get_nvl_point_feature_list_by_user_id(request, user_id=user_id),
            get_nvl_circle_feature_list_by_user_id(request, user_id=user_id),
            get_nvl_linestring_feature_list_by_user_id(request, user_id=user_id)
        )

        for x in data:
            if len(x) > 0:
                for y in x:
                    transcribed_list.append(y)

        ret_val = transcribed_list

    except Exception as gclerr:
        logger.error('get_location_geography_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_location_list_count(
        request: Request,
        name=None,
        user_id=None) -> int:
    """ Get location list count.

    :param request:
    :param user_id:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_location_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name, user_id)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_location_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_location_element(
        request: Request,
        user_id: object = None,
        location_id: int = 0) -> dict:
    """ Get location element by location id.

    :param request:
    :param location_id:
    :param user_id:
    :return:
    """

    ret_val = {}
    query_str = get_location_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, user_id, location_id)

        if row is not None:
            x = dict(row)
            # print('get_location_element: {}'.format(x))
            if x.get('location_type') == 'polygon':
                geo_element = await get_nvl_polygon_element_by_location_id(
                    request, user_id=user_id, location_id=x.get('id'))
                if geo_element:
                    coords_lst = geo_element.get('geom').get('coordinates')
                    if len(coords_lst) > 0:
                        coords = coords_lst[0]
                        # print('THEZEN ARE CORDINATEN: {}'.format(coords))
                        crd_dec = [{'lat': x[0], 'lng': x[1]} for x in coords]
                        x.update(
                            {
                                'coordinates': crd_dec,
                                'label': geo_element.get('label'),
                                'color': geo_element.get('color')
                            })
                action_times = await get_user_hw_action_times_by_location_id(
                    request, location_id=location_id)

                if action_times:
                    x.update(
                        {
                            'date_from': action_times.get('min_date'),
                            'date_to': action_times.get('max_date')
                        }
                    )
                action_list = await get_user_hw_action_list_by_location_id(
                    request, user_id=user_id, location_id=location_id)

                if action_list:
                    x.update({'action': action_list})
                else:
                    x.update({'action': []})

            if x.get('location_type') == 'point':
                geo_element = await get_nvl_point_element_by_location_id(
                    request, user_id=user_id, location_id=x.get('id'))
                if geo_element:
                    coords = geo_element.get('geom').get('coordinates')
                    crd_dec = {'lat': coords[0], 'lng': coords[1]}
                    x.update(
                        {
                            'coordinates': [crd_dec],
                            'label': geo_element.get('label'),
                            'color': geo_element.get('color'),
                            'icon': geo_element.get('icon')
                        })
            if x.get('location_type') == 'circle':
                geo_element = await get_nvl_circle_element_by_location_id(
                    request, user_id=user_id, location_id=x.get('id'))
                # print(geo_element)

                if geo_element:
                    coords = geo_element.get('geom').get('coordinates')
                    crd_dec = {'lat': coords[0], 'lng': coords[1]}
                    x.update(
                        {
                            'coordinates': [crd_dec],
                            'label': geo_element.get('label'),
                            'color': geo_element.get('color'),
                            'radius': geo_element.get('radius')
                        })

                action_times = await get_user_hw_action_times_by_location_id(
                    request, location_id=location_id)

                if action_times:
                    x.update(
                        {
                            'date_from': action_times.get('min_date'),
                            'date_to': action_times.get('max_date')
                        }
                    )
                action_list = await get_user_hw_action_list_by_location_id(
                    request, user_id=user_id, location_id=location_id)
                if action_list:
                    x.update({'action': action_list})
                else:
                    x.update({'action': []})

            if x.get('location_type') == 'linestring':
                geo_element = await get_nvl_linestring_element_by_location_id(
                    request, user_id=user_id, location_id=x.get('id'))
                if geo_element:
                    coords = geo_element.get('geom').get('coordinates')
                    # print(coords)
                    crd_dec = [{'lat': x[0], 'lng': x[1]} for x in coords]
                    x.update(
                        {
                            'coordinates': crd_dec,
                            'label': geo_element.get('label'),
                            'color': geo_element.get('color')
                        })

            ret_val = x

    except Exception as gclcerr:
        logger.error('get_location_element service erred with: {}'.format(gclcerr))

    return ret_val


async def create_location_element(
        request: Request,
        name: str = '',
        location_type_id: object = None,
        user_id: object = None,
        meta_information=None,
        show_on_map: bool = True,
        active: bool = True) -> dict:
    """ Create location element

    :param request:
    :param name:
    :param location_type_id:
    :param user_id:
    :param meta_information:
    :param show_on_map:
    :param active:
    :return:
    """

    if meta_information is None:
        meta_information = {'modules': []}
    ret_val = {}
    query_str = create_location_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, name, location_type_id, user_id, ujson.dumps(meta_information), show_on_map, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('create_location_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_location_element(
        request: Request,
        location_id: int = 0,
        name: str = '',
        location_type_id: object = None,
        user_id: object = None,
        meta_information=None,
        show_on_map: bool = True,
        active: bool = True) -> dict:
    """ Update read status on location element by location id.

    :param request:
    :param location_id:
    :param name:
    :param location_type_id:
    :param user_id:
    :param meta_information:
    :param show_on_map:
    :param active:
    :return:
    """

    if meta_information is None:
        meta_information = {}
    ret_val = {}
    query_str = update_location_element_query
    try:
        print('update_location_element variables')
        print(location_id, name, location_type_id, user_id, meta_information, show_on_map, active)
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, location_id, name, location_type_id, user_id,
                ujson.dumps(meta_information), show_on_map, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('update_location_element_read service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_location_element(
        request: Request,
        user_id: int = 0,
        location_id: int = 0) -> dict:
    """ Delete location element by location id.

    :param request:
    :param user_id:
    :param location_id:
    :return:
    """

    ret_val = {}
    query_str = delete_location_element_query
    # print('DELETED CALLED: {}, {}'.format(user_id, location_id))
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, user_id, location_id)
            # print('THIS IS ROW: {}'.format(row))
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_location_element service erred with: {}'.format(gclcerr))

    return ret_val


# LOCATION TYPE SERVICES
async def get_location_type_list(
        request: Request,
        name=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get location_type list ordered by location_type id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_location_type_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY ltp.id DESC LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY ltp.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_location_type_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_location_type_dropdown_list(
        request: Request,
        name=None) -> list:
    """ Get location_type dropdown list ordered by location_type id desc.

    :param request:
    :param name:
    :return:
    """
    ret_val = []

    query_str = get_location_type_list_dropdown_query

    try:
        query_str += ' ORDER BY ltp.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, name)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_location_type_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_location_type_list_count(
        request: Request,
        name=None) -> int:
    """ Get location_type list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_location_type_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_location_type_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_location_type_element(
        request: Request,
        location_type_id: int = 0) -> dict:
    """ Get location_type element by location id.

    :param request:
    :param location_type_id:
    :return:
    """

    ret_val = {}
    query_str = get_location_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, location_type_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_location_type_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_location_type_element_by_name(
        request: Request,
        location_type_name: str = '') -> dict:
    """ Get location_type element by location name.

    :param request:
    :param location_type_name:
    :return:
    """

    ret_val = {}
    query_str = get_location_type_element_by_name_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, location_type_name)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_location_type_element_by_name service erred with: {}'.format(gclcerr))

    return ret_val


async def create_location_type_element(
        request: Request,
        name: str = '',
        active: bool = True) -> dict:
    """  Create location type element

    :param request:
    :param name:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_location_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, name, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('create_location_type_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_location_type_element(
        request: Request,
        location_type_id: int = 0,
        name: str = '',
        active: bool = True) -> dict:
    """ Update location_type element

    :param request:
    :param location_type_id:
    :param name:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_location_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, location_type_id, name, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('update_location_type_element service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_location_type_element(
        request: Request,
        location_type_id: int = 0) -> dict:
    """ Delete location_type element by location id.

    :param request:
    :param location_type_id:
    :return:
    """

    ret_val = {}
    query_str = delete_location_type_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, location_type_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_location_type_element service erred with: {}'.format(gclcerr))

    return ret_val


# PROCESS LOCATION ELEMENTS
async def process_location_action_list(
        request: Request,
        user_id: int = 0,
        location_id: int = 0,
        date_from: object = None,
        date_to: object = None,
        action_list=None) -> bool:
    """ Process action list for module list

    :param request:
    :param user_id:
    :param location_id:
    :param date_from:
    :param date_to:
    :param action_list:
    :return:
    """

    try:

        if action_list is None:
            print('ACTION LIST IS NONE')
            action_list = []
            print('delete_user_hw_action_list_by_location_id CALLED')
            await delete_user_hw_action_list_by_location_id(
                request, user_id=user_id, location_id=location_id)
        if action_list is not None:
            print('ACTION LIST IS NOT NONE')
            print('delete_user_hw_action_list_by_location_id CALLED')
            await delete_user_hw_action_list_by_location_id(
                request, user_id=user_id, location_id=location_id)

            for action in action_list:
                print('---------------THIS IS ACTION ----------------------')
                print('----------------{}'.format(action))

                user_hw_action = await create_user_hw_action_element(
                    request, user_id=user_id, hw_action_id=action.get('hw_action_id'),
                    value=str(action.get('value')), date_from=date_from, date_to=date_to, active=True)
                print('THIS IS USER HW ACTION: {}'.format(user_hw_action))
                if user_hw_action:
                    print('update_user_hw_action_location_element called: {} {}'.format(
                        user_hw_action.get('id'), location_id))
                    await update_user_hw_action_location_element(
                        request, user_hw_action_id=user_hw_action.get('id'), location_id=location_id)
        ret_val = True
    except Exception as plal_err:
        logger.error('process_location_action_list service erred with: {}'.format(plal_err))
        ret_val = False

    return ret_val


async def process_location_point(
        request: Request,
        location_id: int = 0,
        label: str = '',
        coordinates: list = [],
        icon: str = '',
        color: str = '',
        user_id: int = 0) -> dict:
    """

    :param request:
    :param location_id:
    :param label:
    :param coordinates:
    :param icon:
    :param color:
    :param user_id:
    :return:
    """
    ret_val = {}
    try:
        print(location_id, label, coordinates, icon, color, user_id)
        if len(coordinates) == 0:
            ret_val = await update_nvl_point_partial_element(
                request, location_id=location_id, user_id=user_id,
                label=label, color=color, icon=icon, active=True)
        else:
            await delete_nvl_point_element_by_location_id(request, location_id=location_id)
            ret_val = await create_nvl_point_element(
                request=request, geom=coordinates,
                label=label, color=color, icon=icon, location_id=location_id,
                user_id=user_id, active=True)

    except Exception as al_err:
        logger.error('Function process_location_point erred with: {}'.format(al_err))

    return ret_val


async def process_location_linestring(
        request: Request,
        location_id: int = 0,
        label: str = '',
        coordinates: list = [],
        color: str = '',
        user_id: int = 0) -> dict:
    """

    :param request:
    :param location_id:
    :param label:
    :param coordinates:
    :param color:
    :param user_id:
    :return:
    """

    ret_val = {}
    try:
        if len(coordinates) == 0:
            ret_val = await update_nvl_linestring_partial_element(
                request, location_id=location_id, user_id=user_id,
                label=label, color=color, active=True)
        else:
            await delete_nvl_linestring_element_by_location_id(request, location_id=location_id)
            ret_val = await create_nvl_linestring_element(
                request=request, geom=coordinates,
                label=label, color=color, location_id=location_id,
                user_id=user_id, active=True)
    except Exception as al_err:
        logger.error('Function process_location_linestring erred with: {}'.format(al_err))

    return ret_val


async def process_location_circle(
        request: Request,
        location_id: int = 0,
        label: str = '',
        coordinates: list = [],
        color: str = '',
        radius: Decimal = Decimal('0.0'),
        user_id: int = 0) -> dict:
    """

    :param request:
    :param location_id:
    :param label:
    :param coordinates:
    :param color:
    :param radius:
    :param user_id:
    :return:
    """

    ret_val = {}

    try:
        if len(coordinates) == 0:
            ret_val = await update_nvl_circle_partial_element(
                request, location_id=location_id, user_id=user_id,
                label=label, color=color, active=True)
        else:
            # print('JEBO IM JA MAMU')
            await delete_nvl_circle_element_by_location_id(request, user_id=user_id, location_id=location_id)
            # print(request, coordinates, label, color, radius, location_id, user_id, True)
            ret_val = await create_nvl_circle_element(
                request, user_id=user_id,
                geom=coordinates, radius=radius, location_id=location_id,
                label=label, color=color, meta_information={},
                active=True
            )

    except Exception as al_err:
        logger.error('Function process_location_circle erred with: {}'.format(al_err))

    return ret_val


async def process_location_polygon(
        request: Request,
        location_id: int = 0,
        label: str = '',
        coordinates: list = [],
        color: str = '',
        user_id: int = 0) -> dict:
    """

    :param request:
    :param location_id:
    :param label:
    :param coordinates:
    :param color:
    :param user_id:
    :return:
    """

    ret_val = {}
    try:
        print('process_location_polygon')
        print(location_id, label, coordinates, color, user_id)
        if len(coordinates) == 0:
            print('update_nvl_polygon_element called')
            ret_val = await update_nvl_polygon_element(
                request, location_id=location_id, user_id=user_id,
                label=label, color=color, active=True)
        else:
            print('delete_nvl_polygon_element_by_location_id called')
            await delete_nvl_polygon_element_by_location_id(request, user_id=user_id, location_id=location_id)
            # print(request, coordinates, label, color, location_id, user_id, True)
            ret_val = await create_nvl_polygon_element(
                request=request, geom=coordinates,
                label=label, color=color, location_id=location_id,
                user_id=user_id, active=True)

    except Exception as al_err:
        logger.error('Function process_location_polygon erred with: {}'.format(al_err))

    return ret_val


async def process_location_geo_feature(
        request: Request,
        location_element: dict = {},
        label: str = '',
        coordinates: list = [],
        icon: str = '',
        color: str = '',
        radius: Decimal = Decimal('0.0'),
        date_from: object = None,
        date_to: object = None,
        action_list: list = []) -> bool:
    """ Process location type geo feature and actions if exist.

    :param request:
    :param label:
    :param coordinates:
    :param icon:
    :param color:
    :param location_element:
    :param radius:
    :param date_from:
    :param date_to:
    :param action_list:

    :return:
    """

    try:
        print('process_location_geo_feature')
        print(
            location_element, label, coordinates, icon,
            color, radius, date_from, date_to, action_list)
        location_type = await get_location_type_element(request, location_element.get('location_type_id'))

        if location_type.get('name', None) == 'point':
            await process_location_point(
                request, user_id=location_element.get('user_id', 0), location_id=location_element.get('id'),
                label=label, coordinates=coordinates, icon=icon, color=color)

        elif location_type.get('name', None) == 'linestring':
            await process_location_linestring(
                request, user_id=location_element.get('user_id', 0),
                location_id=location_element.get('id'), label=label,
                coordinates=coordinates, color=color)

        elif location_type.get('name', None) == 'circle':
            await process_location_circle(
                request, user_id=location_element.get('user_id', 0),
                location_id=location_element.get('id'), label=label,
                coordinates=coordinates, color=color, radius=radius)

            await process_location_action_list(
                request, user_id=location_element.get('user_id', 0), location_id=location_element.get('id'),
                date_from=date_from, date_to=date_to, action_list=action_list)

        elif location_type.get('name', None) == 'polygon':
            print('PROCESS LOCATION POLYGON CALLED')
            await process_location_polygon(
                request, user_id=location_element.get('user_id', 0), location_id=location_element.get('id'),
                label=label, coordinates=coordinates, color=color)
            print('PROCESS LOCATION ACTION LIST CALLED')
            await process_location_action_list(
                request, user_id=location_element.get('user_id', 0), location_id=location_element.get('id'),
                date_from=date_from, date_to=date_to, action_list=action_list)

        ret_val = True
    except Exception as plgf_eerr:
        ret_val = False
        logger.error('Exception occurred on process_location_geo_feature erred with : {}'.format(plgf_eerr))

    return ret_val
