#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_nvl_polygon_element_query = """
UPDATE public.nvl_polygon AS npg SET 
 user_id = $2::BIGINT,
 {}

 deleted = TRUE
WHERE npg.location_id = $1::BIGINT RETURNING *;
"""
