#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson

from sanic import Blueprint
from sanic import response

from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, scoped


from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

# from web_backend.nvlserver.module.hw_module_command_state.service import create_hw_module_command_state_element
from .service import (
    get_hw_module_list, get_hw_module_list_count, create_hw_module_element,
    get_hw_module_element, update_hw_module_element, delete_hw_module_element,
    get_hw_module_dropdown_list, get_hw_module_random_unique_str,
    get_hw_module_random_unique_str_list, update_user_hw_module_element
)

api_hw_module_blueprint = Blueprint('api_hw_module', url_prefix='/api/hw_module')


@api_hw_module_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['hw_module:read'], require_all=True, require_all_actions=True)
async def api_hw_module_list_get(
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
    user_id = request.args.get('user_id', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') in ['admin']:
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')
                    hw_module_list = await get_hw_module_list(
                        request, user_id=user_id, name=name, limit=size, offset=offset)
                    hw_module_count = await get_hw_module_list_count(request, user_id=user_id, name=name)

                    if hw_module_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            hw_module_list, hw_module_count, size=size, page=page)
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
            logger.error('Function api_hw_module_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_module_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
@scoped(['hw_module:query_dropdown'], require_all=True, require_all_actions=True)
async def api_hw_module_list_dropdown_get(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.args.get('name', None)

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') in ['admin']:
                        user_id = None
                    else:
                        user_id = user.get('user_id')
                    hw_module_list = await get_hw_module_dropdown_list(
                        request, user_id=user_id, name=name)

                    if hw_module_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = hw_module_list
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
            logger.error('Function api_hw_module_list_dropdown_gets -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_module_blueprint.route('/', methods=['POST'])
@inject_user()
@scoped(['hw_module:create'], require_all=True, require_all_actions=True)
async def api_hw_module_post(
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
        try:
            if user:

                if user.get('user_id'):
                    if user.get('account_type_name') in ['admin']:
                        # print(request.json)
                        name = request.json.get('name', None)
                        user_id = request.json.get('user_id', None)
                        traceable_object_id = request.json.get('traceable_object_id', None)
                        show_on_map = request.json.get('show_on_map', False)
                        active = request.json.get('active', False)

                        meta_information = {}

                        module_id = request.json.get('module_id', await get_hw_module_random_unique_str(request))

                        if None not in [module_id, name]:
                            hw_module = await create_hw_module_element(
                                request, name, module_id, user_id, traceable_object_id,
                                meta_information, show_on_map, active)

                            if hw_module:
                                # await create_hw_module_command_state_element(
                                #     request, hw_module.get('id')
                                # )
                                ret_val['data'] = hw_module
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
            logger.error('Function api_hw_module_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_module_blueprint.route('/<hw_module_id:int>', methods=['GET'])
@inject_user()
@scoped(['hw_module:read'], require_all=True, require_all_actions=True)
async def api_hw_module_element_get(
        request: Request,
        user,
        hw_module_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_module_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None) and hw_module_id:

                    hw_module_element = await get_hw_module_element(request, hw_module_id)

                    if hw_module_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = hw_module_element
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
            logger.error('Function api_hw_module_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_module_blueprint.route('/<hw_module_id:int>', methods=['PUT'])
@inject_user()
@scoped(['hw_module:update'], require_all=True, require_all_actions=True)
async def api_hw_module_element_put(
        request: Request,
        user,
        hw_module_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_module_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id'):

                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and hw_module_id:
                        name = request.json.get('name', None)
                        if user.get('account_type_name') in ['admin']:
                            user_id = request.json.get('user_id', None)
                        else:
                            user_id = user.get('user_id')

                        traceable_object_id = request.json.get('traceable_object_id', None)

                        show_on_map = request.json.get('show_on_map', False)
                        active = request.json.get('active', False)
                        module_id = request.json.get('module_id', None)
                        meta_information = {}

                        if None not in [show_on_map, active]:
                            if user.get('account_type_name') in ['admin']:
                                updated_module = await update_hw_module_element(
                                    request, hw_module_id=hw_module_id, name=name,
                                    module_id=module_id, user_id=user_id, traceable_object_id=traceable_object_id,
                                    meta_information=meta_information,
                                    show_on_map=show_on_map, active=active)
                            else:
                                updated_module = await update_user_hw_module_element(
                                    request, hw_module_id=hw_module_id, user_id=user_id,
                                    traceable_object_id=traceable_object_id,
                                    show_on_map=show_on_map, active=active)

                            ret_val['success'] = True
                            ret_val['message'] = 'server.query_success'
                            ret_val['data'] = updated_module
                            status = 202
                            ret_val['message'] = 'server.accepted'
                        else:
                            status = 412
                            ret_val['message'] = 'server.query_condition_failed'
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_hw_module_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_module_blueprint.route('/<hw_module_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['hw_module:delete'], require_all=True, require_all_actions=True)
async def api_hw_module_element_delete(
        request: Request,
        user,
        hw_module_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_module_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):
                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and hw_module_id:
                        hw_module = await delete_hw_module_element(request, hw_module_id)

                        if hw_module:
                            ret_val['success'] = True
                            ret_val['message'] = 'server.query_success'
                            ret_val['data'] = None
                            status = 202
                            ret_val['message'] = 'server.accepted'
                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_hw_module_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_hw_module_blueprint.route('/unassigned_hw_modules/dropdown', methods=['GET'])
@inject_user()
@scoped(['hw_module:create'], require_all=True, require_all_actions=True)
async def api_hw_module_unassigned_id_get(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    module_id = request.args.get('module_id', None)

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):

                    hw_module_unique_id_list = await get_hw_module_random_unique_str_list(
                        request, module_id=module_id)

                    if hw_module_unique_id_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = hw_module_unique_id_list
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
            logger.error('Function api_hw_module_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
