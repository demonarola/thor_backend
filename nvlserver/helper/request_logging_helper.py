#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sanic import response
from sanic.log import logger


def request_timeout(
        request,
        pg_pool,
        exception):
    """ On request timeout store in database broken connection

    :param request:
    :param pg_pool:
    :param exception:
    :return:
    """
    """ On """
    # global pg_pool
    try:
        if pg_pool and exception:
            ps_connection = pg_pool.getconn()
            if ps_connection:
                exct = '{}'.format(exception.args[0])
                ip_data = exct.lstrip('Request Timeout,')
                ip_data = ip_data.split(',')
                ps_cursor = ps_connection.cursor()
                ps_cursor.execute(
                    """INSERT INTO public.request_timeout_log_view
                     (ip_addr, active, deleted) VALUES ('%s', %s, %s)""" % (
                        ':'.join(ip_data), True, False))
                ps_connection.commit()
                ps_cursor.close()
                # Use this method to release the connection object and send back to connection pool
                pg_pool.putconn(ps_connection)
    except Exception as terr:
        logger.error('timeout erred with : {}'.format(terr))
    finally:
        if ps_cursor:
            ps_cursor.close()
        if ps_connection:
            pg_pool.putconn(ps_connection)

    return response.json({"status": "RequestTimeout"}, status=408)
