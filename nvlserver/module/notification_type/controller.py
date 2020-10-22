#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
from sanic import Blueprint
from sanic.response import raw
from sanic.request import Request
from sanic_jwt import inject_user, protected

from .service import get_notification_type_list

api_notification_type_blueprint = Blueprint('api_notification_type', url_prefix='/api/notification_type')


@api_notification_type_blueprint.route('/', methods=['GET'])
@inject_user()
@protected()
async def api_notification_type(
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

            if user.get('user_id') and user.get('is_superuser'):

                notification_type_list = await get_notification_type_list(request)

                if notification_type_list:
                    not_type_data = {}
                    [not_type_data.update({x.get('id'): x}) for x in notification_type_list]
                    ret_val['success'] = True
                    ret_val['message'] = 'server.query_success'
                    ret_val['data'] = not_type_data
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

    return raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
