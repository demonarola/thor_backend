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
    # IMPORT HW ACTION SERVICES
    get_hw_action_element, get_hw_action_list, get_hw_action_list_count,
    delete_hw_action_element, update_hw_action_element, create_hw_action_element,
)


api_hw_action_blueprint = Blueprint('api_hw_action', url_prefix='/api/hw_action')


# hw_action CONTROLLER
@api_hw_action_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_action(
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
    name = request.args.get('name', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:

            if user:

                if user.get('user_id', None):
                    hw_action_list = await get_hw_action_list(request, name=name, limit=size, offset=offset)
                    hw_action_list_count = await get_hw_action_list_count(request, name=name)

                    if hw_action_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            hw_action_list, hw_action_list_count, size=size, page=page)
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
            logger.error('Function api_hw_action -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_action_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_action(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    action_type = request.args.get('type', None)

    if request.method == 'GET':
        try:

            if user:

                if user.get('user_id', None):
                    hw_action_list = await get_hw_action_list(request, action_type=action_type)

                    if hw_action_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = hw_action_list
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
            logger.error('Function api_hw_action -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_action_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_hw_action_post(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.json.get('name', None)
    active = request.json.get('active', False)
    meta_information = {}

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('user_id') and user.get('account_type_name') == 'admin':

                        if None not in ['name']:
                            hw_action_element = await create_hw_action_element(
                                request, name=name,
                                meta_information=meta_information, active=active)

                            if hw_action_element:
                                ret_val['data'] = hw_action_element
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
            logger.error('Function api_hw_action_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_action_blueprint.route('/<hw_action_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_action_element(
        request: Request,
        user,
        hw_action_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_action_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None) and hw_action_id:

                    hw_action_element = await get_hw_action_element(request, hw_action_id)

                    if hw_action_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = hw_action_element
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
            logger.error('Function api_hw_action_element -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_action_blueprint.route('/<hw_action_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_hw_action_element_put(
        request: Request,
        user,
        hw_action_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_action_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.json.get('name', None)
    # traceable_object_id = request.json.get('traceable_object_id', None)
    active = request.json.get('active', False)
    meta_information = {}

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id', None) and hw_action_id and user.get('account_type_name') == 'admin':

                    hw_action_element = await update_hw_action_element(
                        request, hw_action_id=hw_action_id, name=name,
                        meta_information=meta_information, active=active)

                    if hw_action_element:
                        ret_val['data'] = hw_action_element
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
            logger.error('Function api_hw_action_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_action_blueprint.route('/<hw_action_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_hw_action_element_delete(
        request: Request,
        user,
        hw_action_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_action_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id') and user.get('account_type_name') == 'admin':

                    hw_action = get_hw_action_element(request, hw_action_id)
                    if hw_action:

                        deleted_elem = await delete_hw_action_element(request, hw_action_id)
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
            logger.error('Function api_hw_action_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
