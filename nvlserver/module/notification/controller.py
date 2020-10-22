#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'
import ujson
from sanic import Blueprint
from sanic import response
from sanic.request import Request
from sanic_jwt import inject_user, scoped

from .service import (
    get_notification_element, get_notification_list,
    delete_notification_element, update_notification_element_read, get_notification_unread_count
)


api_notification_blueprint = Blueprint('api_notification', url_prefix='/api/notification')


@api_notification_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_notification(
        request: Request,
        user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': {'all': [], 'byId': {}}}

    if request.method == 'GET':
        # if user:
        if True:

            # if user.get('user_id') and user.get('is_superuser'):
            if True:

                notification_list = await get_notification_list(request)

                if notification_list:
                    not_data = {'all': [x.get('id') for x in notification_list], 'byId': {}}
                    for x in notification_list:
                        not_data['byId'].update({x.get('id'): x})

                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = not_data
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


@api_notification_blueprint.route('/unread_count', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_notification_unread_count(
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
        # if user:
        if True:

            # if user.get('user_id') and user.get('is_superuser'):
            if True:

                unread_count = await get_notification_unread_count(request)

                if unread_count:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = unread_count
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


@api_notification_blueprint.route('/<notification_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_notification_element(
        request: Request,
        user,
        notification_id: int = 0):
    """

    :param request:
    :param user:
    :param notification_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        # if user:
        if True:

            # if user.get('user_id', None) and notification_id and user.get('is_superuser'):
            if True:

                notification_element = await get_notification_element(request, notification_id)

                if notification_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = {notification_element.get('id'): notification_element}
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


@api_notification_blueprint.route('/<notification_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_notification_element(
        request: Request,
        user,
        notification_id: int = 0):
    """

    :param request:
    :param user:
    :param notification_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        # if user:
        if True:

            # if user.get('user_id', None) and notification_id and user.get('is_superuser'):
            if True:

                notification_element = await update_notification_element_read(request, notification_id)

                if notification_element:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = {notification_element.get('id'): notification_element}
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


@api_notification_blueprint.route('/<notification_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_notification_element(
        request: Request,
        user,
        notification_id: int = 0):
    """

    :param request:
    :param user:
    :param notification_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        # if user:
        if True:

            # if user.get('user_id'):
            if True:

                notification = get_notification_element(request, notification_id)
                if notification:
                    # and user.get('is_superuser'):
                    # TODO: ADD DELETION OF ALL ELEMENTS THAT USE LANG AS FOREIGN KEY
                    deleted_elem = await delete_notification_element(request, notification_id)
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

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
