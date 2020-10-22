#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_location_type_element_query = """
UPDATE public.location_type AS ltp
SET name      = $2,
    active    = $3
WHERE ltp.id = $1::BIGINT
RETURNING *;
 """
