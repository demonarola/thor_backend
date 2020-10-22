#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


update_rebate_element_query = """
UPDATE public.rebate AS reb
SET value             = $2,
    rebate_is_fixed   = $3,
    meta_information  = $4,
    active            = $5
WHERE reb.id = $1::BIGINT
RETURNING *;
 """
