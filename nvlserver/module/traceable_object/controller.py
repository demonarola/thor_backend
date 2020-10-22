#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic import response
from sanic.request import Request
from sanic_jwt import inject_user, scoped
from sanic.log import logger

from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

from .service import (
    get_traceable_object_list, get_traceable_object_dropdown_list,
    get_traceable_object_list_count, create_traceable_object_element,
    get_traceable_object_element, update_traceable_object_element, delete_traceable_object_element,
    # TRACEABLE OBJECT TYPE IMPORTS
    get_traceable_object_type_list, get_traceable_object_type_dropdown_list,
    get_traceable_object_type_list_count, create_traceable_object_type_element,
    get_traceable_object_type_element, update_traceable_object_type_element, delete_traceable_object_type_element,
    get_traceable_object_brand_dropdown_list, get_traceable_object_model_dropdown_list
)

from web_backend.nvlserver.module.hw_command.service import (
    create_user_hw_command_element, get_user_hw_command_state_by_traceable_object_id
)
from web_backend.nvlserver.module.hw_action.service import get_hw_action_element
from web_backend.nvlserver.module.hw_module.service import get_hw_module_element


api_traceable_object_blueprint = Blueprint('api_traceable_object', url_prefix='/api/traceable_object')


@api_traceable_object_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['traceable_object:read'], require_all=True, require_all_actions=True)
async def api_traceable_object_list_get(request: Request, user):
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
                    if user.get('account_type_name') == 'admin':
                        traceable_object_list = await get_traceable_object_list(
                            request, user_id=None, name=name, limit=size, offset=offset)
                        traceable_object_count = await get_traceable_object_list_count(
                            request, user_id=None, name=name)
                    else:
                        traceable_object_list = await get_traceable_object_list(
                            request, user_id=user.get('user_id'), name=name, limit=size, offset=offset)
                        traceable_object_count = await get_traceable_object_list_count(
                            request, user_id=user.get('user_id'), name=name)

                    if traceable_object_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            traceable_object_list, traceable_object_count, size=size, page=page)
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
            logger.error('Function api_traceable_object_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
@scoped(['traceable_object:query_dropdown'], require_all=True, require_all_actions=True)
async def api_traceable_object_list_dropdown_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.args.get('name', None)
    user_id = proc_arg_to_int(request.args.get('user_id', ['0'])[0], 0)

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')
                    traceable_object_list = await get_traceable_object_dropdown_list(
                        request, user_id=user_id, name=name)

                    if traceable_object_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = traceable_object_list
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
            logger.error('Function api_traceable_object_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/', methods=['POST'])
@inject_user()
@scoped(['traceable_object:create'], require_all=True, require_all_actions=True)
async def api_traceable_object_post(request: Request, user):
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
                    name = request.json.get('name', None)
                    traceable_object_type_id = request.json.get('traceable_object_type_id', None)

                    note = request.json.get('note', '')
                    show_on_map = request.json.get('show_on_map', False)
                    action = request.json.get('action', False)
                    collision_avoidance_system = request.json.get('collision_avoidance_system', False)
                    active = request.json.get('active', True)
                    consumption = request.json.get('consumption', '0')
                    registration_number = request.json.get('registration_number', '0')
                    vin_number = request.json.get('vin_number', '0')
                    vehicle_brand = request.json.get('vehicle_brand', '')
                    vehicle_brand_id = request.json.get('vehicle_brand_id', 0)
                    vehicle_model = request.json.get('vehicle_model', '')
                    vehicle_model_id = request.json.get('vehicle_model_id', 0)
                    vehicle_year = request.json.get('vehicle_year', '')
                    vehicle_default_throttle = request.json.get('vehicle_default_throttle', 60)
                    meta_information = {
                        'consumption': consumption,
                        'registration_number': registration_number,
                        'vin_number': vin_number,
                        'vehicle_brand': vehicle_brand,
                        'vehicle_model_id': vehicle_model_id,
                        'vehicle_brand_id': vehicle_brand_id,
                        'vehicle_model': vehicle_model,
                        'vehicle_year': vehicle_year,
                        'vehicle_default_throttle': vehicle_default_throttle

                    }
                    if user.get('account_type_name') == 'user':
                        user_id = user.get('user_id')
                    else:
                        user_id = request.json.get('user_id', user.get('user_id'))

                    if None not in [name]:
                        traceable_object = await create_traceable_object_element(
                            request, name=name, traceable_object_type_id=traceable_object_type_id,
                            user_id=user_id, note=note, meta_information=meta_information,
                            show_on_map=show_on_map,
                            action=action, collision_avoidance_system=collision_avoidance_system,
                            active=active)
                        # print(traceable_object)
                        if traceable_object:
                            ret_val['data'] = traceable_object
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = 'server.object_created'
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
            logger.error('Function api_traceable_object_post -> POST erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/<traceable_object_id:int>', methods=['GET'])
@inject_user()
@scoped(['traceable_object:read'], require_all=True, require_all_actions=True)
async def api_traceable_object_element_get(request, user, traceable_object_id: int = 0):
    """

    :param request:
    :param user:
    :param traceable_object_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None) and traceable_object_id:
                    if user.get('account_type_name') == 'user':
                        user_id = user.get('user_id')
                    else:
                        user_id = None
                    traceable_object_element = await get_traceable_object_element(
                        request, user_id=user_id, traceable_object_id=traceable_object_id)

                    if traceable_object_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = traceable_object_element
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
            logger.error('Function api_traceable_object_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/<traceable_object_id:int>', methods=['PUT'])
@inject_user()
@scoped(['traceable_object:update'], require_all=True, require_all_actions=True)
async def api_traceable_object_element_put(request: Request, user, traceable_object_id: int = 0):
    """

    :param request:
    :param user:
    :param traceable_object_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id'):

                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if traceable_object_id:
                        name = request.json.get('name', None)
                        traceable_object_type_id = request.json.get('traceable_object_type_id', None)
                        # REPLACE WHEN USER MANAGEMENT IS IMPLEMENTED TO user.get('user_id')
                        # IMPLEMENT USER DROP DOWN ON ADMIN INTERFACE
                        if user.get('account_type_name') == 'admin':
                            user_id = request.json.get('user_id', None)
                        else:
                            user_id = user.get('user_id')
                        note = request.json.get('note', '')
                        show_on_map = request.json.get('show_on_map', False)
                        action = request.json.get('action', False)
                        active = request.json.get('active', True)
                        consumption = request.json.get('consumption', '0')
                        registration_number = request.json.get('registration_number', '0')
                        collision_avoidance_system = request.json.get('collision_avoidance_system', False)
                        vin_number = request.json.get('vin_number', '0')
                        vehicle_brand = request.json.get('vehicle_brand', '')
                        vehicle_brand_id = request.json.get('vehicle_brand_id', 0)
                        vehicle_model = request.json.get('vehicle_model', '')
                        vehicle_model_id = request.json.get('vehicle_model_id', 0)
                        vehicle_year = request.json.get('vehicle_year', '')
                        vehicle_default_throttle = request.json.get('vehicle_default_throttle', 60)
                        meta_information = {
                            'consumption': consumption,
                            'registration_number': registration_number,
                            'vin_number': vin_number,
                            'vehicle_brand': vehicle_brand,
                            'vehicle_model_id': vehicle_model_id,
                            'vehicle_brand_id': vehicle_brand_id,
                            'vehicle_model': vehicle_model,
                            'vehicle_year': vehicle_year,
                            'vehicle_default_throttle': vehicle_default_throttle

                        }

                        if None not in [name]:
                            traceable_object = await update_traceable_object_element(
                                request, user_id=user_id, traceable_object_id=traceable_object_id, name=name,
                                traceable_object_type_id=traceable_object_type_id,
                                note=note, meta_information=meta_information, show_on_map=show_on_map,
                                action=action, collision_avoidance_system=collision_avoidance_system,
                                active=active)

                            if traceable_object:
                                ret_val['success'] = True
                                ret_val['message'] = 'server.query_success'
                                ret_val['data'] = traceable_object
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
            logger.error('Function api_traceable_object_element_put -> PUT erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/<traceable_object_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['traceable_object:delete'], require_all=True, require_all_actions=True)
async def api_traceable_object_element_delete(request: Request, user, traceable_object_id: int = 0):
    """

    :param request:
    :param user:
    :param traceable_object_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):

                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if traceable_object_id:
                        if user.get('account_type_name') == 'admin':
                            user_id = None
                        else:
                            user_id = user.get('user_id')
                        # print(30 * '-')
                        await delete_traceable_object_element(
                            request, user_id=user_id, traceable_object_id=traceable_object_id)
                        # print(30 * '-')
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
            logger.error('Function api_traceable_object_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/create_command', methods=['POST'])
@inject_user()
@scoped(['traceable_object:create_command'], require_all=True, require_all_actions=True)
async def api_traceable_object_create_command_post(request: Request, user):
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
                    hw_action_id = request.json.get('hw_action_id', None)
                    # TODO: SEND VALID ELEMENTS FROM FRONTEND
                    value = request.json.get('value', True)
                    hw_module_id = request.json.get('hw_module_id')
                    # print(request.json)
                    if None not in [hw_action_id]:
                        hw_action = await get_hw_action_element(request, hw_action_id)
                        hw_module_element = await get_hw_module_element(request, hw_module_id=hw_module_id)
                        if hw_action:
                            # TODO: REMOVE ON FRONTEND NEEDED TO BE IMPLEMENTED VALUE PASS
                            if hw_action_id == 5:
                                state_list = await get_user_hw_command_state_by_traceable_object_id(
                                    request,
                                    hw_module_element.get('traceable_object_id'))
                                if state_list:
                                    act_list = state_list.get('action_list')
                                    pref_action = [x for x in act_list if x.get('hw_action_id') == 5]
                                    if pref_action:
                                        element = pref_action[0]
                                        if element.get('state') is False:
                                            value = True
                                        else:
                                            value = False
                                print(state_list)

                            created_command = await create_user_hw_command_element(
                                request, user_id=user.get('user_id'),
                                hw_action_id=hw_action.get('id'), proto_field=hw_action.get('proto_field'),
                                field_type=hw_action.get('action').get('type'), value=str(value),
                                state='pending', traceable_object_id=hw_module_element.get('traceable_object_id'),
                                hw_module_id=hw_module_element.get('id'), ack_message=True,
                                active=True
                            )

                            if created_command:
                                ret_val['data'] = created_command
                                ret_val['success'] = True
                                status = 201
                                ret_val['message'] = 'server.object_created'
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
            logger.error('Function api_traceable_object_create_command_post -> POST erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# TRACEABLE OBJECT TYPE API
@api_traceable_object_blueprint.route('/type', methods=['GET'])
@inject_user()
@scoped(['traceable_object:read'], require_all=True, require_all_actions=True)
async def api_traceable_object_type_list_get(request: Request, user):
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

                    traceable_object_list = await get_traceable_object_type_list(
                        request, name=name, limit=size, offset=offset)
                    traceable_object_count = await get_traceable_object_type_list_count(request, name=name)

                    if traceable_object_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            traceable_object_list, traceable_object_count, size=size, page=page)
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
            logger.error('Function api_traceable_object_type_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/type/dropdown', methods=['GET'])
@inject_user()
@scoped(['traceable_object:query_dropdown'], require_all=True, require_all_actions=True)
async def api_traceable_object_type_list_dropdown_get(request: Request, user):
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

                    traceable_object_type_list = await get_traceable_object_type_dropdown_list(
                        request, name=name)

                    if traceable_object_type_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = traceable_object_type_list
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
            logger.error('Function api_traceable_object_type_dropdown_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/type', methods=['POST'])
@inject_user()
@scoped(['traceable_object:create'], require_all=True, require_all_actions=True)
async def api_traceable_object_type_post(request: Request, user):
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
                    if user.get('account_type_name') == 'admin':
                        name = request.json.get('name', None)
                        active = request.json.get('active', True)

                        if None not in [name]:
                            traceable_object_type = await create_traceable_object_type_element(
                                request, name, active)

                            ret_val['data'] = traceable_object_type
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
            logger.error('Function api_traceable_object_type_post -> POST erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/type/<traceable_object_type_id:int>', methods=['GET'])
@inject_user()
@scoped(['traceable_object:read'], require_all=True, require_all_actions=True)
async def api_traceable_object_type_element_get(request, user, traceable_object_type_id: int = 0):
    """

    :param request:
    :param user:
    :param traceable_object_type_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None) and traceable_object_type_id:

                    traceable_object_type_element = await get_traceable_object_type_element(
                        request, traceable_object_type_id)

                    if traceable_object_type_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = traceable_object_type_element
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
            logger.error('Function api_traceable_object_type_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/type/<traceable_object_type_id:int>', methods=['PUT'])
@inject_user()
@scoped(['traceable_object:update'], require_all=True, require_all_actions=True)
async def api_traceable_object_type_element_put(request, user, traceable_object_type_id: int = 0):
    """

    :param request:
    :param user:
    :param traceable_object_type_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        try:
            if user:
                if user.get('user_id'):

                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and traceable_object_type_id:
                        name = request.json.get('name', None)

                        if None not in [name]:
                            utot = await update_traceable_object_type_element(
                                request, traceable_object_type_id, name, True)

                            if utot:
                                ret_val['success'] = True
                                ret_val['message'] = 'server.query_success'
                                ret_val['data'] = utot
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
            logger.error('Function api_traceable_object_type_element_put -> PUT erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_traceable_object_blueprint.route('/type/<traceable_object_type_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['traceable_object:delete'], require_all=True, require_all_actions=True)
async def api_traceable_object_type_element_delete(request, user, traceable_object_type_id: int = 0):
    """

    :param request:
    :param user:
    :param traceable_object_type_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:
                if user.get('user_id'):

                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and traceable_object_type_id:
                        await delete_traceable_object_type_element(
                            request, traceable_object_type_id=traceable_object_type_id)

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
            logger.error('Function api_traceable_object_type_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# TRACEABLE OBJECT BRAND API
@api_traceable_object_blueprint.route('/brand/dropdown', methods=['GET'])
@inject_user()
@scoped(['traceable_object:query_dropdown'], require_all=True, require_all_actions=True)
async def api_traceable_object_brand_list_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    # size = proc_arg_to_int(request.args.get('size', '1'), 1)
    # page = proc_arg_to_int(request.args.get('page', '1'), 1)
    name = request.args.get('name', None)
    # offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    traceable_object_brand_list = await get_traceable_object_brand_dropdown_list(
                        request, name=name)

                    if traceable_object_brand_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = traceable_object_brand_list
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
            logger.error('Function api_traceable_object_brand_list_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# TRACEABLE OBJECT BRAND API
@api_traceable_object_blueprint.route('/model/dropdown/<brand_id:int>', methods=['GET'])
@inject_user()
@scoped(['traceable_object:query_dropdown'], require_all=True, require_all_actions=True)
async def api_traceable_object_model_list_get(request: Request, user, brand_id: int = 0):
    """

    :param request:
    :param brand_id:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    # size = proc_arg_to_int(request.args.get('size', '1'), 1)
    # page = proc_arg_to_int(request.args.get('page', '1'), 1)
    name = request.args.get('name', None)
    # offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):

                    traceable_object_model_list = await get_traceable_object_model_dropdown_list(
                        request, name=name, traceable_object_brand_id=brand_id)

                    if traceable_object_model_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = traceable_object_model_list
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
            logger.error('Function api_traceable_object_model_list_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
