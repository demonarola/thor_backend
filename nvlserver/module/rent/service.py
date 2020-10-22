#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_rent_specification import (
    get_rent_list_query, get_rent_list_count_query,
    get_rent_element_query
)
from .specification.delete_rent_specification import delete_rent_element_query
from .specification.update_rent_specification import update_rent_element_query
from .specification.create_rent_specification import create_rent_element_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_rent_list', 'get_rent_list_count', 'get_rent_element',
    'create_rent_element', 'update_rent_element', 'delete_rent_element'
]


async def get_rent_list(
        request: Request,
        user_id: int = 0,
        date_from: object = None,
        date_to: object = None,
        limit: int = 0,
        offset: int = 0) -> list:
    """Get rent list ordered by rent id desc.

    :param request:
    :param user_id:
    :param limit:
    :param offset:
    :param date_from:
    :param date_to:
    :return:
    """

    ret_val = []

    query_str = get_rent_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY rnt.date_to DESC LIMIT $4 OFFSET $5;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(
                    query_str, user_id, date_from, date_to, limit, offset)
        else:
            query_str += ' ORDER BY rnt.date_to DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, user_id, date_from, date_to)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_rent_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_rent_list_count(
        request: Request,
        user_id: int = 0,
        date_from: object = None,
        date_to: object = None) -> int:
    """ Get rent list count.

    :param request:
    :param user_id:
    :param date_from:
    :param date_to:
    :return:
    """

    ret_val = 0
    query_str = get_rent_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, date_from, date_to)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_rent_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_rent_element(
        request: Request,
        rent_id: int = 0) -> dict:
    """ Get rent element by rent id.

    :param request:
    :param rent_id:
    :return:
    """

    ret_val = {}
    query_str = get_rent_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, rent_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_rent_element service erred with: {}'.format(gclcerr))

    return ret_val


async def create_rent_element(
        request: Request,
        user_id: object = None,
        hw_action_id: object = None,
        proto_field: str = '',
        field_type: str = '',
        value: str = '',
        state: str = 'pending',
        traceable_object_id: int = 0,
        hw_module_id: int = 0,
        ack_message: bool = True,
        date_from: str = '',
        date_to: str = '',
        active: bool = True) -> dict:
    """ Create rent element

    :param request:
    :param user_id:
    :param hw_action_id:
    :param proto_field:
    :param field_type:
    :param value:
    :param state:
    :param traceable_object_id:
    :param hw_module_id:
    :param ack_message:
    :param date_from:
    :param date_to:
    :param active:
    :return:
    """
    ret_val = []

    query_str = create_rent_element_query

    try:
        async with request.app.pg.acquire() as connection:
            # print(
            #     user_id, hw_action_id, proto_field, field_type, value,
            #     state, traceable_object_id, hw_module_id, ack_message, date_from, date_to, active)
            row = await connection.fetchrow(
                query_str, user_id, hw_action_id, proto_field, field_type, value,
                state, traceable_object_id, hw_module_id, ack_message, date_from, date_to, active)

            if row is not None:
                ret_val = dict(row)

    except Exception as gclerr:
        logger.error('create_rent_element service erred with: {}'.format(gclerr))

    return ret_val


async def update_rent_element(
        request: Request,
        rent_id: object = None,
        user_id: object = None,
        hw_action_id: object = None,
        proto_field: str = '',
        field_type: str = '',
        value: str = '',
        state: str = 'pending',
        traceable_object_id: int = 0,
        hw_module_id: int = 0,
        ack_message: bool = True,
        date_from: str = '',
        date_to: str = '',
        active: bool = True) -> dict:
    """ Update rent element

    :param request:
    :param rent_id:
    :param user_id:
    :param hw_action_id:
    :param proto_field:
    :param field_type:
    :param value:
    :param state:
    :param traceable_object_id:
    :param hw_module_id:
    :param ack_message:
    :param date_from:
    :param date_to:
    :param active:
    :return:
    """
    ret_val = []

    query_str = update_rent_element_query

    try:
        async with request.app.pg.acquire() as connection:

            row = await connection.fetchrow(
                query_str, rent_id, user_id, hw_action_id, proto_field, field_type, value,
                state, traceable_object_id, hw_module_id, ack_message, date_from, date_to, active)

            if row is not None:
                ret_val = dict(row)

    except Exception as gclerr:
        logger.error('update_rent_element service erred with: {}'.format(gclerr))

    return ret_val


async def delete_rent_element(
        request: Request,
        rent_id: int = 0) -> dict:
    """ Delete rent element by rent id.

    :param request:
    :param rent_id:
    -- :param user_id:
    :return:
    """

    ret_val = {}
    query_str = delete_rent_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, rent_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_rent_element service erred with: {}'.format(gclcerr))

    return ret_val
