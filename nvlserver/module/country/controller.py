#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic import response
from sanic.request import Request
from sanic_jwt import inject_user, scoped

from .service import get_country_list

api_country_blueprint = Blueprint('api_country', url_prefix='/api/country')


@api_country_blueprint.route('/', methods=['GET'])
@inject_user()
# @scoped(['user', 'billing', 'admin'], require_all=True, require_all_actions=True)
async def api_country_get(
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
            
            if user.get('user_id'):
                country_list = await get_country_list(request)

                if country_list:
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = country_list
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


@api_country_blueprint.route('/', methods=['POST'])
@inject_user()
# @scoped(['admin'], require_all=True, require_all_actions=True)
async def api_country_post(
        request: Request,
        user):
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
                pass
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
