#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from sanic.log import logger
from sanic.request import Request

from .specification.get_request_logger_specification import (
    get_request_log_by_route_query
)

from .specification.create_request_logger_specification import create_request_logger_element_query

__all__ = [
    # SERVICES WORKING ON LANGUAGE TABLE
    'create_request_log_element', 'get_request_log_list'
]


# CREATE REQUEST LOG ELEMENT
async def create_request_log_element(
        request: Request,
        route=None,
        request_data=None,
        response_data=None,
        active=True) -> dict:
    """ Create request log element

    :param request:
    :param route:
    :param request_data:
    :param response_data:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_request_logger_element_query
    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, route, request_data, response_data, active)

            if row is not None:
                ret_val = row
    except Exception as crleerr:
        logger.error('create_request_log_element service erred with: {}'.format(crleerr))

    return ret_val


async def get_request_log_list(
        request: Request,
        route=None) -> dict:
    """ Create request log list

    :param request:
    :param route:
    :return:
    """

    ret_val = {}
    query_str = get_request_log_by_route_query
    try:
        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, route)

            if row is not None:
                ret_val = row
    except Exception as grllerr:
        logger.error('get_request_log_list service erred with: {}'.format(grllerr))

    return ret_val
