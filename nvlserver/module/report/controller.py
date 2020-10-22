#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson
import iso8601
# from datetime import datetime
# from datetime import timedelta
import traceback
from sanic import Blueprint
from sanic import response
from sanic.log import logger
from sanic.request import Request
from sanic_jwt import inject_user, scoped
from web_backend.nvlserver.helper.process_request_args import proc_arg_to_int
from web_backend.nvlserver.helper.request_wrapper import populate_response_format
from web_backend.nvlserver.module.traceable_object.service import get_traceable_object_element

from .service import get_nvl_position_list, get_nvl_position_list_count, get_nvl_distance

api_nvl_report_blueprint = Blueprint('nvl_report', url_prefix='/api/nvl_report')


# NVL POINT CONTROLLER
@api_nvl_report_blueprint.route('/', methods=['GET'])
@inject_user()
@scoped(['report:read'], require_all=True, require_all_actions=True)
async def api_nvl_report_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    size = proc_arg_to_int(request.args.get('size', '1'), 1)
    page = proc_arg_to_int(request.args.get('page', '1'), 1)
    date_from_front = request.args.get('date_from', None)
    date_to_front = request.args.get('date_to', None)
    # print(date_from_front)
    # print(date_to_front)
    # TODO: REMOVE REPLACE ON CHANGE PARAM FROM FRONTEND
    if date_from_front is not None:
        date_from = iso8601.parse_date(date_from_front.replace(' ', '+'))
    else:
        date_from = None
    if date_to_front is not None:
        date_to = iso8601.parse_date(date_to_front.replace(' ', '+'))
    else:
        date_to = None
    # print(date_from)
    # print(date_to)
    traceable_object_id = proc_arg_to_int(request.args.get('traceable_object_id', '0'), 0)
    user_id = proc_arg_to_int(request.args.get('user_id', '0'), 0)
    offset = (page - 1) * size

    if request.method == 'GET':
        # print(2222222222222222222)
        try:
            if user:

                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    position_list = await get_nvl_position_list(
                        request, user_id=user_id, traceable_object_id=traceable_object_id,
                        date_from=date_from, date_to=date_to, limit=size, offset=offset
                    )

                    position_list_count = await get_nvl_position_list_count(
                        request, user_id=user_id, traceable_object_id=traceable_object_id,
                        date_from=date_from, date_to=date_to
                    )

                    if position_list:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        res_data_formatted = await populate_response_format(
                            position_list, position_list_count, size=size, page=page)
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
            logger.error('Function api_nvl_report_get -> GET erred with: {}'.format(al_err))
            traceback.print_exc()

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_nvl_report_blueprint.route('/trip_info', methods=['GET'])
@inject_user()
@scoped(['report:read'], require_all=True, require_all_actions=True)
async def api_nvl_report_trip_info_get(request: Request, user):
    """

    :param request:
    :param user:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}

    date_from_front = request.args.get('date_from', None)
    date_to_front = request.args.get('date_to', None)
    # print(date_from_front)
    # print(date_to_front)
    # TODO: REMOVE REPLACE ON CHANGE PARAM FROM FRONTEND
    if date_from_front is not None:
        date_from = iso8601.parse_date(date_from_front.replace(' ', '+'))
    else:
        date_from = None
    if date_to_front is not None:
        date_to = iso8601.parse_date(date_to_front.replace(' ', '+'))
    else:
        date_to = None
    traceable_object_id = proc_arg_to_int(request.args.get('traceable_object_id', '0'), 0)
    user_id = proc_arg_to_int(request.args.get('user_id', '0'), 0)

    if request.method == 'GET':
        try:
            if user:

                if user.get('user_id', None):
                    if user.get('account_type_name') == 'admin':
                        user_id = user_id
                    else:
                        user_id = user.get('user_id')

                    if None in [date_to, date_from]:
                        distance = 0.0
                    else:
                        distance = await get_nvl_distance(
                            request, user_id=user_id, traceable_object_id=traceable_object_id,
                            date_from=date_from, date_to=date_to
                        )

                    traceable_object = await get_traceable_object_element(
                        request, user_id=user_id, traceable_object_id=traceable_object_id)

                    if None in [date_from, date_to] or distance == 0.0:
                        consumption_per_trip = 0.0
                    else:
                        # print(traceable_object.get('consumption', '0'), distance)
                        consumption_per_trip = float(traceable_object.get('consumption', '0')) * (distance / 100000)

                    if traceable_object:
                        ret_val['success'] = True
                        ret_val['message'] = 'server.query_success'
                        ret_val['data'] = {
                            'vehicle_model': traceable_object.get('vehicle_model', ''),
                            'vehicle_brand': traceable_object.get('vehicle_brand', ''),
                            'consumption': '{} l/100km'.format(traceable_object.get('consumption', '')),
                            'distance': '{0:.2f} km'.format((distance / 1000.)),
                            'consumption_per_trip': '{0:.2f} l'.format(consumption_per_trip)

                        }
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
            logger.error('Function api_nvl_report_trip_info_get -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
