#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import ujson

from sanic import Blueprint
from sanic import response
from sanic.log import logger
from sanic.request import Request

api_test_blueprint = Blueprint('nvl_test', url_prefix='/api/test')


# NVL POINT CONTROLLER
@api_test_blueprint.route('/point_list', methods=['GET'])
async def api_nvl_test_get(request: Request):
    """

    :param request:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': None}
    query_str_active = """
        SELECT id, (meta_information ->> 'gps_active')::boolean as gps_active,
         meta_information ->> 'time' as time, meta_information ->> 'date' as date, record_time FROM
        public.hw_module_user_position ORDER by record_time desc;
    """
    html_top = """<html>
        <head>
        <meta http-equiv="refresh" content="4">
        </head>
        <table style="width:100%;">
        <tr><td>ID</td><td>GPS_ACTIVE</td><td>TIME</td><td>DATE</td><td>TIMESTAMP</td></tr>"""
    html_table_body = ""
    html_bot = "</table></body></html>"
    if request.method == 'GET':
        try:
            async with request.app.pg.acquire() as connection:
                await connection.set_type_codec(
                    'json',
                    encoder=ujson.dumps,
                    decoder=ujson.loads,
                    schema='pg_catalog'
                )
                active_gps_points = await connection.fetch(query_str_active)
                if active_gps_points:
                    for x in active_gps_points:
                        if x.get('gps_active') is True:

                            html_table_body += '''
                                <tr style="background-color: rgba(00, 255, 00, 0.5)">
                                    <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
                                </tr>'''.format(
                                x.get('id'), x.get('gps_active'), x.get('time'), x.get('date'), x.get('record_time'))
                        else:
                            html_table_body += '''
                                <tr style="background-color: rgba(255, 00, 00, 0.5)">
                                    <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
                                </tr>'''.format(
                                x.get('id'), x.get('gps_active'), x.get('time'), x.get('date'), x.get('record_time'))

                ret_val['success'] = True
                status = 202
        except Exception as al_err:
            logger.error('Function api_nvl_test_get -> GET erred with: {}'.format(al_err))

    return response.html(
        body=html_top + html_table_body + html_bot,
        # headers={'X-Served-By': 'sanic', 'Content-Type': 'application/html'},
        status=status
    )


@api_test_blueprint.route('/delete_points', methods=['GET'])
async def api_nvl_test_delete(request: Request):
    """

    :param request:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': {}}
    delete_hwmupv_query = """
        DELETE FROM public.hw_module_user_position_view WHERE TRUE RETURNING 1;
    """
    delete_hwmpv_query = """
        DELETE FROM public.hw_module_position_view WHERE TRUE RETURNING 1;
    """
    truncate_hwmupv_query = """
        TRUNCATE TABLE public.hw_module_user_position RESTART IDENTITY;
    """
    truncate_hwmpv_query = """
        TRUNCATE TABLE public.hw_module_position RESTART IDENTITY;
    """

    if request.method == 'GET':
        try:
            async with request.app.pg.acquire() as connection:
                delete_hwmupv = await connection.fetchval(delete_hwmupv_query)
                delete_hwmpv = await connection.fetchval(delete_hwmpv_query)
                await connection.fetchval(truncate_hwmupv_query)
                await connection.fetchval(truncate_hwmpv_query)
                if delete_hwmupv:
                    ret_val['data'].update({'user_points_deleted': True})
                if delete_hwmpv:
                    ret_val['data'].update({'points_deleted': True})

                ret_val['success'] = True
                status = 202

        except Exception as al_err:
            logger.error('Function api_nvl_test_delete -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )


@api_test_blueprint.route('/test_long_query', methods=['GET'])
async def api_nvl_test_delete(request: Request):
    """

    :param request:
    :return:
    """
    status = 500
    ret_val = {'success': False, 'message': 'server.query_failed', 'data': {}}

    lest_long_query = """
        select pg_sleep(15);
    """

    if request.method == 'GET':
        try:
            async with request.app.pg.acquire() as connection:
                test_dta = await connection.fetchrow(lest_long_query)
                if test_dta:
                    ret_val['data'].update({'user_points_deleted': dict(test_dta)})

                ret_val['success'] = True
                status = 202

        except Exception as al_err:
            logger.error('Function api_nvl_test_delete -> GET erred with: {}'.format(al_err))

    return response.raw(
        ujson.dumps(ret_val).encode(),
        headers={'X-Served-By': 'sanic', 'Content-Type': 'application/json'},
        status=status
    )
