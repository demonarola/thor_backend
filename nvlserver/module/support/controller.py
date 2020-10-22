#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'
import os
import ujson
import uuid
import aiofiles

from sanic import Blueprint
from sanic import response
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, scoped, protected


from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int
from .service import (
    get_support_list, get_support_list_count, create_support_element,
    get_support_element, update_support_element, delete_support_element
)

api_support_blueprint = Blueprint('api_support', url_prefix='/api/support')


@api_support_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_support_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    email = request.args.get('email', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:

            if user:

                if user.get('user_id', None):
                    support_list = await get_support_list(request, email=email, limit=size, offset=offset)
                    support_count = await get_support_list_count(request, email=email)

                    if support_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            support_list, support_count, size=size, page=page)
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
        except Exception as al_err:
            logger.error('Function api_support_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_support_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_support_post(request: Request, user):
    """

    :param request:
    --  :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    support_data_dir = request.app.support_store_dir

    if request.method == 'POST':
        try:
            # if user:
            if True:
                # if user.get('user_id'):
                if True:
                    # if user.get('user_id') and user.get('is_superuser'):
                    if True:
                        email = request.json.get('email', None)
                        user_id = request.json.get('user_id', None)
                        subject = request.json.get('subject', None)
                        message = request.json.get('message', False)
                        active = request.json.get('active', False)
                        file = request.files.get('file')

                        if file:
                            file_data = file.body
                            supp_file_name = request.json.get('file_name', '')
                            file_uuid = str(uuid.uuid4())
                        else:
                            supp_file_name = ''
                            file_data = None
                            file_uuid = None

                        if True:
                            if file_data:
                                async with aiofiles.open(
                                        os.path.join(support_data_dir, file_uuid), mode='wb+') as f:
                                    await f.write(file_data)

                            support = await create_support_element(
                                request, email=email, user_id=user_id, subject=subject,
                                file_uuid=file_uuid, file_name=supp_file_name, message=message, active=active)

                            if support:
                                ret_val['data'] = support
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
            logger.error('Function api_support_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_support_blueprint.route('/<support_id:int>', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_support_element_get(request: Request, user, support_id: int = 0):
    """

    :param request:
    :param user:
    :param support_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            # if user:
            if True:

                # if user.get('user_id', None) and support_id:
                if True:

                    support_element = await get_support_element(request, support_id)

                    if support_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = support_element
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
            logger.error('Function api_support_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_support_blueprint.route('/<support_id:int>', methods=['PUT'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_support_element_put(request: Request, user, support_id: int = 0):
    """

    :param request:
    :param user:
    :param support_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    support_data_dir = request.app.support_store_dir

    if request.method == 'PUT':
        try:
            # if user:
            if True:

                # if user.get('user_id'):
                if True:
                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and support_id:
                        email = request.json.get('email', None)
                        user_id = request.json.get('user_id', None)
                        subject = request.json.get('subject', None)
                        message = request.json.get('message', False)
                        active = request.json.get('active', False)
                        file = request.files.get('file')

                        if file:
                            file_data = file.body
                            supp_file_name = request.json.get('file_name', '')
                            file_uuid = str(uuid.uuid4())
                        else:
                            supp_file_name = ''
                            file_data = None
                            file_uuid = None

                        if True:
                            if file_data:
                                async with aiofiles.open(
                                        os.path.join(support_data_dir, file_uuid), mode='wb+') as f:
                                    await f.write(file_data)

                            support_element = await update_support_element(
                                request, support_id=support_id, email=email, user_id=user_id, subject=subject,
                                file_uuid=file_uuid, file_name=supp_file_name, message=message, active=active)

                            ret_val['success'] = True
                            ret_val['message'] = 'server.query_success'
                            ret_val['data'] = support_element
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
            logger.error('Function api_support_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_support_blueprint.route('/<support_id:int>', methods=['DELETE'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_support_element_delete(request: Request, user, support_id: int = 0):
    """

    :param request:
    :param user:
    :param support_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            # if user:
            if True:

                # if user.get('user_id'):
                if True:
                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and support_id:
                        support = await delete_support_element(request, support_id)

                        if support:
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
            logger.error('Function api_support_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
