#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

# import os
import ujson
import datetime

import iso8601

from sanic import Blueprint
from sanic import response
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, protected, scoped

from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

from .service import (
    get_rent_list, get_rent_list_count, get_rent_element,
    create_rent_element, update_rent_element, delete_rent_element
)
from web_backend.nvlserver.module.traceable_object.service import get_traceable_object_element
from web_backend.nvlserver.module.hw_action.service import get_hw_action_element
from web_backend.nvlserver.module.hw_module.service import get_hw_module_element_by_traceable_object_id


api_rent_blueprint = Blueprint('api_rent', url_prefix='/api/rent')


@api_rent_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['rent:read'], require_all=True, require_all_actions=True)
async def api_rent_get(
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
    user_id_param = proc_arg_to_int(request.args.get('user_id', '1'), 0)
    date_from_front = request.args.get('date_from', None)
    date_to_front = request.args.get('date_to', None)
    # print(date_from_front)
    # print(date_to_front)
    # TODO: REMOVE REPLACE ON CHANGE PARAM FROM FRONTEND
    if date_from_front is not None:
        date_from = iso8601.parse_date(date_from_front.replace(' ', '+'))
    else:
        date_from = None
    #     date_from = datetime.datetime.now() - datetime.timedelta(days=30)
    if date_to_front is not None:
        date_to = iso8601.parse_date(date_to_front.replace(' ', '+'))
    else:
        date_to = None
    #     date_to = datetime.datetime.now()
    # print(date_from)
    # print(date_to)
    # state = request.args.get('state', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:

            if user:

                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id_param
                    else:
                        user_id = user.get('user_id')

                    rent_list = await get_rent_list(
                        request, user_id=user_id, date_from=date_from, date_to=date_to, limit=size, offset=offset)
                    rent_count = await get_rent_list_count(
                        request, user_id=user_id, date_from=date_from, date_to=date_to)
                    print(rent_list)
                    print(rent_count)

                    if rent_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            rent_list, rent_count, size=size, page=page)
                        ret_val['data'] = res_data_formatted
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
        except Exception as rt_err:
            logger.error('Function api_rent_get -> GET erred with: {}'.format(rt_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_rent_blueprint.route('/', methods=['POST'])
@inject_user()
@protected()
@scoped(['rent:create'], require_all=True, require_all_actions=True)
async def api_rent_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    user_id_param = request.json.get('user_id', None)
    traceable_object_id = request.json.get('traceable_object_id', None)
    date_from_front = request.json.get('date_from', None)
    date_to_front = request.json.get('date_to', None)
    # print(request.json)

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id_param
                    else:
                        user_id = user.get('user_id')

                    if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':
                        if date_from_front:
                            date_from = iso8601.parse_date(date_from_front)
                        else:
                            date_from = None
                        if date_to_front:
                            date_to = iso8601.parse_date(date_to_front)
                        else:
                            date_to = None

                        traceable_object = await get_traceable_object_element(
                            request, traceable_object_id=traceable_object_id)

                        # CHANGED HET OBJECT WITH NAME
                        hw_action_object = await get_hw_action_element(
                            request, hw_action_id=7)
                        hw_module_object = await get_hw_module_element_by_traceable_object_id(
                            request, traceable_object_id=traceable_object_id)

                        if None not in (traceable_object, hw_action_object, hw_module_object):
                            rent_obj = await create_rent_element(
                                request, user_id=user_id,
                                hw_action_id=hw_action_object.get('id'),
                                proto_field=hw_action_object.get('proto_field'),
                                field_type='bool',
                                value='true',
                                hw_module_id=hw_module_object.get('id'),
                                traceable_object_id=traceable_object.get('id'),
                                ack_message=True,
                                date_from=date_from,
                                date_to=date_to, active=True)

                            if rent_obj:
                                print(rent_obj)
                                ret_val['data'] = rent_obj
                                ret_val['success'] = True
                                status = 201
                                ret_val['message'] = 'server.object_created'

                        else:
                            status = 412
                            ret_val['message'] = 'server.query_condition_failed'
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
            logger.error('Function api_rent_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_rent_blueprint.route('/<rent_id:int>', methods=['GET'])
@inject_user()
@scoped(['rent:read'], require_all=True, require_all_actions=True)
async def api_rent_element_get(
        request: Request,
        user,
        rent_id: int = 0):
    """

    :param request:
    :param user:
    :param rent_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None) and rent_id:

                    rent_element = await get_rent_element(request, rent_id)

                    if rent_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = rent_element
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
            logger.error('Function api_rent_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_rent_blueprint.route('/<rent_id:int>', methods=['PUT'])
@inject_user()
@scoped(['rent:update'], require_all=True, require_all_actions=True)
async def api_rent_element_put(
        request: Request,
        user,
        rent_id: int = 0):
    """

    :param request:
    :param user:
    :param rent_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id_param = request.json.get('user_id', None)
    traceable_object_id = request.json.get('traceable_object_id', None)
    date_from_front = request.json.get('date_from', None)
    date_to_front = request.json.get('date_to', None)

    if request.method == 'PUT':
        try:
            if user:
                # print(request.json)
                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id_param
                    else:
                        user_id = user.get('user_id')

                    if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':
                        if date_from_front:
                            date_from = iso8601.parse_date(date_from_front)
                        else:
                            date_from = None
                        if date_to_front:
                            date_to = iso8601.parse_date(date_to_front)
                        else:
                            date_to = None

                        traceable_object = await get_traceable_object_element(
                            request, traceable_object_id=traceable_object_id)

                        # CHANGED HET OBJECT WITH NAME
                        hw_action_object = await get_hw_action_element(
                            request, hw_action_id=7)
                        hw_module_object = await get_hw_module_element_by_traceable_object_id(
                            request, traceable_object_id=traceable_object_id)

                        if None not in (traceable_object, hw_action_object, hw_module_object):
                            rent_obj = await update_rent_element(
                                request, rent_id=rent_id, user_id=user_id, hw_action_id=hw_action_object.get('id'),
                                proto_field=hw_action_object.get('proto_field'),
                                field_type='bool',
                                value='true',
                                hw_module_id=hw_module_object.get('id'),
                                traceable_object_id=traceable_object.get('id'),
                                ack_message=True,
                                date_from=date_from,
                                date_to=date_to, active=True)

                            if rent_obj:
                                ret_val['data'] = rent_obj
                                ret_val['success'] = True
                                status = 201
                                ret_val['message'] = 'server.object_created'

                        else:
                            status = 412
                            ret_val['message'] = 'server.query_condition_failed'
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
            logger.error('Function api_rent_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_rent_blueprint.route('/<rent_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['rent:delete'], require_all=True, require_all_actions=True)
async def api_rent_element_delete(request: Request, user, rent_id: int = 0):
    """

    :param request:
    :param user:
    :param rent_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):

                    if True and rent_id:
                        rent = await delete_rent_element(request, rent_id)

                        if rent:
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
            logger.error('Function api_rent_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
