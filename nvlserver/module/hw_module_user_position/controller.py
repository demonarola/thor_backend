#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson
import iso8601
import time
from sanic import Blueprint
from sanic import response
from geojson import FeatureCollection
from sanic.request import Request
from sanic_jwt import inject_user

from .service import (
    get_hw_module_user_position_element,
    get_hw_module_user_position_linestring_list,
    get_hw_module_user_position_last_point_list,
    delete_hw_module_user_position_all,
    get_hw_module_user_position_last_point_element_by_traceable_object_id,
    get_hw_module_user_position_linestring_list_timed
)
from web_backend.nvlserver.module.hw_module.service import get_hw_module_element_by_traceable_object_id


api_hw_module_user_position_blueprint = Blueprint(
    'api_hw_module_user_position', url_prefix='/api/hw_module_user_position')


@api_hw_module_user_position_blueprint.route('/line', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_user_position_linestring_list_get(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    vehicles = request.args.get('vehicles', None)
    user_id = request.args.get('user_id', None)
    vehicle_list = None
    date_from_front = request.args.get('date_from', None)
    date_to_front = request.args.get('date_to', None)
    # print(date_from_front)
    # print(date_to_front)
    # TODO: REMOVE REPLACE ON CHANGE PARAM FROM FRONTEND
    if date_from_front is not None:
        date_from = iso8601.parse_date(date_from_front.replace(' ', '+'))
    else:
        date_from = None
    if date_to_front is not None:
        date_to = iso8601.parse_date(date_to_front.replace(' ', '+'))
    else:
        date_to = None

    if request.method == 'GET':
        if user:
            if user.get('user_id', None):
                if user.get('account_type_name') in ['admin', 'billing']:
                    user_id = user_id
                else:
                    user_id = user.get('user_id')

                if vehicles:
                    vehicle_list = vehicles.split(',')

                if date_from is not None and date_to is not None:
                    if vehicle_list:
                        vehicle_list = [int(x) for x in vehicle_list]
                        hw_module_linestring_list = await get_hw_module_user_position_linestring_list_timed(
                            request, user_id=user_id, date_from=date_from, date_to=date_to,
                            hw_module_id=tuple(vehicle_list))
                    else:
                        hw_module_linestring_list = await get_hw_module_user_position_linestring_list_timed(
                            request, user_id=user_id, date_from=date_from, date_to=date_to,
                            hw_module_id=None)
                else:
                    if vehicle_list:
                        vehicle_list = [int(x) for x in vehicle_list]
                        hw_module_linestring_list = await get_hw_module_user_position_linestring_list(
                            request, user_id=user_id, map_pool_time=user.get('map_pool_time', 900),
                            hw_module_id=tuple(vehicle_list))
                    else:
                        hw_module_linestring_list = await get_hw_module_user_position_linestring_list(
                            request, user_id=user_id, map_pool_time=user.get('map_pool_time', 900),
                            hw_module_id=None)

                if hw_module_linestring_list:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = FeatureCollection(
                                features=hw_module_linestring_list,
                                property={'layer_type': 'line'})
                    status = 200
                else:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = FeatureCollection(
                                features=[],
                                property={'layer_type': 'line'})
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


@api_hw_module_user_position_blueprint.route('/point', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_user_position_last_point_get(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    vehicles = request.args.get('vehicles', None)
    user_id = request.args.get('user_id', None)
    vehicle_list = None

    if request.method == 'GET':
        if user:
            if user.get('user_id', None):
                if user.get('account_type_name') in ['admin', 'billing']:
                    user_id = user_id
                else:
                    user_id = user.get('user_id')
                if vehicles:
                    vehicle_list = vehicles.split(',')

                if vehicle_list:
                    vehicle_list = [int(x) for x in vehicle_list]
                    hw_module_last_point_list = await get_hw_module_user_position_last_point_list(
                        request, user_id=user_id, hw_module_id_list=tuple(vehicle_list))
                else:
                    hw_module_last_point_list = await get_hw_module_user_position_last_point_list(
                        request, user_id=user_id, hw_module_id_list=tuple())

                if hw_module_last_point_list:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = FeatureCollection(
                                features=hw_module_last_point_list,
                                property={'layer_type': 'point'})
                    status = 200
                else:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = FeatureCollection(
                                features=[],
                                property={'layer_type': 'point'})
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


@api_hw_module_user_position_blueprint.route('/line/<traceable_object_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_user_position_linestring_list_get(
        request: Request,
        user,
        traceable_object_id: int = 0):
    """

    :param request:
    :param traceable_object_id:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    hw_module_id = None

    if request.method == 'GET':
        if user:

            if user.get('user_id', None):

                if traceable_object_id:
                    traceable_object = await get_hw_module_element_by_traceable_object_id(
                        request, user_id=user.get('user_id'), traceable_object_id=traceable_object_id)
                    if traceable_object:
                        hw_module_id = (
                            traceable_object.get('module_id') if traceable_object.get('module_id') != '' else None)

                hw_module_linestring_list = await get_hw_module_user_position_linestring_list(
                    request, user_id=user.get('user_id'), hw_module_id=hw_module_id)

                if hw_module_linestring_list:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = FeatureCollection(
                                features=hw_module_linestring_list,
                                property={'layer_type': 'line'})
                    status = 200
                else:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = FeatureCollection(
                                features=[],
                                property={'layer_type': 'line'})
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


@api_hw_module_user_position_blueprint.route('/point/<traceable_object_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_user_position_last_point_get(
        request: Request,
        user,
        traceable_object_id: int = 0):
    """

    :param request:
    :param traceable_object_id:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id_front = request.args.get('user_id', None)

    if request.method == 'GET':
        if user:
            if user.get('user_id', None):
                if user.get('account_type') == 'admin':
                    user_id = user_id_front
                else:
                    user_id = user.get('user_id', None)

                if traceable_object_id:

                    t2 = time.time()

                    hw_module_last_point = await get_hw_module_user_position_last_point_element_by_traceable_object_id(
                        request, user_id=user_id, traceable_object_id=traceable_object_id)
                    t3 = time.time()
                    print(t3-t2)
                    if hw_module_last_point:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = FeatureCollection(
                                    features=[hw_module_last_point],
                                    property={'layer_type': 'point'})
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = FeatureCollection(
                                    features=[],
                                    property={'layer_type': 'point'})
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


@api_hw_module_user_position_blueprint.route('/<hw_module_user_position_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_user_position_element_get(
        request: Request,
        user,
        hw_module_user_position_id: int = 0):
    """

    :param request:
    :param user:
    :param hw_module_user_position_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:

            if user.get('user_id', None) and hw_module_user_position_id:

                hw_module_position_element = await get_hw_module_user_position_element(
                    request, hw_module_user_position_id)

                if hw_module_position_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = hw_module_position_element
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


@api_hw_module_user_position_blueprint.route('/delete_all', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_user_position_delete_all(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:
            if user.get('user_id', None):
                all_deleted = await delete_hw_module_user_position_all(request)

                if all_deleted:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = None

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
