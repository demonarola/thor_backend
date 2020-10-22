#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
import ujson
from sanic import Blueprint
from sanic.response import raw
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, scoped, protected


from web_backend.nvlserver.security.helper import generate_password, check_password, update_password
from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int
from web_backend.nvlserver.security.helper import check_unique_by_column_name
from web_backend.nvlserver.module.timezone.service import get_timezone_element_by_name
from web_backend.nvlserver.security.helper import update_user_in_redis
from web_backend.nvlserver.security.helper import generate_new_access_token

from .service import (
    get_user_list, get_user_list_count, create_user_element, delete_user_element, update_user_element,
    get_user_element, get_user_by_id, get_user_list_by_fullname, update_user_element_timezone,
    update_user_element_map_pool_time
)

api_user_management_blueprint = Blueprint('api_user_management', url_prefix='/api/user_management')


@api_user_management_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['user:read'], require_all=True, require_all_actions=True)
async def api_user_get(request: Request, user):
    """ Get User list

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '10'), 10)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    email = request.args.get('email', None)
    fullname = request.args.get('fullname', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        """ Get User list."""
        try:
            if user:
                if user.get('user_id'):
                    user_list = await get_user_list(
                        request, email=email, fullname=fullname, limit=size, offset=offset)
                    user_list_count = await get_user_list_count(request, email=email, fullname=fullname)

                    if user_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            user_list, user_list_count, size=size, page=page)
                        ret_val['data'] = res_data_formatted
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = {}
                        status = 200
                else:
                    status = 400
                    ret_val['message'] = '400 Bad Request'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user -> GET erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
@scoped(['user:read'], require_all=True, require_all_actions=True)
async def api_user_get_dropdown(request: Request, user):
    """ Get User list

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    fullname = request.args.get('fullname', None)

    if request.method == 'GET':
        """ Get User list."""
        try:
            if user:
                if user.get('user_id'):
                    user_list = await get_user_list_by_fullname(request, fullname=fullname)

                    if user_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = user_list
                        status = 200
                    else:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = {}
                        status = 200
                else:
                    status = 400
                    ret_val['message'] = '400 Bad Request'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user -> GET erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/', methods=['POST'])
@inject_user()
@scoped(['user:create'], require_all=True, require_all_actions=True)
async def api_user_post(request: Request, user):
    """ Create User

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'POST':
        """ Create User element"""
        try:
            if user:
                if user.get('user_id', None) and user.get('account_type_name') == 'admin':

                    email = request.json.get('email', None)
                    password = request.json.get('password', None)
                    fullname = request.json.get('fullname', None)
                    language_id = request.json.get('language_id', None)
                    locked = request.json.get('locked', False)
                    account_type_id = request.json.get('account_type_id', None)
                    timezone = request.json.get('timezone_id', None)
                    map_pool_time = request.json.get('map_pool_time', None)
                    active = request.json.get('active', False)

                    q_pass = await generate_password(request, password)
                    if timezone is None:
                        timezone_element = await get_timezone_element_by_name(request, 'Europe/Zagreb')
                        timezone = timezone_element.get('id')

                    if None not in [email, q_pass, fullname, timezone, language_id, account_type_id]:
                        email_unique = await check_unique_by_column_name(request, user_ident=email)

                        if email_unique:
                            if q_pass:
                                user_element = await create_user_element(
                                    request, email=email, password=str(q_pass), fullname=fullname,
                                    locked=locked, language_id=language_id,
                                    timezone=timezone, map_pool_time=map_pool_time, account_type_id=account_type_id,
                                    active=active)
                                if user_element:
                                    user_data = await get_user_by_id(request, user_element.get('id'))
                                    await update_user_in_redis(request, user_element.get('id'))

                                    ret_val['data'] = user_data
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
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user -> POST erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/<user_id:int>', methods=['GET'])
@inject_user()
@scoped(['user:read'], require_all=True, require_all_actions=True)
async def api_user_element_get(request: Request, user, user_id: int = 0):
    """ Get User element / Update User element / Delete User element.

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status, ret_val = 404, {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        """ Get User element."""
        try:
            if user:
                if user.get('user_id', None) and user_id:
                    user_element = await get_user_element(request, user_id)
                    ret_val['data'] = user_element
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    status = 200
                else:
                    status = 400
                    ret_val['message'] = 'server.bad_request'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as au_err:
            logger.error('Function api_user_element erred with: {}'.format(au_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/<user_id:int>', methods=['PUT'])
@inject_user()
@scoped(['user:update'], require_all=True, require_all_actions=True)
async def api_user_element_put(request: Request, user, user_id: int = 0):
    """ Get User element / Update User element / Delete User element.

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status, ret_val = 500, {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        """ Edit User element."""
        try:
            if user:
                if user.get('user_id', None):
                    email = request.json.get('email', None)
                    password = request.json.get('password', None)
                    fullname = request.json.get('fullname', None)
                    language_id = request.json.get('language_id', None)
                    timezone = request.json.get('timezone_id', None)
                    map_pool_time = request.json.get('map_pool_time', None)
                    locked = request.json.get('locked', False)
                    account_type_id = request.json.get('account_type_id', None)
                    active = request.json.get('active', False)
                    if timezone is None:
                        timezone_element = await get_timezone_element_by_name(request, 'Europe/Zagreb')
                        timezone = timezone_element.get('id')

                    user_element = await get_user_by_id(request, user_id)

                    if password in [None, '']:
                        q_pass = user_element.get('password')
                    else:
                        q_pass = await generate_password(request, password)

                    if user_element.get('email') != email:
                        email_unique = await check_unique_by_column_name(request, user_ident=email)
                    else:
                        email_unique = True

                    # CHECK IF USER IS ADMIN AND THAT GENERATING USER IS OF THE SAME CUSTOMER

                    if None not in [email, fullname, timezone, language_id] and email_unique:
                        user_element = await update_user_element(
                            request, user_id=user_id, email=email, password=str(q_pass),
                            fullname=fullname, locked=locked, language_id=language_id,
                            timezone=timezone, map_pool_time=map_pool_time,
                            account_type_id=account_type_id, active=active)

                        if user_element:
                            user_data = await get_user_by_id(request, user_element.get('id'))
                            await update_user_in_redis(request, user_element.get('id'))
                            ret_val['data'] = user_data
                            status = 202
                            ret_val['success'] = True
                            ret_val['message'] = 'server.accepted'
                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'
                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as aue_err:
            logger.error('Function api_user_element -> PUT erred with: {}'.format(aue_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/<user_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['user:delete'], require_all=True, require_all_actions=True)
async def api_user_element_delete(request: Request, user, user_id: int = 0):
    """ Get User element / Update User element / Delete User element.

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status, ret_val = 500, {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        """ Delete User element."""
        try:
            if user:

                if user.get('user_id', None) and user.get('account_type_name') == 'admin':

                    user_data = await delete_user_element(request, user_id)

                    if user_data:
                        status = 202
                        ret_val['success'] = True
                        ret_val['message'] = 'server.accepted'

                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user_element -> DELETE erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/update_password/<user_id:int>', methods=['PUT'])
@inject_user()
@scoped(['user:update_password'], require_all=True, require_all_actions=True)
async def api_user_change_password_put(request: Request, user, user_id: int = 0):
    """ Update user password

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        # print(request, request.args, request.body)
        """ Update user password"""
        try:
            if user:
                if user.get('user_id', None) == user_id:

                    new_password = request.json.get('password', None)
                    old_password = request.json.get('old_password', None)

                    old_password_checked = await check_password(request, user.get('email'), old_password)

                    if old_password_checked and len(new_password) >= 4:
                        crypted_password = await generate_password(request, new_password)
                        await update_password(request, user.get('email'), str(crypted_password))
                        user_data = await get_user_by_id(request, user.get('user_id'))

                        ret_val['data'] = user_data
                        ret_val['success'] = True
                        status = 202
                        ret_val['message'] = 'server.accepted'

                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'
                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user_change_password_post -> POST erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/update_timezone/<user_id:int>', methods=['PUT'])
@inject_user()
@scoped(['user:update_timezone'], require_all=True, require_all_actions=True)
async def api_user_update_timezone_put(request: Request, user, user_id: int = 0):
    """ Update user timezone

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        # logger.error(request, request.args, request.body)
        """ Update user timezone"""
        try:
            if user:
                if user.get('user_id', None) == user_id:

                    timezone_id = request.json.get('timezone_id', None)

                    if timezone_id:
                        user_data = await update_user_element_timezone(
                            request, user_id=user.get('user_id'), timezone_id=timezone_id)
                        if user_data:
                            await update_user_in_redis(request, user_id)
                            access_token = await generate_new_access_token(request, user_id)

                            if user:
                                ret_val['data'] = access_token
                                ret_val['success'] = True
                                status = 202
                                ret_val['message'] = 'server.accepted'

                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'
                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user_update_timezone_put -> POST erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_user_management_blueprint.route('/update_map_pool_time/<user_id:int>', methods=['PUT'])
@inject_user()
@scoped(['user:update_map_pool_time'], require_all=True, require_all_actions=True)
async def api_user_update_map_pool_time_put(request: Request, user, user_id: int = 0):
    """ Create User

    :param request:
    :param user:
    :param user_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    # print(request.args, request)
    map_pool_time = proc_arg_to_int(request.json.get('map_pool_time', '5'), 5)

    if request.method == 'PUT':
        # print(request, request.args, request.body)
        """ Update user password"""
        try:
            if user:
                if user.get('user_id', None) == user_id:

                    if map_pool_time:
                        user_data = await update_user_element_map_pool_time(
                            request, user_id=user.get('user_id'), map_pool_time=map_pool_time)

                        if user_data:
                            await update_user_in_redis(request, user_id)
                            access_token = await generate_new_access_token(request, user_id)

                            if user:
                                ret_val['data'] = access_token
                                ret_val['success'] = True
                                status = 202
                                ret_val['message'] = 'server.accepted'

                    else:
                        status = 412
                        ret_val['message'] = 'server.query_condition_failed'
                else:
                    status = 403
                    ret_val['message'] = 'server.forbidden'
            else:
                status = 401
                ret_val['message'] = 'server.unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user_update_map_pool_time_put -> PUT erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')
