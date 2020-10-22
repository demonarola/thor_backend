#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_nvl_circle_element_partial_query = """
UPDATE public.nvl_circle AS ncr SET 
 user_id = $2::BIGINT,
 {}
 deleted = FALSE
WHERE ncr.location_id = $1::BIGINT RETURNING *;
"""

update_nvl_circle_element_query = """
UPDATE public.nvl_circle AS ncr SET 
 user_id = $2::BIGINT,
 geom = $3::geometry,
 label = $4::VARCHAR,
 color = $5::VARCHAR,
 location_id = $6::BIGINT,
 radius = $7::NUMERIC,
 meta_information = $8::jsonb,
 active = $9::BOOLEAN,
 deleted = TRUE
WHERE ncr.id = $1::BIGINT RETURNING *;
"""
