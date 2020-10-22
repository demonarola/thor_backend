#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.create_hw_command_specification import (
    create_hw_command_element_query, create_hw_command_element_rent_query
)
from .specification.get_hw_command_specification import (
    get_hw_command_list_query, get_hw_command_list_count_query, get_hw_command_state_by_hw_module_id_query
)

__all__ = [
    # SERVICES WORKING ON USER HW COMMAND TABLE
    'get_user_hw_command_list', 'get_user_hw_command_list_count', 'create_user_hw_command_element',
    'create_user_hw_command_element_rent', 'get_user_hw_command_state_by_traceable_object_id'
]


async def get_user_hw_command_list(
        request: Request,
        user_id: int = 0,
        action_name: str = '',
        action_type: str = '',
        state: str = '',
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get get hw_command list ordered by id desc.

    :param request:
    :param user_id:
    :param action_name:
    :param action_type:
    :param state:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_hw_command_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY uhc.id DESC LIMIT $5 OFFSET $6;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(
                    query_str, user_id, action_name, action_type, state, limit, offset)
        else:
            query_str += ' ORDER BY uhc.id DESC;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, user_id, action_name, action_type, state)

        if rows is not None:
            ret_val = [dict(x) for x in rows]
            print(ret_val)

    except Exception as gclerr:
        logger.error('get_user_hw_command_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_user_hw_command_list_count(
        request: Request,
        user_id: int = 0,
        action_name: str = '',
        action_type: str = '',
        state: str = '') -> int:
    """Get hw  command list count.

    :param request:
    :param user_id:
    :param action_name:
    :param action_type:
    :param state:
    :return:
    """

    ret_val = 0
    query_str = get_hw_command_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, user_id, action_name, action_type, state)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_user_hw_command_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_user_hw_command_state_by_traceable_object_id(
        request: Request,
        traceable_object_id: int = 0) -> []:
    """Get hw  command list count.

    :param request:
    :param traceable_object_id:

    :return:
    """

    ret_val = 0
    query_str = get_hw_command_state_by_hw_module_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, traceable_object_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_user_hw_command_state_by_traceable_object_id service erred with: {}'.format(gclcerr))

    return ret_val



async def create_user_hw_command_element(
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
        active: bool = True) -> dict:
    """ Create user hw command element

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
    :param active:
    :return:
    """
    ret_val = []

    query_str = create_hw_command_element_query

    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, hw_action_id, proto_field, field_type, value,
                state, traceable_object_id, hw_module_id, ack_message, active)

            if row is not None:
                ret_val = dict(row)

    except Exception as gclerr:
        logger.error('create_user_hw_command_element service erred with: {}'.format(gclerr))

    return ret_val


async def create_user_hw_command_element_rent(
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
        date_from: object = None,
        date_to: object = None,
        active: bool = True) -> dict:
    """ Create user hw command element

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

    query_str = create_hw_command_element_rent_query

    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, user_id, hw_action_id, proto_field, field_type, value,
                state, traceable_object_id, hw_module_id, ack_message, date_from, date_to, active)

            if row is not None:
                ret_val = dict(row)

    except Exception as gclerr:
        logger.error('create_user_hw_command_element_rent service erred with: {}'.format(gclerr))

    return ret_val
