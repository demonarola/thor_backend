#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_user_hw_action_element_query = """
UPDATE public.user_hw_action AS uhwa
SET user_id      = $2,
    hw_action_id = $3,
    value        = $4,
    date_from    = $5,
    date_to      = $6,
    active       = $7,
    updated_on   = now()
WHERE uhwa.id = $1::BIGINT
RETURNING *;
 """
