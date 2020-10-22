#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_location_element_query = """
UPDATE public.location AS loc
SET name             = $2,
    location_type_id = $3,
    user_id          = $4,
    meta_information = $5,
    show_on_map      = $6,
    active           = $7
WHERE loc.id = $1::BIGINT
RETURNING *;
 """
