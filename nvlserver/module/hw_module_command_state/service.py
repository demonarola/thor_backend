#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

''' NOT USABLE CODE STATE CALCULATED ON POSTGRESQL SIDE
import ujson
from sanic.log import logger
from sanic.request import Request

from .specification.get_hw_module_command_state_specification import (
    get_hw_module_command_state_element_query,
    get_hw_module_command_state_element_by_hw_module_id_query,
    get_hw_module_command_state_element_by_traceable_object_id_query
)

from .specification.create_hw_module_command_state_specification import create_hw_module_command_state_element_query
from .specification.update_hw_module_command_state_specification import (
    update_hw_module_command_state_element_query,
    update_hw_module_command_state_disable_engine_start_by_hw_module_id_query,
    update_hw_module_command_state_sound_buzzer_by_hw_module_id_query,
    update_hw_module_command_state_stop_engine_by_hw_module_id_query

)
from .specification.delete_hw_module_command_state_specification import delete_hw_module_command_state_element_query

__all__ = [
    # SERVICES WORKING ON HW MODULE TABLE
    'get_hw_module_command_state_element_by_hw_module_id',
    'get_hw_module_command_state_element_by_traceable_object_id',
    'create_hw_module_command_state_element',
    'update_hw_module_command_state_element',
    'delete_hw_module_command_state_element',
]


async def get_hw_module_command_state_element(
        request: Request,
        hw_module_command_state_id: int = 0) -> dict:
    """ Get hw_module element

    :param request:
    :param hw_module_command_state_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_command_state_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, hw_module_command_state_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def get_hw_module_command_state_element_by_hw_module_id(
        request: Request,
        hw_module_id: int = 0) -> dict:
    """ Get hw_module_command_state element

    :param request:
    :param hw_module_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_command_state_element_by_hw_module_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(query_str, hw_module_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('get_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def get_hw_module_command_state_element_by_traceable_object_id(
        request: Request,
        user_id: object = None,
        traceable_object_id: int = 0) -> dict:
    """ Get hw_module_command_state element by traceable object id

    :param request:
    :param user_id:
    :param traceable_object_id:
    :return:
    """

    ret_val = {}
    query_str = get_hw_module_command_state_element_by_traceable_object_id_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, user_id, traceable_object_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error(
            'get_hw_module_command_state_element_by_traceable_object_id service erred with: {}'.format(cleerr))

    return ret_val


async def create_hw_module_command_state_element(
        request: Request,
        hw_module_id: object = None,
        sound_buzzer_state: bool = False,
        sound_buzzer_lock: bool = False,
        stop_engine_state: bool = False,
        stop_engine_lock: bool = False,
        disable_engine_start_state: bool = False,
        disable_engine_start_lock: bool = False,
        active: bool = True) -> dict:
    """ Create hw_module_command_state element

    :param request:
    :param hw_module_id:
    :param sound_buzzer_state:
    :param sound_buzzer_lock:
    :param stop_engine_state:
    :param stop_engine_lock:
    :param disable_engine_start_state:
    :param disable_engine_start_lock:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = create_hw_module_command_state_element_query
    try:

        async with request.app.pg.acquire() as connection:

            row = await connection.fetchrow(
                query_str, hw_module_id, sound_buzzer_state,
                sound_buzzer_lock, stop_engine_state, stop_engine_lock,
                disable_engine_start_state, disable_engine_start_lock,
                active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('create_hw_module_command_state_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_command_state_element(
        request: Request,
        hw_module_command_state_id: object = None,
        hw_module_id: object = None,
        sound_buzzer_state: bool = False,
        sound_buzzer_lock: bool = False,
        stop_engine_state: bool = False,
        stop_engine_lock: bool = False,
        disable_engine_start_state: bool = False,
        disable_engine_start_lock: bool = False,
        active: bool = True) -> dict:
    """Update hw_module_command_state element

    :param request:
    :param hw_module_command_state_id:
    :param hw_module_id:
    :param sound_buzzer_state:
    :param sound_buzzer_lock:
    :param stop_engine_state:
    :param stop_engine_lock:
    :param disable_engine_start_state:
    :param disable_engine_start_lock:
    :param active:
    :return:
    """

    ret_val = {}
    query_str = update_hw_module_command_state_element_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_command_state_id, hw_module_id, sound_buzzer_state,
                sound_buzzer_lock, stop_engine_state, stop_engine_lock,
                disable_engine_start_state, disable_engine_start_lock,
                active)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('update_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_command_state_disable_engine_start_by_hw_module_id(
        request: Request,
        hw_module_id: int = 0,
        disable_engine_start_state: bool = False,
        disable_engine_start_lock: bool = False) -> dict:
    """ Update hw_module_command_state element, update disable_engine_start

    :param request:
    :param hw_module_id:
    :param disable_engine_start_state:
    :param disable_engine_start_lock:
    :return:
    """

    ret_val = {}
    query_str = update_hw_module_command_state_disable_engine_start_by_hw_module_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_id, disable_engine_start_state,
                disable_engine_start_lock)
            if row is not None:
                dta = dict(row)
                ret_val = await get_hw_module_command_state_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error('update_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_command_state_sound_buzzer_by_hw_module_id(
        request: Request,
        hw_module_id: int = 0,
        sound_buzzer_state: bool = False,
        sound_buzzer_lock: bool = False) -> dict:
    """ Update hw_module_command_state element, update sound buzzer

    :param request:
    :param hw_module_id:
    :param sound_buzzer_state:
    :param sound_buzzer_lock:
    :return:
    """

    ret_val = {}
    query_str = update_hw_module_command_state_sound_buzzer_by_hw_module_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_id, sound_buzzer_state,
                sound_buzzer_lock)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error(
            'update_hw_module_command_state_sound_buzzer_by_hw_module_id service erred with: {}'.format(cleerr))

    return ret_val


async def update_hw_module_command_state_stop_engine_by_hw_module_id(
        request: Request,
        hw_module_id: int = 0,
        stop_engine_state: bool = False,
        stop_engine_lock: bool = False) -> dict:
    """ Update hw_module_command_state element, update stop engine

    :param request:
    :param hw_module_id:
    :param stop_engine_state:
    :param stop_engine_lock:
    :return:
    """

    ret_val = {}
    query_str = update_hw_module_command_state_stop_engine_by_hw_module_id_query
    try:

        async with request.app.pg.acquire() as connection:
            row = await connection.fetchrow(
                query_str, hw_module_id, stop_engine_state,
                stop_engine_lock)
            if row is not None:
                dta = dict(row)
                ret_val = await get_hw_module_command_state_element(request, dta.get('id'))
    except Exception as cleerr:
        logger.error(
            'update_hw_module_command_state_stop_engine_by_hw_module_id service erred with: {}'.format(cleerr))

    return ret_val


async def delete_hw_module_command_state_element(
        request: Request,
        lift_id: int = 0) -> dict:
    """ Delete hw_module element

    :param request:
    :param lift_id:
    :return:
    """

    ret_val = {}
    query_str = delete_hw_module_command_state_element_query
    try:

        async with request.app.pg.acquire() as connection:
            await connection.set_type_codec(
                'json',
                encoder=ujson.dumps,
                decoder=ujson.loads,
                schema='pg_catalog'
            )
            row = await connection.fetchrow(query_str, lift_id)
            if row is not None:
                ret_val = dict(row)
    except Exception as cleerr:
        logger.error('delete_hw_module_element service erred with: {}'.format(cleerr))

    return ret_val
'''