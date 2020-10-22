#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_location_element_query = """
UPDATE public.location AS loc
SET deleted = TRUE, active = FALSE WHERE 
    ($1::BIGINT = 0 OR loc.user_id = $1::BIGINT)
AND loc.id = $2::BIGINT RETURNING *;
 """
