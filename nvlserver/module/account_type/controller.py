#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic.response import raw
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, protected, scoped


from .service import (
    get_account_type_dropdown_list
)


api_account_type_blueprint = Blueprint('api_account_type', url_prefix='/api/account_type')


@api_account_type_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
@protected()
async def api_account_type_dropdown(
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

                    account_type_list = await get_account_type_dropdown_list(
                        request, name=name)

                    if account_type_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = account_type_list
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
            logger.error('Function api_account_type_dropdown -> GET erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')
