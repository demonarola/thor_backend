#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_hw_action_element_query = """
UPDATE public.hw_action AS hwa
SET name              = $2,
    proto_field       = $3,
    meta_information  = $4,
    active            = $5
WHERE hwa.id = $1::BIGINT
RETURNING *;
 """
