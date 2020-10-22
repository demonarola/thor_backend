#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic import response
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, scoped
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int
from web_backend.nvlserver.helper.request_wrapper import populate_response_format

from .service import (
    # IMPORT POINT SERVICES
    get_nvl_point_list, get_nvl_point_list_count, get_nvl_point_element,
    create_nvl_point_element, update_nvl_point_element, delete_nvl_point_element,
    # IMPORT LINESTRING SERVICES
    get_nvl_linestring_list, get_nvl_linestring_list_count, get_nvl_linestring_element,
    create_nvl_linestring_element, update_nvl_linestring_element, delete_nvl_linestring_element,
    # IMPORT CIRCLE SERVICES
    get_nvl_circle_list, get_nvl_circle_list_count, get_nvl_circle_element,
    create_nvl_circle_element, update_nvl_circle_element, delete_nvl_circle_element,
    # IMPORT POLYGON SERVICES
    get_nvl_polygon_list, get_nvl_polygon_list_count, get_nvl_polygon_element,
    create_nvl_polygon_element, update_nvl_polygon_element, delete_nvl_polygon_element,
)

api_nvl_cartography_blueprint = Blueprint('nvl_cartography', url_prefix='/api/nvl_cartography')


# NVL POINT CONTROLLER
@api_nvl_cartography_blueprint.route('/nvl_point', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_point(
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
    label = request.args.get('label', None)
    user_id = request.args.get('user_id', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):

                    point_list = await get_nvl_point_list(
                        request, label=label,
                        user_id=user_id, limit=size, offset=offset)
                    point_list_count = await get_nvl_point_list_count(
                        request, label=label, user_id=user_id)

                    if point_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            point_list, point_list_count, size=size, page=page)
                        ret_val['data'] = res_data_formatted
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
            logger.error('Function api_subscription_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_point', methods=['POST'])
@inject_user()
@scoped(['map:create'], require_all=True, require_all_actions=True)
async def api_nvl_point_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    icon = request.json.get('icon', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('date_from', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'POST':
        try:
            if user:
                if user.get('user_id'):
                    if user.get('user_id'):
                        if None not in [geom, user_id]:
                            nvl_point_element = await create_nvl_point_element(
                                request, geom=geom, label=label,
                                color=color, icon=icon,
                                location_id=location_id, user_id=user_id,
                                meta_information=meta_information, active=active)

                            if nvl_point_element:
                                ret_val['data'] = nvl_point_element
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
            logger.error('Function api_subscription_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_point/<nvl_point_id:int>', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_point_element(
        request: Request,
        user,
        nvl_point_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_point_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:
            if user.get('user_id', None) and nvl_point_id:

                nvl_point_element = await get_nvl_point_element(
                    request, nvl_point_id=nvl_point_id)

                if nvl_point_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = nvl_point_element
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


@api_nvl_cartography_blueprint.route('/nvl_point/<nvl_point_id:int>', methods=['PUT'])
@inject_user()
@scoped(['map:update'], require_all=True, require_all_actions=True)
async def api_nvl_point_element(
        request: Request,
        user,
        nvl_point_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_point_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    icon = request.json.get('icon', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('date_from', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'PUT':
        if user:

            if user.get('user_id', None) and nvl_point_id:

                nvl_point_element = await update_nvl_point_element(
                    request, nvl_point_id=nvl_point_id, geom=geom, label=label, color=color, icon=icon,
                    location_id=location_id, user_id=user_id,
                    meta_information=meta_information, active=active)

                if nvl_point_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = nvl_point_element
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


@api_nvl_cartography_blueprint.route('/nvl_point/<nvl_point_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['map:delete'], require_all=True, require_all_actions=True)
async def api_nvl_point_element(
        request: Request,
        user,
        nvl_point_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_point_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        if user:

            if user.get('user_id'):

                if nvl_point_id:
                    # TODO: ADD DELETION OF ALL ELEMENTS THAT USE LANG AS FOREIGN KEY
                    nvl_point_element = await delete_nvl_point_element(request, nvl_point_id)
                    if nvl_point_element:
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

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# NVL LINESTRING CONTROLLER
@api_nvl_cartography_blueprint.route('/nvl_linestring', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_linestring(
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
    label = request.args.get('label', None)
    user_id = request.args.get('user_id', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):

                    linestring_list = await get_nvl_linestring_list(
                        request, label=label,
                        user_id=user_id, limit=size, offset=offset)
                    linestring_list_count = await get_nvl_linestring_list_count(
                        request, label=label, user_id=user_id)

                    if linestring_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            linestring_list, linestring_list_count, size=size, page=page)
                        ret_val['data'] = res_data_formatted
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
            logger.error('Function api_subscription_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_linestring', methods=['POST'])
@inject_user()
@scoped(['map:create'], require_all=True, require_all_actions=True)
async def api_nvl_linestring_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('user_id', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'POST':
        try:
            if user:
                if user.get('user_id'):
                    if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':

                        if None in [user_id, geom, label]:
                            nvl_linestring_element = await create_nvl_linestring_element(
                                request, geom=geom, label=label,
                                color=color, location_id=location_id, user_id=user_id,
                                meta_information=meta_information, active=active)

                            if nvl_linestring_element:
                                ret_val['data'] = nvl_linestring_element
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
            logger.error('Function api_subscription_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_linestring/<nvl_linestring_id:int>', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_linestring_element(
        request: Request,
        user,
        nvl_linestring_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_linestring_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:

            if user.get('user_id', None) and nvl_linestring_id:
                if user.get('account_type_name') == 'admin':
                    nvl_linestring_element = await get_nvl_linestring_element(
                        request, user_id=None, nvl_linestring_id=nvl_linestring_id)
                else:
                    nvl_linestring_element = await get_nvl_linestring_element(
                        request, user_id=user.get('user_id'), nvl_linestring_id=nvl_linestring_id)

                if nvl_linestring_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = nvl_linestring_element
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


@api_nvl_cartography_blueprint.route('/nvl_linestring/<nvl_linestring_id:int>', methods=['PUT'])
@inject_user()
@scoped(['map:update'], require_all=True, require_all_actions=True)
async def api_nvl_linestring_element(
        request: Request,
        user,
        nvl_linestring_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_linestring_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    location_id = request.json.get('location_id', None)
    user_data_id = request.json.get('user_id', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'PUT':
        if user:

            if user.get('user_id', None) and nvl_linestring_id:
                if user.get('account_type_name') == 'admin':
                    user_id = user_data_id
                else:
                    user_id = user.get('user_id')

                nvl_linestring_element = await update_nvl_linestring_element(
                    request, user_id=user_id, nvl_linestring_id=nvl_linestring_id, geom=geom, label=label,
                    color=color, location_id=location_id,
                    meta_information=meta_information, active=active)

                if nvl_linestring_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = nvl_linestring_element
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


@api_nvl_cartography_blueprint.route('/nvl_linestring/<nvl_linestring_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['map:delete'], require_all=True, require_all_actions=True)
async def api_nvl_linestring_element(
        request: Request,
        user,
        nvl_linestring_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_linestring_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        if user:

            if user.get('user_id'):

                if nvl_linestring_id:

                    if user.get('account_type_name') == 'admin':
                        user_id = None
                    else:
                        user_id = user.get('user_id')

                    nvl_linestring_element = await delete_nvl_linestring_element(
                        request, user_id=user_id, nvl_linestring_id=nvl_linestring_id)

                    if nvl_linestring_element:
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

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# NVL CIRCLE CONTROLLER
@api_nvl_cartography_blueprint.route('/nvl_circle', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_circle(
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
    user_id = request.args.get('user_id', None)
    label = request.args.get('label', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    circle_list = await get_nvl_circle_list(
                        request, user_id=user_id, label=label,
                        limit=size, offset=offset)
                    circle_list_count = await get_nvl_circle_list_count(
                        request, user_id=user_id, label=label)

                    if circle_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            circle_list, circle_list_count, size=size, page=page)
                        ret_val['data'] = res_data_formatted
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
            logger.error('Function api_subscription_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_circle', methods=['POST'])
@inject_user()
@scoped(['map:create'], require_all=True, require_all_actions=True)
async def api_nvl_circle_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('user_id', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'POST':
        try:
            if user:
                if user.get('user_id'):
                    if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':

                        nvl_circle_element = await create_nvl_circle_element(
                            request, user_id=user_id, geom=geom, label=label,
                            color=color, location_id=location_id,
                            meta_information=meta_information, active=active)

                        if nvl_circle_element:
                            ret_val['data'] = nvl_circle_element
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
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_subscription_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_circle/<nvl_circle_id:int>', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_circle_element(request, user, nvl_circle_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_circle_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:

            if user.get('user_id', None):
                if user.get('account_type_name') == 'admin':
                    user_id = None
                else:
                    user_id = user.get('user_id')

                nvl_circle_element = await get_nvl_circle_element(request, user_id, nvl_circle_id)

                if nvl_circle_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = nvl_circle_element
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


@api_nvl_cartography_blueprint.route('/nvl_circle/<nvl_circle_id:int>', methods=['PUT'])
@inject_user()
@scoped(['map:update'], require_all=True, require_all_actions=True)
async def api_nvl_circle_element(
        request,
        user,
        nvl_circle_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_circle_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('user_id', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'PUT':
        if user:

            if user.get('user_id', None) and nvl_circle_id:
                if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':
                    nvl_circle_element = await update_nvl_circle_element(
                        request, user_id=user_id, nvl_circle_id=nvl_circle_id, geom=geom, label=label,
                        color=color, location_id=location_id,
                        meta_information=meta_information, active=active)

                    if nvl_circle_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = nvl_circle_element
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        status = 200
                else:
                    status = 412
                    ret_val['message'] = 'server.query_condition_failed'
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


@api_nvl_cartography_blueprint.route('/nvl_circle/<nvl_circle_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['map:delete'], require_all=True, require_all_actions=True)
async def api_nvl_circle_element(
        request,
        user,
        nvl_circle_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_circle_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        if user:
            if user.get('user_id'):

                if nvl_circle_id:
                    if user.get('account_type_name') == 'admin':
                        user_id = None
                    else:
                        user_id = user.get('user_id')
                    # TODO: ADD DELETION OF ALL ELEMENTS THAT USE LANG AS FOREIGN KEY
                    nvl_circle_element = await delete_nvl_circle_element(
                        request, user_id=user_id, nvl_circle_id=nvl_circle_id)
                    if nvl_circle_element:
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

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# NVL POLYGON CONTROLLER
@api_nvl_cartography_blueprint.route('/nvl_polygon', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_polygon(
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
    label = request.args.get('label', None)
    user_id = request.args.get('user_id', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    circle_polygon = await get_nvl_polygon_list(
                        request, user_id=user_id, label=label,
                        limit=size, offset=offset)
                    circle_polygon_count = await get_nvl_circle_list_count(
                        request, user_id=user_id, label=label)

                    if circle_polygon:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            circle_polygon, circle_polygon_count, size=size, page=page)
                        ret_val['data'] = res_data_formatted
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
            logger.error('Function api_subscription_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_polygon', methods=['POST'])
@inject_user()
@scoped(['map:create'], require_all=True, require_all_actions=True)
async def api_nvl_polygon_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('user_id', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id'):
                    if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':

                        nvl_polygon_element = await create_nvl_polygon_element(
                            request, user_id=user_id, geom=geom, label=label,
                            color=color, location_id=location_id,
                            meta_information=meta_information, active=active)

                        if nvl_polygon_element:
                            ret_val['data'] = nvl_polygon_element
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = 'server.object_created'

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
            logger.error('Function api_subscription_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_cartography_blueprint.route('/nvl_polygon/<nvl_polygon_id:int>', methods=['GET'])
@inject_user()
@scoped(['map:read'], require_all=True, require_all_actions=True)
async def api_nvl_polygon_element(
        request: Request,
        user,
        nvl_polygon_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_polygon_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:

            if user.get('user_id', None) and nvl_polygon_id:
                if user.get('account_type_name') == 'admin':
                    user_id = None
                else:
                    user_id = user.get('user_id')

                nvl_polygon_element = await get_nvl_polygon_element(
                    request, user_id=user_id, nvl_polygon_id=nvl_polygon_id)

                if nvl_polygon_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = nvl_polygon_element
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


@api_nvl_cartography_blueprint.route('/nvl_polygon/<nvl_polygon_id:int>', methods=['PUT'])
@inject_user()
@scoped(['map:update'], require_all=True, require_all_actions=True)
async def api_nvl_polygon_element(
        request,
        user,
        nvl_polygon_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_polygon_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    geom = request.json.get('geom', None)
    label = request.json.get('label', None)
    color = request.json.get('color', None)
    location_id = request.json.get('location_id', None)
    user_id = request.json.get('user_id', None)
    meta_information = request.json.get('meta_information', {})
    active = request.json.get('active', True)

    if request.method == 'PUT':
        if user:

            if user.get('user_id', None) and nvl_polygon_id:
                if user_id == user.get('user_id') or user.get('account_type_name') == 'admin':
                    nvl_polygon_element = await update_nvl_polygon_element(
                        request, nvl_polygon_id=nvl_polygon_id, user_id=user_id, geom=geom, label=label,
                        color=color, location_id=location_id,
                        meta_information=meta_information, active=active)

                    if nvl_polygon_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = nvl_polygon_element
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        status = 200
                else:
                    status = 412
                    ret_val['message'] = 'server.query_condition_failed'
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


@api_nvl_cartography_blueprint.route('/nvl_polygon/<nvl_polygon_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['map:delete'], require_all=True, require_all_actions=True)
async def api_nvl_polygon_element(
        request: Request,
        user,
        nvl_polygon_id: int = 0):
    """

    :param request:
    :param user:
    :param nvl_polygon_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        if user:

            if user.get('user_id'):

                if nvl_polygon_id:
                    if user.get('account_type_name') == 'admin':
                        user_id = None
                    else:
                        user_id = user.get('user_id')

                    nvl_polygon_element = await delete_nvl_polygon_element(
                        request, user_id=user_id, nvl_polygon_id=nvl_polygon_id)

                    if nvl_polygon_element:
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

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
