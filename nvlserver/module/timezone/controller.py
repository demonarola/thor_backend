#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

import ujson

from sanic import Blueprint
from sanic.response import raw
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, protected

from .service import get_timezone_list, get_timezone_list_count, get_timezone_dropdown_list
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int

api_timezone_blueprint = Blueprint('api_timezone', url_prefix='/api/timezone')


@api_timezone_blueprint.route('/', methods=['GET'])
@inject_user()
@protected()
async def api_timezone(request: Request, user):
    """ Get TimeZone list.

    :param request:
    :param user:
    :return:
    """
    status, ret_val = 500, {'success': False, 'data': None, 'msg': '', 'count': 0}
    limit = proc_arg_to_int(request.args.get('limit', '0'), 0)
    page = proc_arg_to_int(request.args.get('offset', '0'), 0)
    code = request.args.get('code', None)
    offset = page * limit

    if request.method == 'GET':
        """ Get TimeZone list with filter."""
        try:
            if user:
                logged_in_user_id = user.get('user_id', None)
                if logged_in_user_id:
                    all_records = await get_timezone_list(
                        request, code=code, limit=limit, offset=offset)
                    rec_count = await get_timezone_list_count(request, code=code)
                    ret_val['data'] = all_records
                    ret_val['count'] = rec_count
                    ret_val['success'] = True
                    status = 200
                else:
                    status = 403
                    ret_val['msg'] = '403 Forbidden'
            else:
                status = 401
                ret_val['msg'] = '401 Unauthorized'
        except Exception as al_err:
            logger.error('Function api_timezone erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')


@api_timezone_blueprint.route('/dropdown', methods=['GET'])
@inject_user()
@protected()
async def api_timezone_dropdown(request: Request, user):
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

                    timezone_list = await get_timezone_dropdown_list(
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
            logger.error('Function api_timezone_dropdown -> GET erred with: {}'.format(al_err))

    return raw(ujson.dumps(ret_val).encode(), status=status, content_type='application\\json')
