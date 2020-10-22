#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

import sys
# import uvloop
import asyncio
# import concurrent
# import signal as pysig
# import aiotask_context as context
from httptools import HttpParserUpgrade
from time import time

from config import PORT, HOSTNAME
from nvlserver import nvl_app

from sanic.server import Signal
from sanic.exceptions import (
    RequestTimeout
)

from sanic.websocket import WebSocketProtocol


class CustomHttpProtocol(WebSocketProtocol):
    def __init__(
            self,
            *,
            loop,
            app,
            request_handler,
            error_handler,
            signal=Signal(),
            connections=None,
            request_timeout=10,
            response_timeout=10,
            keep_alive_timeout=10,
            request_max_size=100000,
            request_buffer_queue_size=200,
            request_class=None,
            access_log=False,
            keep_alive=False,
            is_request_stream=False,
            router=None,
            state=None,
            debug=False,
            websocket_timeout=10,
            websocket_max_size=None,
            websocket_max_queue=None,
            websocket_read_limit=2 ** 16,
            websocket_write_limit=2 ** 16,
            **kwargs):

        super().__init__(
            loop=loop,
            app=app,
            request_handler=request_handler,
            error_handler=error_handler,
            signal=signal,
            connections=connections,
            request_timeout=request_timeout,
            response_timeout=response_timeout,
            keep_alive_timeout=keep_alive_timeout,
            request_max_size=request_max_size,
            request_buffer_queue_size=request_buffer_queue_size,
            request_class=request_class,
            access_log=access_log,
            keep_alive=keep_alive,
            is_request_stream=is_request_stream,
            router=router,
            state=state,
            debug=debug,
            **kwargs)
        self.websocket = None
        # self.app = None
        self.websocket_timeout = websocket_timeout
        self.websocket_max_size = websocket_max_size
        self.websocket_max_queue = websocket_max_queue
        self.websocket_read_limit = websocket_read_limit
        self.websocket_write_limit = websocket_write_limit
        # print('ASASASS')

    def connection_made(self, transport):
        super(CustomHttpProtocol, self).connection_made(transport=transport)
        print('CON MADE')

    def connection_lost(self, exc):
        print('CON LOST')
        if self.websocket is not None:
            self.websocket.connection_lost(exc)
        super().connection_lost(exc)
        self.connections.discard(self)
        if self._request_handler_task:
            self._request_handler_task.cancel()
        if self._request_stream_task:
            self._request_stream_task.cancel()
        if self._request_timeout_handler:
            self._request_timeout_handler.cancel()
        if self._response_timeout_handler:
            self._response_timeout_handler.cancel()
        if self._keep_alive_timeout_handler:
            self._keep_alive_timeout_handler.cancel()

    def request_timeout_callback(self):
        print('REQUEST TIMEOUT CALLBACK')
        if self.websocket is None:
            time_elapsed = time() - self._last_request_time
            if time_elapsed < self.request_timeout:
                time_left = self.request_timeout - time_elapsed
                self._request_timeout_handler = self.loop.call_later(
                    time_left, self.request_timeout_callback
                )
            else:
                if self._request_stream_task:
                    self._request_stream_task.cancel()
                if self._request_handler_task:
                    self._request_handler_task.cancel()
                self.write_error(
                    RequestTimeout("Request Timeout,{},{}".format(
                        self.transport.get_extra_info("peername")[0],
                        self.transport.get_extra_info("peername")[1]
                    )))

    def response_timeout_callback(self):
        if self.websocket is None:
            super().response_timeout_callback()

    def keep_alive_timeout_callback(self):
        if self.websocket is None:
            super().keep_alive_timeout_callback()

    def data_received(self, data):
        if self.websocket is not None:
            # pass the data to the websocket protocol
            self.websocket.data_received(data)
        else:
            try:
                super().data_received(data)
            except HttpParserUpgrade:
                # this is okay, it just indicates we've got an upgrade request
                pass

    def write_response(self, response):
        if self.websocket is not None:
            # websocket requests do not write a response
            self.transport.close()
        else:
            super().write_response(response)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        HOSTNAME = str(sys.argv[1])
        PORT = int(sys.argv[2])

    # def killme(signal, frame):
    #     print('THIS IS SIGVER: {}, {}'.format(signal, frame))
    #     app_loop.stop()

    serv_coro = nvl_app.create_server(
        host=HOSTNAME,
        # protocol=CustomHttpProtocol,
        port=PORT, debug=False, access_log=False,
        backlog=100, return_asyncio_server=True
    )
    app_loop = asyncio.get_event_loop()
    app_loop.set_debug(True)
    serv_task = asyncio.ensure_future(serv_coro, loop=app_loop)

    server = app_loop.run_until_complete(serv_task)
    server.after_start()
    try:
        app_loop.run_forever()
    except KeyboardInterrupt as e:
        app_loop.stop()
    finally:
        server.before_stop()

        # Wait for server to close
        close_task = server.close()
        app_loop.run_until_complete(close_task)

        # Complete all tasks on the loop
        for connection in server.connections:
            connection.close_if_idle()
        server.after_stop()
