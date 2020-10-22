#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from decimal import Decimal
from sanic.log import logger
from sanic.request import Request

# IMPORT HW ACTION SPECIFICATIONS
from .specification.get_hw_action_specification import (
    get_hw_action_list_query, get_hw_action_list_count_query,
    get_hw_action_element_query, get_hw_action_list_user_type_query
)
from .specification.delete_hw_action_specification import delete_hw_action_element_query
from .specification.update_hw_action_specification import update_hw_action_element_query
from .specification.create_hw_action_specification import create_hw_action_element_query


__all__ = [
    # SERVICES WORKING ON HW ACTION TABLE
    'get_hw_action_list', 'get_hw_action_list_count', 'get_hw_action_element',
    'get_hw_action_list_user_type', 'create_hw_action_element', 'update_hw_action_element',
    'delete_hw_action_element'
]


# HW ACTION SERVICES
async def get_hw_action_list(
        request: Request,
        name: object = None,
        action_type: object = None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get hw_action list ordered by hw_action id desc.

    :param request:
    :param name:
    :param action_type:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_hw_action_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY hwa.id DESC LIMIT $3 OFFSET $4;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, action_type, limit, offset)
        else:
            query_str += ' ORDER BY hwa.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, action_type)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_hw_action_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_hw_action_list_count(
        request: Request,
        name: object = None,
        action_type: object = None) -> int:
    """ Get hw_action list count.

    :param request:

    :param name:
    :param action_type:
    :return:
    """

    ret_val = 0
    query_str = get_hw_action_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name, action_type)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_hw_action_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_hw_action_element(
        request: Request,
        hw_action_id: int = 0) -> dict:
    """ Get hw_action element by hw_action id.

    :param request:
    :param hw_action_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, hw_action_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val


async def get_hw_action_list_user_type(
        request: Request) -> list:
    """ Get all hw actions with user_type

    :param request:
    :return:
    """

    ret_val = {}
    query_str = get_hw_action_list_user_type_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            rows = await connection.fetch(query_str)
            if rows is not None:
                ret_val = [dict(x) for x in rows]
                print(30 * '-')
                print('get_hw_action_list_user_type_query')
                print(ret_val)
    except Exception as gclcerr:
        logger.error('get_hw_action_list_user_type service erred with: {}'.format(gclcerr))

    return ret_val


async def create_hw_action_element(
        request: Request,
        name: str = '',
        proto_field: str = '',
        meta_information: dict = {},
        min_value: Decimal = Decimal('0.0'),
        max_value: Decimal = Decimal('100.0'),
        active: bool = True) -> dict:
    """ Create hw_action element

    :param request:
    :param name:
    :param proto_field:
    :param meta_information:
    :param min_value:
    :param max_value:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, name, proto_field, ujson.dumps(meta_information),
                min_value, max_value, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('create_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_hw_action_element(
        request: Request,
        hw_action_id: int = 0,
        name: str = '',
        proto_field: str = '',
        meta_information: dict = {},
        min_value: Decimal = Decimal('0.0'),
        max_value: Decimal = Decimal('100.0'),
        active: bool = True) -> dict:
    """ Update read status on hw_action element by hw_action id.

    :param request:
    :param hw_action_id:
    :param name:
    :param proto_field:
    :param meta_information:
    :param min_value:
    :param max_value:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_action_id, name,
                proto_field,
                ujson.dumps(meta_information),
                min_value, max_value, active)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('update_hw_action_element_read service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_hw_action_element(
        request: Request,
        hw_action_id: int = 0) -> dict:
    """ Delete hw_action element by hw_action id.

    :param request:
    :param hw_action_id:
    :return:
    """

    ret_val = {}
    query_str = delete_hw_action_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, hw_action_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_hw_action_element service erred with: {}'.format(gclcerr))

    return ret_val
