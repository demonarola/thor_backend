#!/usr/bin/env python3db_user = await get_user_login_by_email(request, username)
# -*- coding: utf-8 -*-


__version__ = '1.0.1'

from psycopg2 import pool
from copy import deepcopy
from asyncpg import create_pool
from sanic import Sanic
# from sanic.exceptions import RequestTimeout

from sanic_cors import CORS
from sanic_jwt import Initialize
from sanic.log import logger
from sanic_redis_ext import RedisExtension

from web_backend.nvlserver.security import nv_payload_extender, nv_scope_extender
from web_backend.nvlserver.helper.request_logging_helper import request_timeout

# WEB API BLUEPRINTS USED FOR COMMUNICATION BETWEEN FRONTEND AND BACKEND


from web_backend.nvlserver.module.user.controller import api_user_management_blueprint
from web_backend.nvlserver.module.town.controller import api_town_blueprint
from web_backend.nvlserver.module.country.controller import api_country_blueprint
from web_backend.nvlserver.module.language.controller import api_language_blueprint

from web_backend.nvlserver.module.notification_type.controller import api_notification_type_blueprint
from web_backend.nvlserver.module.notification.controller import api_notification_blueprint
from web_backend.nvlserver.module.hw_module.controller import api_hw_module_blueprint
from web_backend.nvlserver.module.support.controller import api_support_blueprint
from web_backend.nvlserver.module.console.controller import api_console_blueprint
from web_backend.nvlserver.module.traceable_object.controller import api_traceable_object_blueprint
from web_backend.nvlserver.module.subscription.controller import api_subscription_blueprint
from web_backend.nvlserver.module.nvl_cartography.controller import api_nvl_cartography_blueprint
from web_backend.nvlserver.module.hw_action.controller import api_hw_action_blueprint
from web_backend.nvlserver.module.location.controller import api_location_blueprint
from web_backend.nvlserver.module.hw_module_position.controller import api_hw_module_position_blueprint
from web_backend.nvlserver.module.hw_module_user_position.controller import api_hw_module_user_position_blueprint
from web_backend.nvlserver.module.account_type.controller import api_account_type_blueprint
from web_backend.nvlserver.module.timezone.controller import api_timezone_blueprint
from web_backend.nvlserver.module.report.controller import api_nvl_report_blueprint
from web_backend.nvlserver.module.rent.controller import api_rent_blueprint
from web_backend.nvlserver.module.to_remove.controller import api_test_blueprint
from web_backend.nvlserver.module.user_hw_action.controller import api_user_hw_action_blueprint


# TODO: REMOVE IN PRODUCTION OR LIMIT USAGE CURRENTLY FRONT HTML PAGE

from .security import RedisPgAuthentication
from web_backend import config
from sanic.log import LOGGING_CONFIG_DEFAULTS

__all__ = ['nvl_app', 'db_conf']

# INIT SANIC object
nvl_app = Sanic(__name__)
CORS(nvl_app, automatic_options=True)

# LOAD CONFIGURATION IN TO SANIC APP
nvl_app.config.REQUEST_MAX_SIZE = config.REQUEST_MAX_SIZE
nvl_app.config.REQUEST_TIMEOUT = config.REQUEST_TIMEOUT
nvl_app.config.update(config.REDIS)

# ADD BLUEPRINTS TO SANIC

nvl_app.blueprint(api_user_management_blueprint)
nvl_app.blueprint(api_town_blueprint)
nvl_app.blueprint(api_country_blueprint)
nvl_app.blueprint(api_language_blueprint)
nvl_app.blueprint(api_notification_blueprint)
nvl_app.blueprint(api_notification_type_blueprint)
nvl_app.blueprint(api_hw_module_blueprint)
nvl_app.blueprint(api_support_blueprint)
nvl_app.blueprint(api_console_blueprint)
nvl_app.blueprint(api_traceable_object_blueprint)
nvl_app.blueprint(api_subscription_blueprint)
nvl_app.blueprint(api_nvl_cartography_blueprint)
nvl_app.blueprint(api_location_blueprint)
nvl_app.blueprint(api_hw_action_blueprint)
nvl_app.blueprint(api_user_hw_action_blueprint)
nvl_app.blueprint(api_hw_module_position_blueprint)
nvl_app.blueprint(api_hw_module_user_position_blueprint)
nvl_app.blueprint(api_account_type_blueprint)
nvl_app.blueprint(api_timezone_blueprint)
nvl_app.blueprint(api_nvl_report_blueprint)
nvl_app.blueprint(api_rent_blueprint)
nvl_app.blueprint(api_test_blueprint)

RedisExtension(nvl_app)


db_conf = deepcopy(config.DATABASE)

pg_pool = pool.ThreadedConnectionPool(
    5, 20,
    user=db_conf['user'],
    password=db_conf['password'],
    host=db_conf['host'],
    port=db_conf['port'],
    database=db_conf['database'])

# SETUP JWT TOKEN
Initialize(nvl_app,
           algorithm='HS512',
           authentication_class=RedisPgAuthentication,
           refresh_token_enabled=True,
           url_prefix='/api/auth',
           expiration_delta=604800,
           access_token_name='access_token',
           verify_exp=True,
           secret=config.SALT,
           extend_payload=nv_payload_extender,
           add_scopes_to_payload=nv_scope_extender
           )


@nvl_app.listener('before_server_start')
async def before_server_start_test(app, loop):
    """ Init Postgresql DB.

    :param app:
    :param loop:
    :return:
    """

    try:
        conn_uri = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
            'postgres',
            db_conf['user'], db_conf['password'], db_conf['host'],
            db_conf['port'], db_conf['database'])
        app.pg_pool = await create_pool(
            conn_uri, min_size=2, max_size=10,
            server_settings={'application_name': 'thorium_backend'})
        app.pg = app.pg_pool
        app.support_store_dir = config.SUPPORT_DATA_DIRECTORY
    except Exception as ipg_error:
        logger.error('BEFORE SERVER START ERRED WITH :{}'.format(ipg_error))
        app.pg = None


@nvl_app.listener("after_server_start")
async def after_server_start_test(*args, **kwargs):
    # print("after_server_start")
    pass


@nvl_app.listener('before_server_stop')
async def before_server_stop_test(app, loop):
    """ Init Postgresql DB.

    :param app:
    :param loop:
    :return:
    """

    try:
        await app.pg.close()
    except Exception as ipg_error:
        logger.error('BEFORE SERVER STOP ERRED WITH :{}'.format(ipg_error))
        app.pg = None
        app.redis = None


@nvl_app.listener("after_server_stop")
async def after_server_stop_test(*args, **kwargs):
    # print("after_server_stop")
    pass

# SETUP RELOAD AND LOGGER IN DEV ENV
if config.DEBUG:
    LOG_CONFIG = LOGGING_CONFIG_DEFAULTS

    @nvl_app.middleware('response')
    async def request_log(request, response):
        logger.info(f'{request.method} - {request.url} - {response.status}')
