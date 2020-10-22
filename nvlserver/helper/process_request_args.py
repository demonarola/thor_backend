#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
from sanic.log import logger
from datetime import datetime

default_str_dict_mapper = {'0': False, '1': True}


def proc_arg_to_int(
        input_value: object,
        default_value: int = 0) -> int:
    """ Function processes request arg input to integer_value

    :param input_value:
    :param default_value:
    :return:
    """

    ret_val = default_value

    try:
        if input_value is not None:
            ret_val = int(input_value)
        else:
            ret_val = 0
    except Exception as pati_err:
        logger.error('Error in function proc_arg_to_int erred with {}'.format(pati_err))

    return ret_val


def proc_arg_to_datetime(
        input_value: object,
        default_value: object = None) -> object:
    """ Function processes request arg input to datetime

    :param input_value:
    :param default_value:
    :return:
    """

    ret_val = default_value

    try:
        if input_value is not None and isinstance(input_value, str):
            ret_val = datetime.fromtimestamp(int(input_value)/1000)
        else:
            ret_val = None
    except Exception as pati_err:
        logger.error('Error in proc_arg_to_datetime erred with {}'.format(pati_err))

    return ret_val


def proc_arg_to_bool(
        input_value: object,
        mapper: object,
        default_value: bool = False) -> bool:
    """ Function processes request arg input to boolean value

    :param input_value:
    :param default_value:
    :param mapper: Dictionary used to map string values to boolean
    :return:
    """

    ret_val = default_value
    if mapper is None:
        mapper = default_str_dict_mapper

    try:
        if input_value is not None and not isinstance(input_value, str):
            ret_val = bool(input_value)
        elif input_value is not None and isinstance(input_value, str):
            mapped_value = mapper.get(input_value)
            if mapped_value is not None:
                ret_val = mapped_value
            else:
                ret_val = default_value
        else:
            ret_val = default_value
    except Exception as pati_err:
        logger.error('Error in proc_arg_to_bool proc_arg_to_int erred with {}'.format(pati_err))

    return ret_val
