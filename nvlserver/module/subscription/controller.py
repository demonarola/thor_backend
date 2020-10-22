#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson
import uuid
import datetime
import iso8601
from sanic import Blueprint
from sanic import response
from decimal import Decimal
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, scoped

from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int
from .service import (
    # SUBSCRIPTION SERVICES
    get_subscription_list, get_subscription_list_count, create_subscription_element,
    get_subscription_element, update_subscription_element, delete_subscription_element,
    # SUBSCRIPTION MODEL SERVICES
    get_subscription_model_list, get_subscription_model_list_count, create_subscription_model_element,
    get_subscription_model_element, update_subscription_model_element, delete_subscription_model_element,
    get_subscription_model_dropdown_list,
    # REBATE SERVICES
    get_rebate_list, get_rebate_list_count, create_rebate_element,
    get_rebate_element, update_rebate_element, delete_rebate_element, get_rebate_dropdown_list,
)

api_subscription_blueprint = Blueprint('api_subscription', url_prefix='/api/subscription')


# SUBSCRIPTION CONTROLLER
@api_subscription_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['subscription:read'], require_all=True, require_all_actions=True)
async def api_subscription_get(request: Request, user):
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
    rebate_id = request.args.get('rebate_id', None)
    subscription_model_id = request.args.get('subscription_model_id', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None):
                    if user.get('account_type_name') in ['admin', 'billing']:
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')
                    subscription_list = await get_subscription_list(
                        request, subscription_model_id=subscription_model_id,
                        user_id=user_id, rebate_id=rebate_id, limit=size, offset=offset)
                    subscription_list_count = await get_subscription_list_count(
                        request, subscription_model_id=subscription_model_id, user_id=user_id, rebate_id=rebate_id)

                    if subscription_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            subscription_list, subscription_list_count, size=size, page=page)
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


@api_subscription_blueprint.route('/', methods=['POST'])
@inject_user()
@scoped(['subscription:create'], require_all=True, require_all_actions=True)
async def api_subscription_post(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'POST':
        try:
            if user:
                if user.get('user_id'):
                    if user.get('account_type_name') in ['admin', 'billing']:

                        subscription_uuid = request.json.get('subscription_uuid', str(uuid.uuid4()))
                        user_id = request.json.get('user_id', None)
                        subscription_model_id = request.json.get('subscription_model_id', None)
                        rebate_id = request.json.get('rebate_id', None)
                        meta_information = request.json.get('meta_information', {})
                        unit_count = request.json.get('unit_count', None)
                        date_from_front = request.json.get('date_from', None)
                        date_to_front = request.json.get('date_to', None)
                        active = request.json.get('active', True)

                        if True and date_from_front and date_to_front:
                            date_from = iso8601.parse_date(date_from_front)
                            date_to = iso8601.parse_date(date_to_front)
                            subscription_element = await create_subscription_element(
                                request, subscription_uuid=subscription_uuid, user_id=user_id,
                                subscription_model_id=subscription_model_id, rebate_id=rebate_id,
                                meta_information=meta_information, unit_count=unit_count,
                                date_from=date_from, date_to=date_to, active=active)

                            if subscription_element:
                                ret_val['data'] = subscription_element
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


@api_subscription_blueprint.route('/<subscription_id:int>', methods=['GET'])
@inject_user()
@scoped(['subscription:read'], require_all=True, require_all_actions=True)
async def api_subscription_element_get(request: Request, user, subscription_id: int = 0):
    """

    :param request:
    :param user:
    :param subscription_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:
                if user.get('account_type_name', None) is not None and subscription_id:

                    subscription_element = await get_subscription_element(request, subscription_id)

                    if subscription_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = subscription_element
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
            logger.error('Function api_subscription_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/<subscription_id:int>', methods=['PUT'])
@inject_user()
@scoped(['subscription:update'], require_all=True, require_all_actions=True)
async def api_subscription_element_put(request: Request, user, subscription_id: int = 0):
    """

    :param request:
    :param user:
    :param subscription_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id', None) is not None:

                    # subscription_uuid = request.json.get('subscription_uuid', str(uuid.uuid4()))
                    if user.get('account_type_name', None) in ['admin', 'billing']:
                        user_id = request.json.get('user_id', None)
                    else:
                        user_id = user.get('user_id')
                    subscription_model_id = request.json.get('subscription_model_id', None)
                    rebate_id = request.json.get('rebate_id', None)
                    meta_information = request.json.get('meta_information', {})
                    unit_count = request.json.get('unit_count', None)
                    active = request.json.get('active', True)
                    date_from_front = request.json.get('date_from', None)
                    date_to_front = request.json.get('date_to', None)

                    if subscription_id and date_from_front and date_to_front:
                        date_from = iso8601.parse_date(date_from_front)
                        date_to = iso8601.parse_date(date_to_front)
                        subscription_element = await update_subscription_element(
                            request, subscription_id=subscription_id,
                            user_id=user_id,
                            subscription_model_id=subscription_model_id, rebate_id=rebate_id,
                            meta_information=ujson.dumps(meta_information), unit_count=unit_count,
                            date_from=date_from, date_to=date_to, active=active)

                        if subscription_element:
                            ret_val['data'] = subscription_element
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = 'server.object_created'
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
            logger.error('Function api_subscription_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/<subscription_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['subscription:delete'], require_all=True, require_all_actions=True)
async def api_subscription_element_delete(request: Request, user, subscription_id: int = 0):
    """

    :param request:
    :param user:
    :param subscription_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('account_type_name', None) in ['admin', 'billing']:
                    # TODO: IMPLEMENT USER ACCESS if user.get('is_superuser'):
                    if True and subscription_id:
                        await delete_subscription_element(request, subscription_id)

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
            logger.error('Function api_subscription_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# SUBSCRIPTION MODEL CONTROLLER
@api_subscription_blueprint.route('/model', methods=['GET'])
@inject_user()
@scoped(['subscription:read'], require_all=True, require_all_actions=True)
async def api_subscription_model_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    description = request.args.get('description', None)
    duration_month = request.args.get('duration_month', None)
    price_per_unit = request.args.get('price_per_unit', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None) and user.get('account_type_name') in ['admin', 'billing']:

                    subscription_model_list = await get_subscription_model_list(
                        request, description=description,
                        duration_month=duration_month, price_per_unit=price_per_unit, limit=size, offset=offset)
                    subscription_model_list_count = await get_subscription_model_list_count(
                        request, description=description, duration_month=duration_month, price_per_unit=price_per_unit)

                    if subscription_model_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            subscription_model_list, subscription_model_list_count, size=size, page=page)
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
            logger.error('Function api_subscription_model_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/model/dropdown', methods=['GET'])
@inject_user()
@scoped(['subscription:query_dropdown'], require_all=True, require_all_actions=True)
async def api_subscription_model_dropdown_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': []}
    description = request.args.get('description', None)

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):

                    subscription_model_dropdown_list = await get_subscription_model_dropdown_list(
                        request, description=description)

                    if subscription_model_dropdown_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = subscription_model_dropdown_list
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
            logger.error('Function api_subscription_model_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/model', methods=['POST'])
@inject_user()
@scoped(['subscription:create'], require_all=True, require_all_actions=True)
async def api_subscription_model_post(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('account_type_name') in ['admin', 'billing']:

                        description = request.json.get('description', '')
                        duration_month = request.json.get('duration_month', 0)
                        price_per_unit = request.json.get('price_per_unit', Decimal(0))
                        meta_information = request.json.get('meta_information', {})
                        active = request.json.get('active', True)

                        if None not in [description, duration_month, price_per_unit]:
                            subscription_model_element = await create_subscription_model_element(
                                request, description=description, duration_month=duration_month,
                                price_per_unit=price_per_unit,
                                meta_information=meta_information, active=active)

                            if subscription_model_element:
                                ret_val['data'] = subscription_model_element
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
            logger.error('Function api_subscription_model_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/model/<subscription_model_id:int>', methods=['GET'])
@inject_user()
@scoped(['subscription:read'], require_all=True, require_all_actions=True)
async def api_subscription_model_element_get(request: Request, user, subscription_model_id: int = 0):
    """

    :param request:
    :param user:
    :param subscription_model_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:

                if subscription_model_id:

                    subscription_model_element = await get_subscription_model_element(request, subscription_model_id)

                    if subscription_model_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = subscription_model_element
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
            logger.error('Function api_subscription_model_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/model/<subscription_model_id:int>', methods=['PUT'])
@inject_user()
@scoped(['subscription:update'], require_all=True, require_all_actions=True)
async def api_subscription_model_element_put(request: Request, user, subscription_model_id: int = 0):
    """

    :param request:
    :param user:
    :param subscription_model_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('account_type_name', None) in ['admin', 'billing']:
                        description = request.json.get('description', '')
                        duration_month = request.json.get('duration_month', 0)
                        price_per_unit = request.json.get('price_per_unit', Decimal(0))
                        meta_information = request.json.get('meta_information', {})
                        active = request.json.get('active', True)

                        if True and subscription_model_id:
                            subscription_model_element = await update_subscription_model_element(
                                request, subscription_model_id=subscription_model_id,
                                description=description, duration_month=duration_month,
                                price_per_unit=price_per_unit,
                                meta_information=meta_information, active=active)

                            if subscription_model_element:
                                ret_val['data'] = subscription_model_element
                                ret_val['success'] = True
                                status = 201
                                ret_val['message'] = 'server.object_created'
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
            logger.error('Function api_subscription_model_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/model/<subscription_model_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['subscription:delete'], require_all=True, require_all_actions=True)
async def api_subscription_model_element_delete(request: Request, user, subscription_model_id: int = 0):
    """

    :param request:
    :param user:
    :param subscription_model_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('account_type_name', None) in ['admin', 'billing'] and subscription_model_id:
                        await delete_subscription_model_element(request, subscription_model_id)

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
            logger.error('Function api_subscription_model_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


# REBATE CONTROLLER
@api_subscription_blueprint.route('/rebate', methods=['GET'])
@inject_user()
@scoped(['rebate:read'], require_all=True, require_all_actions=True)
async def api_rebate_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    value = request.args.get('value', None)
    rebate_is_fixed = request.args.get('rebate_is_fixed', None)
    offset = (page - 1) * size

    if request.method == 'GET':
        try:
            if user:

                # if user.get('user_id', None):
                if True:
                    rebate_list = await get_rebate_list(
                        request, value=value,
                        rebate_is_fixed=rebate_is_fixed, limit=size, offset=offset)
                    rebate_list_count = await get_rebate_list_count(
                        request, value=value,
                        rebate_is_fixed=rebate_is_fixed)

                    if rebate_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            rebate_list, rebate_list_count, size=size, page=page)
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
            logger.error('Function api_rebate_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/rebate/fixed/dropdown', methods=['GET'])
@inject_user()
@scoped(['rebate:query_dropdown'], require_all=True, require_all_actions=True)
async def api_rebate_dropdown_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': []}
    value = request.args.get('value', None)

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):

                    rebate_dropdown_list = await get_rebate_dropdown_list(request, value, True)

                    if rebate_dropdown_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = rebate_dropdown_list
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
            logger.error('Function api_rebate_dropdown_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/rebate/percentage/dropdown', methods=['GET'])
@inject_user()
@scoped(['rebate:query_dropdown'], require_all=True, require_all_actions=True)
async def api_rebate_dropdown_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': []}
    value = request.args.get('value', None)

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):

                    rebate_dropdown_list = await get_rebate_dropdown_list(request, value, False)

                    if rebate_dropdown_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = rebate_dropdown_list
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
            logger.error('Function api_rebate_dropdown_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/rebate', methods=['POST'])
@inject_user()
@scoped(['rebate:create'], require_all=True, require_all_actions=True)
async def api_rebate_post(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'POST':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('user_id') and user.get('account_type_name') in ['admin', 'billing']:

                        value = request.json.get('value', 0)
                        rebate_is_fixed = request.json.get('rebate_is_fixed', False)
                        active = request.json.get('active', True)

                        if rebate_is_fixed:
                            meta_information = {'description': 'Fixed rebate of {}'.format(value)}
                        else:
                            meta_information = {'description': 'Percentage rebate of {} %'.format(value)}

                        rebate_element = await create_rebate_element(
                            request, value=value,
                            rebate_is_fixed=rebate_is_fixed, meta_information=meta_information, active=active)

                        if rebate_element:
                            ret_val['data'] = rebate_element
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
            logger.error('Function api_rebate_post -> POST erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/rebate/<rebate_id:int>', methods=['GET'])
@inject_user()
@scoped(['rebate:read'], require_all=True, require_all_actions=True)
async def api_rebate_element_get(request: Request, user, rebate_id: int = 0):
    """

    :param request:
    :param user:
    :param rebate_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'GET':
        try:
            if user:
                if user.get('user_id', None) and rebate_id:

                    rebate_element = await get_rebate_element(request, rebate_id)

                    if rebate_element:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = rebate_element
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
            logger.error('Function api_rebate_element_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/rebate/<rebate_id:int>', methods=['PUT'])
@inject_user()
@scoped(['rebate:update'], require_all=True, require_all_actions=True)
async def api_rebate_element_put(request: Request, user, rebate_id: int = 0):
    """

    :param request:
    :param user:
    :param rebate_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'PUT':
        try:
            if user:

                if user.get('user_id') and user.get('account_type_name') in ['admin', 'billing']:

                    value = request.json.get('value', 0)
                    rebate_is_fixed = request.json.get('rebate_is_fixed', False)
                    active = request.json.get('active', True)

                    if True and rebate_id:
                        if rebate_is_fixed:
                            meta_information = {'description': 'Fixed rebate of {}'.format(value)}
                        else:
                            meta_information = {'description': 'Percentage rebate of {} %'.format(value)}

                        rebate_element = await update_rebate_element(
                            request, rebate_id=rebate_id,
                            value=value,
                            rebate_is_fixed=rebate_is_fixed, meta_information=meta_information, active=active)

                        if rebate_element:
                            ret_val['data'] = rebate_element
                            ret_val['success'] = True
                            status = 201
                            ret_val['message'] = 'server.object_created'
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
            logger.error('Function api_rebate_element_put -> PUT erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_subscription_blueprint.route('/rebate/<rebate_id:int>', methods=['DELETE'])
@inject_user()
@scoped(['rebate:delete'], require_all=True, require_all_actions=True)
async def api_rebate_element_delete(request: Request, user, rebate_id: int = 0):
    """

    :param request:
    :param user:
    :param rebate_id:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    if request.method == 'DELETE':
        try:
            if user:

                if user.get('user_id'):

                    if user.get('account_type_name') in ['admin', 'billing'] and rebate_id:
                        await delete_rebate_element(request, rebate_id)

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
            logger.error('Function api_rebate_element_delete -> DELETE erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
