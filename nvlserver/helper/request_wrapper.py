#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from copy import deepcopy
from math import ceil

response_format = {
    "content": [],
    "pageable": {
        "sort": {
            "sorted": False,
            "unsorted": True,
            "empty": True
        },
        "pageNumber": 0,
        "pageSize": 0,
        "offset": 0,
        "unpaged": False,
        "paged": True
    },
    "totalElements": 0,
    "totalPages": 0,
    "last": False,
    "first": False,
    "sort": {
        "sorted": False,
        "unsorted": True,
        "empty": True
    },
    "size": 0,
    "number": 0,
    "numberOfElements": 0,
    "empty": True
}


async def populate_response_format(
        content: list,
        content_count: int,
        page: int,
        size: int) -> dict:
    """ Return formatted response used for filtering sorting data on a frontend.

    :param content:
    :param content_count:
    :param page:
    :param size:
    :return:
    """
    # print(content, content_count)
    res_format_dta = deepcopy(response_format)
    if size != 0:
        res_format_dta['size'] = size
        res_format_dta['number'] = len(content)

        if len(content) != 0:
            res_format_dta['content'] = content
            res_format_dta['empty'] = False

        if page != 0:
            res_format_dta['pageable']['pageNumber'] = page
            res_format_dta['pageable']['pageSize'] = size
            res_format_dta['pageable']['offset'] = page * size

        if content_count != 0:
            res_format_dta['totalElements'] = content_count
            res_format_dta['totalPages'] = ceil(content_count / size)
            res_format_dta['numberOfElements'] = content_count

        ret_val = res_format_dta

    else:
        ret_val = res_format_dta

    return ret_val
