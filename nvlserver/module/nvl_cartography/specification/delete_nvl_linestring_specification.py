#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_nvl_linestring_element_query = """
UPDATE public.nvl_linestring AS nls SET deleted = TRUE, 
 active = FALSE WHERE ($1::BIGINT is NULL OR  nls.user_id = $1::BIGINT) AND  nls.id = $2::BIGINT RETURNING *;
 """


delete_nvl_linestring_element_by_location_id_query = """
UPDATE public.nvl_linestring AS nls SET deleted = TRUE, 
 active = FALSE WHERE ($1::BIGINT is NULL OR  nls.user_id = $1::BIGINT) AND nls.location_id = $2::BIGINT RETURNING *;
 """
