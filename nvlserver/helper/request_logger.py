#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__version__ = '1.0.1'
from functools import wraps
from sanic.request import Request

from web_backend.nvlserver.module.request_logger.service import create_request_log_element


def request_logger(func):
    """ Login required decorator used in api views.

    :param func:
    :return:
    """
    @wraps(func)
    async def decorated_view(*args, **kwargs):
        resp = await func(*args, **kwargs)
        # LOG API ACCESS TO DATABASE
        if isinstance(args[0], Request):
            if isinstance(args[0].body, bytes):
                rdata = args[0].body.decode('utf-8')
            else:
                rdata = args[0].body

            if isinstance(args[0].body, bytes):
                resp_data = resp.body.decode('utf-8')
            else:
                resp_data = resp.body
            await create_request_log_element(args[0], args[0].url, rdata, resp_data)

        return resp
    return decorated_view
