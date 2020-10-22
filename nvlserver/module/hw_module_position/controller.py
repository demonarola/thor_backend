#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic import response
from geojson import FeatureCollection
from sanic.request import Request
from sanic_jwt import inject_user

from .service import (
    get_hw_module_position_last_point_list, delete_hw_module_all_positions
)
from web_backend.nvlserver.module.hw_module.service import get_hw_module_element_by_traceable_object_id


api_hw_module_position_blueprint = Blueprint('api_hw_module_position', url_prefix='/api/hw_module_position')


@api_hw_module_position_blueprint.route('/point/<traceable_object_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_position_last_point_get(
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
                    traceable_object = await get_hw_module_element_by_traceable_object_id(request, traceable_object_id)
                    if traceable_object:
                        hw_module_id = (
                            traceable_object.get('module_id') if traceable_object.get('module_id') != '' else None)

                hw_module_last_point_list = await get_hw_module_position_last_point_list(
                    request, user_id=user.get('user_id'), hw_module_id=hw_module_id)

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


@api_hw_module_position_blueprint.route('/delete_all', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_hw_module_position_delete_all(
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
                all_deleted = await delete_hw_module_all_positions(request)

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
