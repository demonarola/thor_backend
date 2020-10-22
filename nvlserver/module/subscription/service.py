#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
import ujson
from decimal import Decimal
from sanic.log import logger
from sanic.request import Request

# SUBSCRIPTION IMPORTS
from .specification.get_subscription_specification import (
    get_subscription_list_query, get_subscription_list_count_query, get_subscription_element_query
)
from .specification.create_subscription_specification import create_subscription_element_query
from .specification.update_subscription_specification import update_subscription_element_query
from .specification.delete_subscription_specification import delete_subscription_element_query

# SUBSCRIPTION MODEL IMPORTS
from .specification.get_subscription_model_specification import (
    get_subscription_model_list_query, get_subscription_model_list_count_query, get_subscription_model_element_query,
    get_subscription_model_list_dropdown_query
)
from .specification.create_subscription_model_specification import create_subscription_model_element_query
from .specification.update_subscription_model_specification import update_subscription_model_element_query
from .specification.delete_subscription_model_specification import delete_subscription_model_element_query

# REBATE IMPORTS
from .specification.get_rebate_specification import (
    get_rebate_list_query, get_rebate_list_count_query, get_rebate_element_query, get_rebate_list_dropdown_query
)
from .specification.create_rebate_specification import create_rebate_element_query
from .specification.update_rebate_specification import update_rebate_element_query
from .specification.delete_rebate_specification import delete_rebate_element_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_subscription_list', 'get_subscription_list_count',
    'get_subscription_element', 'create_subscription_element', 'update_subscription_element',
    'delete_subscription_element', 'get_subscription_model_list', 'get_subscription_model_dropdown_list',
    'get_subscription_model_list_count', 'get_subscription_model_element', 'create_subscription_model_element',
    'update_subscription_model_element', 'delete_subscription_model_element', 'get_rebate_list',
    'get_rebate_dropdown_list', 'get_rebate_list_count', 'get_rebate_element', 'create_rebate_element',
    'update_rebate_element', 'delete_rebate_element'
]


# SUBSCRIPTION SERVICES
async def get_subscription_list(
        request: Request,
        subscription_model_id=None,
        user_id=None,
        rebate_id=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get subscription list ordered by subscription id desc.

    :param request:
    :param subscription_model_id:
    :param user_id:
    :param rebate_id:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_subscription_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY sub.id DESC LIMIT $4 OFFSET $5;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, subscription_model_id, user_id, rebate_id, limit, offset)
        else:
            query_str += ' ORDER BY sub.id DESC;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, subscription_model_id, user_id, rebate_id)

        if rows is not None:
            ret_list = []
            temp_list = [dict(x) for x in rows]
            for x in temp_list:
                x['date_from'] = x['date_from'].isoformat() if x['date_from'] is not None else ''
                x['date_to'] = x['date_to'].isoformat() if x['date_to'] is not None else ''
                ret_list.append(x)
            ret_val = ret_list

    except Exception as gclerr:
        logger.error('get_subscription_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_subscription_list_count(
        request: Request,
        subscription_model_id=None,
        user_id=None,
        rebate_id=None) -> int:
    """ Get subscription list count.

    :param request:
    :param subscription_model_id:
    :param user_id:
    :param rebate_id:
    :return:
    """

    ret_val = 0
    query_str = get_subscription_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, subscription_model_id, user_id, rebate_id)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_subscription_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_subscription_element(
        request: Request,
        subscription_id: int = 0) -> dict:
    """ Get subscription element

    :param request:
    :param subscription_id:
    :return:
    """

    ret_val = {}
    query_str = get_subscription_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, subscription_id)
            if row is not None:
                x = dict(row)
                x['date_from'] = x['date_from'].isoformat() if x['date_from'] is not None else ''
                x['date_to'] = x['date_to'].isoformat() if x['date_to'] is not None else ''
                ret_val = x
    except Exception as cleerr:
        logger.error('get_subscription_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_subscription_element(
        request: Request,
        subscription_uuid: str = '',
        user_id: object = None,
        subscription_model_id: object = None,
        rebate_id: object = None,
        meta_information: dict = {},
        unit_count: bool = False,
        date_from: object = None,
        date_to: object = None,
        active: bool = True) -> dict:
    """ Create subscription element

    :param request:
    :param subscription_uuid:
    :param user_id:
    :param subscription_model_id:
    :param rebate_id:
    :param meta_information:
    :param unit_count:
    :param date_from:
    :param date_to:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_subscription_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, subscription_uuid, user_id, subscription_model_id, rebate_id,
                ujson.dumps(meta_information), unit_count, date_from, date_to, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_subscription_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('create_subscription_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_subscription_element(
        request: Request,
        subscription_id: int = 0,
        user_id: object = None,
        subscription_model_id: object = None,
        rebate_id: object = None,
        meta_information: dict = {},
        unit_count: bool = False,
        date_from: object = None,
        date_to: object = None,
        active: bool = True) -> dict:
    """ Update subscription element

    :param request:
    :param subscription_id:
    --:param subscription_uuid:
    :param user_id:
    :param subscription_model_id:
    :param rebate_id:
    :param meta_information:
    :param unit_count:
    :param date_from:
    :param date_to:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_subscription_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, subscription_id, user_id, subscription_model_id, rebate_id,
                ujson.dumps(meta_information), unit_count, date_from, date_to, active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_subscription_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_subscription_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_subscription_element(
        request: Request,
        subscription_id: int = 0) -> dict:
    """ Delete subscription element

    :param request:
    :param subscription_id:
    :return:
    """

    ret_val = {}
    query_str = delete_subscription_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, subscription_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_subscription_element service erred with: {}'.format(cleerr))

    return ret_val


# SUBSCRIPTION MODEL SERVICES
async def get_subscription_model_list(
        request: Request,
        description=None,
        duration_month=None,
        price_per_unit=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get subscription model list

    :param request:
    :param description:
    :param duration_month:
    :param price_per_unit:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_subscription_model_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY subm.id DESC LIMIT $4 OFFSET $5;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, description, duration_month, price_per_unit, limit, offset)
        else:
            query_str += ' ORDER BY subm.id DESC;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, description, duration_month, price_per_unit)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_subscription_model_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_subscription_model_dropdown_list(
        request: Request,
        description=None) -> list:
    """ Get subscription model list ordered by subscription model id desc filtered by description.

    :param request:
    :param description:
    :return:
    """
    ret_val = []

    query_str = get_subscription_model_list_dropdown_query

    try:
        query_str += ' ORDER BY subm.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, description)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_subscription_model_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_subscription_model_list_count(
        request: Request,
        description=None,
        duration_month=None,
        price_per_unit=None,) -> int:
    """ Get subscription model list count.

    :param request:
    :param description:
    :param duration_month:
    :param price_per_unit:
    :return:
    """

    ret_val = 0
    query_str = get_subscription_model_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, description, duration_month, price_per_unit)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_subscription_model_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_subscription_model_element(
        request: Request,
        subscription_model_id: int = 0) -> dict:
    """ Get subscription model element

    :param request:
    :param subscription_model_id:
    :return:
    """

    ret_val = {}
    query_str = get_subscription_model_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, subscription_model_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_subscription_model_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_subscription_model_element(
        request: Request,
        description: str = '',
        duration_month: int = 0,
        price_per_unit: Decimal = Decimal(0),
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Create subscription model element

    :param request:
    :param description:
    :param duration_month:
    :param price_per_unit:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_subscription_model_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, description, duration_month, price_per_unit, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_subscription_model_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('create_subscription_model_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_subscription_model_element(
        request: Request,
        subscription_model_id: int = 0,
        description: str = '',
        duration_month: int = 0,
        price_per_unit: Decimal = Decimal(0),
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Update subscription model element

    :param request:
    :param subscription_model_id:
    :param description:
    :param duration_month:
    :param price_per_unit:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_subscription_model_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, subscription_model_id, description, duration_month,
                price_per_unit, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                ret_val = await get_subscription_model_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_subscription_model_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_subscription_model_element(
        request: Request,
        subscription_model_id: int = 0) -> dict:
    """ Delete subscription model element

    :param request:
    :param subscription_model_id:
    :return:
    """

    ret_val = {}
    query_str = delete_subscription_model_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, subscription_model_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_subscription_model_element service erred with: {}'.format(cleerr))

    return ret_val


# REBATE SERVICES
async def get_rebate_list(
        request: Request,
        value=None,
        rebate_is_fixed=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get rebate model list

    :param request:
    :param value:
    :param rebate_is_fixed:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_rebate_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY reb.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(
                    query_str, value, rebate_is_fixed, limit, offset)
        else:
            query_str += ' ORDER BY reb.id DESC;'
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                rows = await connection.fetch(query_str, value, rebate_is_fixed)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_rebate_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_rebate_dropdown_list(
        request: Request,
        value=None,
        rebate_is_fixed=False) -> list:
    """ Get rebate list ordered by rebate id desc.

    :param request:
    :param value:
    :param rebate_is_fixed:
    :return:
    """
    ret_val = []

    query_str = get_rebate_list_dropdown_query

    try:
        query_str += ' ORDER BY reb.id DESC;'
        async with request.app.pg.acquire() as connection:
            rows = await connection.fetch(query_str, value, rebate_is_fixed)

            if rows is not None:
                ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_rebate_dropdown_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_rebate_list_count(
        request: Request,
        value=None,
        rebate_is_fixed=None) -> int:
    """ Get rebate count

    :param request:
    :param value:
    :param rebate_is_fixed:
    :return:
    """

    ret_val = 0
    query_str = get_rebate_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, value, rebate_is_fixed)
            # print(value, rebate_is_fixed, row)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_rebate_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_rebate_element(
        request: Request,
        rebate_id: int = 0) -> dict:
    """ Get subscription model element

    :param request:
    :param rebate_id:
    :return:
    """

    ret_val = {}
    query_str = get_rebate_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, rebate_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_rebate_element service erred with: {}'.format(cleerr))

    return ret_val


async def create_rebate_element(
        request: Request,
        value: Decimal = Decimal(0),
        rebate_is_fixed: bool = False,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """  Create rebate element

    :param request:
    :param value:
    :param rebate_is_fixed:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_rebate_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, value,
                rebate_is_fixed, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                # print(dta)
                ret_val = await get_rebate_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('create_rebate_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_rebate_element(
        request: Request,
        rebate_id: int = 0,
        value: Decimal = Decimal(0),
        rebate_is_fixed: bool = False,
        meta_information: dict = {},
        active: bool = True) -> dict:
    """ Update rebate element

    :param request:
    :param rebate_id:
    :param value:
    :param rebate_is_fixed:
    :param meta_information:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_rebate_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, rebate_id, value,
                rebate_is_fixed, ujson.dumps(meta_information), active)
            if row is not None:
                dta = dict(row)
                # print(dta)
                ret_val = await get_rebate_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_rebate_element service erred with: {}'.format(cleerr))

    return ret_val


async def delete_rebate_element(
        request: Request,
        rebate_id: int = 0) -> dict:
    """ Delete rebate element

    :param request:
    :param rebate_id:
    :return:
    """

    ret_val = {}
    query_str = delete_rebate_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, rebate_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_rebate_element service erred with: {}'.format(cleerr))

    return ret_val
