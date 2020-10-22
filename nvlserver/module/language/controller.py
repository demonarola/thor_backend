#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic.response import raw
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, protected, scoped


from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

from web_backend.nvlserver.security.helper import update_user_in_redis
from web_backend.nvlserver.module.user.service import update_user_element_language
from .service import (
    get_language_element,
    get_language_list,
    get_language_list_count,
    create_language_element,
    check_if_language_name_is_free,
    update_language_element,
    delete_language_element,
    get_language_element_by_short_code,
    get_language_dropdown_list
)


api_language_blueprint = Blueprint('api_language', url_prefix='/api/language')


@api_language_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_language(
        request: Request,
        user):
    """ Get Language list

    :param request:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    name = request.args.get('name', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        """ Get Language list."""
        try:

            all_languages_list = await get_language_list(request, name=name, limit=size, offset=offset)
            all_languages_list_count = get_language_list_count(request, name=name)
            if all_languages_list:
                ret_val['success'] = True
                ret_val['message'] = 'server.query_success'
                res_data_formatted = await populate_response_format(
                    all_languages_list, all_languages_list_count, size=size, page=page)
                ret_val['data'] = res_data_formatted
                status = 200
            else:
                ret_val['success'] = True
                ret_val['message'] = 'server.query_success'
                ret_val['data'] = {}
                status = 200

        except Exception as al_err:
            logger.error('Function api_language -> GET erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_language_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_language_create(
        request: Request,
        user):
    """ Create language element

    :param request:
    :param user:
    :return:
    """
    status, ret_val = 500, {'success': False, 'data': None, 'message': '', 'count': 0}
    if request.method == 'POST':
        """ Create Language element."""
        try:
            if user:

                if user.get('user_id', None) and user.get('account_type_name') == 'admin':
                    name = request.json.get('name', None)
                    short_code = request.json.get('short_code', None)
                    default_language = request.json.get('default_language', False)
                    active = request.json.get('active', True)

                    lang_free = await check_if_language_name_is_free(name=name)

                    if lang_free:
                        new_language = await create_language_element(
                            request, name=name, short_code=short_code,
                            default_language=default_language, active=active)
                        if new_language:
                            ret_val['data'] = new_language
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = '201 Created'
                        else:
                            status = 200
                            ret_val['message'] = 'Can not create language.'
                    else:
                        status = 200
                        ret_val['message'] = 'Can not recreate existing language.'

                else:
                    status = 403
                    ret_val['message'] = '403 Forbidden'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as al_err:
            logger.error('Function api_language -> POST erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_language_blueprint.route('/change', methods=['POST'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_language_change(
        request: Request,
        user):
    """ Create language element

    :param request:
    :param user:
    :return:
    """
    status, ret_val = 500, {'success': False, 'data': None, 'message': '', 'count': 0}
    if request.method == 'POST':
        """ Create Language element."""
        try:
            if user:

                if user.get('user_id', None) and user.get('account_type_name') == 'admin':
                    language_short_code = request.json.get('code')
                    language = await get_language_element_by_short_code(request, language_short_code)
                    if language:
                        usr_change = await update_user_element_language(
                            request, user.get('user_id'), language.get('id'))
                        await update_user_in_redis(request, user.get('user_id'))
                        if usr_change:
                            # print(dir(request.get('app')))
                            # r = RedisPgAuthentication()
                            # dta = r.generate_access_token(usr_change)
                            status = 202
                            # ret_val['message'] = dta
                            ret_val['success'] = True
                else:
                    status = 403
                    ret_val['message'] = '403 Forbidden'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as al_err:
            logger.error('Function api_language -> POST erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_language_blueprint.route('/<language_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_language_element_get(
        request: Request,
        user,
        language_id: int = 0):
    """ Get Language element / Edit Language element / Delete Language element

    :param request:
    :param user:
    :param language_id:
    :return:
    """
    status, ret_val = 500, {'success': False, 'data': None}

    if request.method == 'GET':
        """ Get Language element."""
        try:
            if user:

                if user.get('user_id', None) and language_id:
                    language = await get_language_element(request, language_id)
                    ret_val['data'] = language
                    ret_val['success'] = True
                    status = 200

                else:
                    status = 400
                    ret_val['message'] = '400 Bad Request'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as ale_err:
            logger.error('Function api_language_element -> GET erred with: {}'.format(ale_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_language_blueprint.route('/<language_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_language_element_put(
        request: Request,
        user,
        language_id: int = 0):
    """ Get Language element / Edit Language element / Delete Language element

    :param request:
    :param user:
    :param language_id:
    :return:
    """
    status, ret_val = 500, {'success': False, 'data': None}

    if request.method == 'PUT':
        """ Edit Language element."""
        try:
            if user:

                if user.get('user_id', None) and language_id and user.get('account_type_name') == 'admin':
                    name = request.json.get('name', None)
                    short_code = request.json.get('short_code', None)
                    default_language = request.json.get('default_language', False)
                    active = request.json.get('active', True)

                    lang_free = await check_if_language_name_is_free(request, name=name, language_id=language_id)

                    if lang_free:
                        language = await get_language_element(
                            request, language_id=language_id)
                        if language:
                            updated_language = await update_language_element(
                                request, language_id=language_id, name=name, short_code=short_code,
                                default_language=default_language, active=active)
                            if updated_language:
                                ret_val['data'] = updated_language
                                ret_val['success'] = True
                                status = 202
                                ret_val['message'] = '202 Accepted'
                        else:
                            status = 200
                            ret_val['message'] = 'Can not find language.'
                    else:
                        status = 200
                        ret_val['message'] = 'Language with the same name all ready exist.'
                else:
                    status = 403
                    ret_val['message'] = '403 Forbidden'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as rer_err:
            logger.error('Function api_user_element -> PUT erred with: {}'.format(rer_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_language_blueprint.route('/<language_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_language_element_delete(
        request: Request,
        user,
        language_id: int = 0):
    """ Get Language element / Edit Language element / Delete Language element

    :param request:
    :param user:
    :param language_id:
    :return:
    """
    status, ret_val = 500, {'success': False, 'data': None}

    if request.method == 'DELETE':
        """ Delete Language element."""
        try:
            if user:
                if user.get('user_id', None) and language_id and user.get('account_type_name') == 'admin':
                    deleted_language = await delete_language_element(request, language_id=language_id)
                    if deleted_language:
                        ret_val['data'] = deleted_language
                        ret_val['success'] = True
                        status = 202
                        ret_val['message'] = '202 Accepted'
                else:
                    status = 403
                    ret_val['message'] = '403 Forbidden'
            else:
                status = 401
                ret_val['message'] = '401 Unauthorized'
        except Exception as ale_err:
            logger.error('Function api_language_element -> DELETE erred with: {}'.format(ale_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_language_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
@protected()
async def api_language_dropdown(
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

                    timezone_list = await get_language_dropdown_list(
                        request, name=name)

                    if timezone_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = timezone_list
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
            logger.error('Function api_language_dropdown -> GET erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')
