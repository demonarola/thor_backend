#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic import response
from sanic.request import Request
from sanic.log import logger
from sanic_jwt import inject_user, scoped
from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

from .service import (
    get_user_hw_action_list, get_user_hw_action_list_count, get_user_hw_action_element,
    create_user_hw_action_element, update_user_hw_action_element, delete_user_hw_action_element
)


api_user_hw_action_blueprint = Blueprint('api_user_hw_action', url_prefix='/api/hw_action/user')


# USER HW ACTION TYPE CONTROLLER
@api_user_hw_action_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_user_hw_action(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    name = request.args.get('name', None)
    user_id = request.args.get('user_id', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    user_hw_action_list = await get_user_hw_action_list(
                        request, user_id=user_id, name=name, limit=size, offset=offset)
                    user_hw_action_list_count = await get_user_hw_action_list_count(
                        request, user_id=user_id, name=name)

                    if user_hw_action_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            user_hw_action_list, user_hw_action_list_count, size=size, page=page)
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
        except Exception as al_err:
            logger.error('Function api_user_hw_action -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# TODO: REMOVE UN USED PART OF THE CODE
@api_user_hw_action_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_user_hw_action_dropdown_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.args.get('name', None)
    user_id = request.args.get('user_id', None)

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):

                    user_hw_action_list = await get_user_hw_action_list(
                        request, user_id=user_id, name=name)

                    if user_hw_action_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = user_hw_action_list
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = []
                        status = 200
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_user_hw_action_dropdown_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_user_hw_action_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_user_hw_action_post(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = request.args.get('user_id', None)
    hw_action_id = request.args.get('hw_action_id', None)
    value = request.args.get('value', None)
    date_from = request.args.get('date_from', None)
    date_to = request.json.get('date_to', None)
    active = request.json.get('active', False)

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('user_id') and user.get('account_type_name') == 'admin':

                        if None not in [user_id, hw_action_id, value]:
                            user_hw_action_element = await create_user_hw_action_element(
                                request, user_id=user_id, hw_action_id=hw_action_id,
                                value=value, date_from=date_from, date_to=date_to, active=active)

                            if user_hw_action_element:
                                ret_val['data'] = user_hw_action_element
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
        except Exception as al_err:
            logger.error('Function api_user_hw_action_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_user_hw_action_blueprint.route('/<user_hw_action_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_user_hw_action_element(request: Request, user, user_hw_action_id: int = 0):
    """

    :param request:
    :param user:
    :param user_hw_action_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = request.args.get('user_id', None)

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None) and user_hw_action_id:

                    user_hw_action_element = await get_user_hw_action_element(
                        request, user_id=user_id, user_hw_action_id=user_hw_action_id)

                    if user_hw_action_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = user_hw_action_element
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
        except Exception as al_err:
            logger.error('Function api_user_hw_action_element -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_user_hw_action_blueprint.route('/<user_hw_action_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_user_hw_action_element_put(request: Request, user, user_hw_action_id: int = 0):
    """

    :param request:
    :param user:
    :param user_hw_action_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = request.args.get('user_id', None)
    hw_action_id = request.args.get('hw_action_id', None)
    value = request.args.get('value', None)
    date_from = request.args.get('date_from', None)
    date_to = request.json.get('date_to', None)
    active = request.json.get('active', False)

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id', None) and user_hw_action_id and user.get('account_type_name') == 'admin':
                    user_hw_action_element = await update_user_hw_action_element(
                        request, user_hw_action_id=user_hw_action_id,
                        user_id=user_id, hw_action_id=hw_action_id,
                        value=value, date_from=date_from, date_to=date_to, active=active)

                    if user_hw_action_element:
                        ret_val['data'] = user_hw_action_element
                        ret_val['success'] = True
                        status = 201
                        ret_val['message'] = 'server.object_created'
                else:
                    status = 412
                    ret_val['message'] = 'server.query_condition_failed'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_user_hw_action_type_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_user_hw_action_blueprint.route('/<user_hw_action_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_user_hw_action_element_delete(request: Request, user, user_hw_action_id: int = 0):
    """

    :param request:
    :param user:
    :param user_hw_action_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = request.args.get('user_id', None)

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):

                    if user_hw_action_id and user.get('account_type_name') == 'admin':

                        deleted_elem = await delete_user_hw_action_element(
                            request, user_id=user_id, user_hw_action_id=user_hw_action_id)
                        if deleted_elem:
                            status = 202
                            ret_val['success'] = True
                            ret_val['message'] = 'server.accepted'
                    else:
                        status = 403
                        ret_val['message'] = 'server.forbidden'
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_user_hw_action_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
