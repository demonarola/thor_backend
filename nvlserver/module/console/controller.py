#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from asyncio import sleep
import datetime
from sanic import Blueprint
from sanic import response
from sanic.request import Request
from sanic_jwt import inject_user, scoped

from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int
from .service import (
    get_console_list, get_console_list_count, create_console_element,
    get_console_element, update_console_element, delete_console_element
)

api_console_blueprint = Blueprint('api_console', url_prefix='/api/console')


@api_console_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_console_get(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    offset = (page - 1) * size

    if request.method == 'GET':
        if user:
            if user.get('user_id', None):
                console_list = await get_console_list(request, limit=size, offset=offset)
                console_list_count = await get_console_list_count(request)
                # print(console_list, console_list_count)

                if console_list:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    res_data_formatted = await populate_response_format(
                        console_list, console_list_count, size=size, page=page)
                    ret_val['data'] = res_data_formatted
                    status = 200
                else:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = {}
                    status = 200
            else:
                status = 400
                ret_val['message'] = 'server.bad_request'
        else:
            status = 401
            ret_val['message'] = 'server.unauthorized'

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_console_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_console_element_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'POST':
        if user:
            if user.get('user_id') is not None:
                if user.get('user_id') and user.get('account_type_name') == 'admin':
                    timestamp_utc = request.json.get('timestamp', None)
                    message = request.json.get('message', None)
                    user_id = request.json.get('user_id', None)
                    timestamp = datetime.datetime.fromtimestamp(timestamp_utc)

                    if None not in [user_id, message]:
                        console_element = await create_console_element(request, timestamp, user_id, message, True)

                        if console_element:
                            ret_val['data'] = console_element
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = 'server.object_created'
                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'

                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'

            else:
                status = 400
                ret_val['message'] = 'server.bad_request'
        else:
            status = 401
            ret_val['message'] = 'server.unauthorized'

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_console_blueprint.route('/<console_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_console_element_get(
        request: Request,
        user,
        console_id: int = 0):
    """

    :param request:
    :param user:
    :param console_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:

            if user.get('user_id', None) and console_id:

                console_element = await get_console_element(request, console_id)

                if console_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = console_element
                    status = 200
                else:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    status = 200
            else:
                status = 400
                ret_val['message'] = 'server.bad_request'
        else:
            status = 401
            ret_val['message'] = 'server.unauthorized'

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_console_blueprint.route('/<console_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_console_element_put(
        request: Request,
        user,
        console_id: int = 0):
    """

    :param request:
    :param user:
    :param console_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        if user:

            if user.get('user_id'):
                if user.get('user_id') and user.get('account_type_name') == 'admin':
                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    timestamp_utc = request.json.get('timestamp', None)
                    message = request.json.get('message', None)
                    user_id = request.json.get('user_id', None)
                    timestamp = datetime.datetime.fromtimestamp(timestamp_utc)

                    if None not in [user_id, message]:
                        console_element = await update_console_element(
                            request, console_id, timestamp, user_id, message, True)

                        if console_element:
                            ret_val['data'] = console_element
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = 'server.object_created'
                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'

                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 400
                ret_val['message'] = 'server.bad_request'
        else:
            status = 401
            ret_val['message'] = 'server.unauthorized'

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_console_blueprint.route('/<console_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_console_element_delete(
        request: Request,
        user,
        console_id: int = 0):
    """

    :param request:
    :param user:
    :param console_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        # if user:
        if True:

            # if user.get('user_id') and console_id:
            if True:

                console_element = await delete_console_element(request, console_id)

                if console_element:
                    ret_val['success'] = True
                    status = 201
                    ret_val['message'] = 'server.object_created'
            else:
                status = 400
                ret_val['message'] = 'server.bad_request'
        else:
            status = 401
            ret_val['message'] = 'server.unauthorized'

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
