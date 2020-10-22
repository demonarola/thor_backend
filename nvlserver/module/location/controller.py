#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson
import iso8601
from sanic import Blueprint
from sanic import response
from sanic.log import logger
from geojson import FeatureCollection
from sanic.request import Request
from sanic_jwt import inject_user, scoped

from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

from .service import (
    # IMPORT LOCATION SERVICES
    get_location_element, get_location_list, get_location_list_count,
    delete_location_element, update_location_element, create_location_element,
    # IMPORT LOCATION TYPE SERVICES
    get_location_type_list, get_location_type_element, get_location_type_dropdown_list,
    delete_location_type_element, update_location_type_element,
    get_location_type_list_count, get_location_geography_list,
    process_location_geo_feature, get_location_type_element_by_name
)


api_location_blueprint = Blueprint('api_location', url_prefix='/api/location')


@api_location_blueprint.route('/geography', methods=['GET'])
@inject_user()
@scoped(['location:read'], require_all=True, require_all_actions=True)
async def api_location_geography(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = request.args.get('user_id', None)

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') in ['admin']:
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    location_list = await get_location_geography_list(request, user_id=user_id)

                    if location_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = FeatureCollection(
                                features=location_list,
                                property={'layer_type': 'location'})
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = FeatureCollection(
                                features=[],
                                property={'layer_type': 'location'})
                        status = 200
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_location_geography -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/geography/<user_id:int>', methods=['GET'])
@inject_user()
@scoped(['location:read'], require_all=True, require_all_actions=True)
async def api_location_geography_by_user_id(
        request: Request,
        user,
        user_id: int = 0):
    """

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    # user_id = request.args.get('user_id', None)

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') in ['admin']:
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')
                    location_list = await get_location_geography_list(request, user_id=user_id)

                    if location_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = FeatureCollection(
                                features=location_list,
                                property={'layer_type': 'location'})
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = FeatureCollection(
                                features=[],
                                property={'layer_type': 'location'})
                        status = 200
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_location_geography_by_user_id -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# LOCATION CONTROLLER
@api_location_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['location:read'], require_all=True, require_all_actions=True)
async def api_location(
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

                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')
                    # t1 = time.time()
                    location_list = await get_location_list(
                        request, user_id=user_id, name=name, limit=size, offset=offset)
                    # t2 = time.time()
                    location_list_count = await get_location_list_count(request, user_id=user_id, name=name)
                    # t3 = time.time()

                    if location_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        # t4 = time.time()
                        res_data_formatted = await populate_response_format(
                            location_list, location_list_count, size=size, page=page)
                        # t5 = time.time()
                        ret_val['data'] = res_data_formatted
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = {}
                        status = 200
                    # print('LOC_LIST: {} | LOC_LIST_CNT: {} | RES_DTA_FORMATED: {}'.format((t2-t1), (t3-t2), (t5-t4)))
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_location -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/', methods=['POST'])
@inject_user()
@scoped(['location:create'], require_all=True, require_all_actions=True)
async def api_location_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """

    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    name = request.json.get('name', None)
    user_id = request.json.get('user_id', None)
    location_type = request.json.get('location_type', None)
    action_list = request.json.get('action', [])
    module_list = request.json.get('modules', [])
    date_from_front = request.json.get('date_from', None)
    date_to_front = request.json.get('date_to', None)
    label = request.json.get('label', None)
    radius = request.json.get('radius', None)
    color = request.json.get('color', '')
    icon = request.json.get('icon', None)
    coordinates = request.json.get('coordinates', [])
    show_on_map = request.json.get('show_on_map', False)
    active = request.json.get('active', False)

    if date_from_front is not None:
        date_from = iso8601.parse_date(date_from_front)
    else:
        date_from = None
    if date_to_front is not None:
        date_to = iso8601.parse_date(date_to_front)
    else:
        date_to = None

    if request.method == 'POST':
        try:
            if user:
                if user.get('user_id'):
                    if user.get('account_type_name') == 'admin':
                        if user_id is None:
                            user_id = user.get('user_id')
                        else:
                            user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    if user.get('user_id') and None not in [coordinates, user_id, label]:

                        location_type_element = await get_location_type_element_by_name(request, location_type)
                        location_element = await create_location_element(
                            request, name=name,
                            location_type_id=location_type_element.get('id'), user_id=user_id,
                            meta_information={'modules': module_list}, show_on_map=show_on_map, active=active)

                        if location_element:

                            proc_gof = await process_location_geo_feature(
                                request, location_element=location_element,
                                label=label, coordinates=coordinates, icon=icon, color=color, radius=radius,
                                date_from=date_from, date_to=date_to, action_list=action_list
                            )

                            if proc_gof:
                                ret_val['data'] = location_element
                                ret_val['success'] = True
                                status = 201
                                ret_val['message'] = 'server.object_created'
                            else:
                                await delete_location_element(
                                    request, user_id=user_id, location_id=location_element.get('id'))

                    else:
                        status = 400
                        ret_val['message'] = 'server.bad_request'

                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_location_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/<location_id:int>', methods=['GET'])
@inject_user()
@scoped(['location:read'], require_all=True, require_all_actions=True)
async def api_location_element(
        request: Request,
        user,
        location_id: int = 0):
    """

    :param request:
    :param user:
    :param location_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = request.args.get('user_id', None)

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    location_element = await get_location_element(
                        request, user_id=user_id, location_id=location_id)
                    # print(location_element)

                    if location_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = location_element
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
            logger.error('Function api_location_element -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/<location_id:int>', methods=['PUT'])
@inject_user()
@scoped(['location:update'], require_all=True, require_all_actions=True)
async def api_location_element_put(
        request: Request,
        user,
        location_id: int = 0):
    """

    :param request:
    :param user:
    :param location_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.json.get('name', None)
    # SUBSTITUTE WITH USER MANAGEMENT
    user_id = request.json.get('user_id', None)
    location_type = request.json.get('location_type', None)
    # module_id = request.json.get('module_id', None)
    action_list = request.json.get('action', [])
    module_list = request.json.get('modules', [])
    date_from_front = request.json.get('date_from', None)
    date_to_front = request.json.get('date_to', None)
    label = request.json.get('label', None)
    radius = request.json.get('radius', None)
    color = request.json.get('color', '')
    icon = request.json.get('icon', None)
    coordinates = request.json.get('coordinates', [])
    # traceable_object_id = request.json.get('traceable_object_id', None)
    show_on_map = request.json.get('show_on_map', False)
    active = request.json.get('active', False)

    if date_from_front is not None:
        date_from = iso8601.parse_date(date_from_front)
    else:
        date_from = None
    if date_to_front is not None:
        date_to = iso8601.parse_date(date_to_front)
    else:
        date_to = None

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id', None) and location_id:
                    if user.get('account_type_name') == 'admin':
                        if user_id is None:
                            user_id = user.get('user_id')
                    else:
                        user_id = user.get('user_id')
                    print('prosao user detecion')
                    if user.get('user_id') and None not in [label]:
                        location_type_element = await get_location_type_element_by_name(request, location_type)
                        location_element = await update_location_element(
                            request, location_id=location_id, name=name,
                            location_type_id=location_type_element.get('id'), user_id=user_id,
                            meta_information={'modules': module_list}, show_on_map=show_on_map, active=active)

                        if location_element:
                            print('process location geo_feature called')
                            proc_gof = await process_location_geo_feature(
                                request, location_element=location_element,
                                label=label, coordinates=coordinates, icon=icon, color=color, radius=radius,
                                date_from=date_from, date_to=date_to, action_list=action_list
                            )

                            if proc_gof:
                                ret_val['data'] = location_element
                                ret_val['success'] = True
                                status = 201
                                ret_val['message'] = 'server.object_created'
                            else:
                                await delete_location_element(
                                    request, user_id=user_id, location_id=location_element.get('id'))
                    else:
                        status = 400
                        ret_val['message'] = 'server.bad_request'
                else:
                    status = 412
                    ret_val['message'] = 'server.query_condition_failed'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_location_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/<location_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['location:delete'], require_all=True, require_all_actions=True)
async def api_location_element_delete(
        request: Request,
        user,
        location_id: int = 0):
    """

    :param request:
    :param user:
    :param location_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    user_id = proc_arg_to_int(request.args.get('user_id', '0'), 0)

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    location = await get_location_element(request, user_id, location_id)
                    if location:
                        # print('LOCATION :{}'.format(location))
                        # TODO: ADD DELETION OF ALL ELEMENTS THAT USE LANG AS FOREIGN KEY
                        deleted_elem = await delete_location_element(request, user_id, location_id)
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
            logger.error('Function api_location_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# LOCATION TYPE CONTROLLER
@api_location_blueprint.route('/type', methods=['GET'])
@inject_user()
@scoped(['location:read'], require_all=True, require_all_actions=True)
async def api_location_type(
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
                    location_type_list = await get_location_type_list(request, name=name, limit=size, offset=offset)
                    location_type_list_count = await get_location_type_list_count(request, name=name)

                    if location_type_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            location_type_list, location_type_list_count, size=size, page=page)
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
            logger.error('Function api_location_type -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/type/dropdown', methods=['GET'])
@inject_user()
@scoped(['location:query_dropdown'], require_all=True, require_all_actions=True)
async def api_location_type_dropdown_get(
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

                    location_type_list = await get_location_type_dropdown_list(
                        request, name=name)

                    if location_type_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = location_type_list
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
            logger.error('Function api_location_type_dropdown_get -> GET erred with: {}'.format(al_err))
    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/type', methods=['POST'])
@inject_user()
@scoped(['location:create'], require_all=True, require_all_actions=True)
async def api_location_type_post(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.json.get('name', None)
    active = request.json.get('active', False)

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id'):

                    location_type_element = await create_location_element(
                        request, name=name, active=active)

                    if location_type_element:
                        ret_val['data'] = location_type_element
                        ret_val['success'] = True
                        status = 201
                        ret_val['message'] = 'server.object_created'

                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as al_err:
            logger.error('Function api_location_type_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/type/<location_type_id:int>', methods=['GET'])
@inject_user()
@scoped(['location:read'], require_all=True, require_all_actions=True)
async def api_location_type_element(
        request: Request,
        user,
        location_type_id: int = 0):
    """

    :param request:
    :param user:
    :param location_type_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None) and location_type_id:

                    location_type_element = await get_location_type_element(request, location_type_id)

                    if location_type_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = location_type_element
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
            logger.error('Function api_location_type_element -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/type/<location_type_id:int>', methods=['PUT'])
@inject_user()
@scoped(['location:update'], require_all=True, require_all_actions=True)
async def api_location_type_element_put(
        request: Request,
        user,
        location_type_id: int = 0):
    """

    :param request:
    :param user:
    :param location_type_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    name = request.json.get('name', None)
    active = request.json.get('active', False)

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id', None) and location_type_id:
                    location_type_element = await update_location_type_element(
                        request, location_type_id=location_type_id, name=name, active=active)

                    if location_type_element:
                        ret_val['data'] = location_type_element
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
            logger.error('Function api_location_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_location_blueprint.route('/type/<location_type_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['location:delete'], require_all=True, require_all_actions=True)
async def api_location_type_element_delete(
        request: Request,
        user,
        location_type_id: int = 0):
    """

    :param request:
    :param user:
    :param location_type_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):

                    if location_type_id:

                        # TODO: ADD DELETION OF ALL ELEMENTS THAT USE LANG AS FOREIGN KEY
                        deleted_elem = await delete_location_type_element(request, location_type_id)
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
            logger.error('Function api_location_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
