#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'
import ujson
from sanic import Blueprint
from sanic import response
from sanic.request import Request
from sanic_jwt import inject_user, scoped, protected

from .service import get_town_list, create_town_element, get_town_element, update_town_element, delete_town_element

api_town_blueprint = Blueprint('api_town', url_prefix='/api/town')


@api_town_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_town_get(request: Request, user):
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
                town_list = await get_town_list(request)

                if town_list:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = town_list
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


@api_town_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_town_post(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'POST':
        if user:
            if user.get('user_id'):
                if user.get('user_id') and user.get('is_superuser'):
                    name = request.json.get('name', None)
                    country_id = request.json.get('country_id', None)

                    if None not in [name, country_id]:
                        town = await create_town_element(request, name, country_id, True)

                        ret_val['data'] = town
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


@api_town_blueprint.route('/<town_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_town_element_get(request: Request, user, town_id: int = 0):
    """

    :param request:
    :param user:
    :param town_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        if user:

            if user.get('user_id', None) and town_id:

                town_element = await get_town_element(request, town_id)

                if town_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = town_element
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

    if request.method == 'PUT':
        if user:

            if user.get('user_id'):
                # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                if True and town_id:
                    name = request.json.get('name', None)
                    country_id = request.json.get('country_id', None)
                    if None not in [name, country_id]:
                        town = await update_town_element(request, town_id, name, country_id)

                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = town
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

    if request.method == 'DELETE':
        if user:

            if user.get('user_id'):
                # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                if True and town_id:
                    await delete_town_element(request, town_id)

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


@api_town_blueprint.route('/<town_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_town_element_put(request: Request, user, town_id: int = 0):
    """

    :param request:
    :param user:
    :param town_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        if user:

            if user.get('user_id'):
                # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                if True and town_id:
                    name = request.json.get('name', None)
                    country_id = request.json.get('country_id', None)
                    if None not in [name, country_id]:
                        town = await update_town_element(request, town_id, name, country_id)

                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = town
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

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_town_blueprint.route('/<town_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_town_element_delete(request: Request, user, town_id: int = 0):
    """

    :param request:
    :param user:
    :param town_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        if user:

            if user.get('user_id'):
                # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                if True and town_id:
                    await delete_town_element(request, town_id)

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
