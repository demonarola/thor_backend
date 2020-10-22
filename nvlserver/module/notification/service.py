#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_notification_specification import (
    get_notification_list_query, get_notification_list_count_query,
    get_notification_element_query, get_notification_list_unread_count_query
)
from .specification.delete_notification_specification import delete_notification_element_query
from .specification.update_notification_specification import update_notification_element_read_query
from .specification.create_notification_specification import create_notification_element_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'get_notification_list', 'get_notification_unread_count', 'get_notification_list_count',
    'get_notification_element', 'create_notification_element', 'update_notification_element_read',
    'delete_notification_element'
]


async def get_notification_list(
        request: Request,
        name=None,
        limit: int = 0,
        offset: int = 0) -> list:
    """ Get notification list ordered by notification id desc.

    :param request:
    :param name:
    :param limit:
    :param offset:
    :return:
    """
    ret_val = []

    query_str = get_notification_list_query

    try:
        if limit > 0:
            query_str += ' ORDER BY nt.id DESC, nt.read LIMIT $2 OFFSET $3;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name, limit, offset)
        else:
            query_str += ' ORDER BY nt.id DESC, nt.read;'
            async with request.app.pg.acquire() as connection:
                rows = await connection.fetch(query_str, name)

        if rows is not None:
            ret_val = [dict(x) for x in rows]

    except Exception as gclerr:
        logger.error('get_notification_list service erred with: {}'.format(gclerr))

    return ret_val


async def get_notification_unread_count(
        request: Request) -> int:
    """ Get notification list unread count.

    :param request:
    :return:
    """

    ret_val = 0
    query_str = get_notification_list_unread_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_notification_unread_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_notification_list_count(
        request: Request,
        name=None) -> int:
    """ Get notification list count.

    :param request:
    :param name:
    :return:
    """

    ret_val = 0
    query_str = get_notification_list_count_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, name)
            if row is not None:
                ret_val = row
    except Exception as gclcerr:
        logger.error('get_notification_list_count service erred with: {}'.format(gclcerr))

    return ret_val


async def get_notification_element(
        request: Request,
        notification_id: int = 0) -> dict:
    """ Get notification element by notification id.

    :param request:
    :param notification_id:
    :return:
    """

    ret_val = {}
    query_str = get_notification_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchval(query_str, notification_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('get_notification_element service erred with: {}'.format(gclcerr))

    return ret_val


async def create_notification_element(
        request: Request,
        name: str = '',
        notification_type_id: int = 0,
        description: str = '') -> dict:
    """ Create notification element

    :param request:
    :param name:
    :param notification_type_id:
    :param description:
    :return:
    """

    ret_val = {}
    query_str = create_notification_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, name, description, notification_type_id, False, True)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('create_notification_element service erred with: {}'.format(gclcerr))

    return ret_val


async def update_notification_element_read(
        request: Request,
        notification_id: int = 0) -> dict:
    """ Update read status on notification element by notification id.

    :param request:
    :param notification_id:
    :return:
    """

    ret_val = {}
    query_str = update_notification_element_read_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, notification_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('update_notification_element_read service erred with: {}'.format(gclcerr))

    return ret_val


async def delete_notification_element(
        request: Request,
        notification_id: int = 0) -> dict:
    """ Delete notification element by notification id.

    :param request:
    :param notification_id:
    :return:
    """

    ret_val = {}
    query_str = delete_notification_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, notification_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as gclcerr:
        logger.error('delete_notification_element service erred with: {}'.format(gclcerr))

    return ret_val
