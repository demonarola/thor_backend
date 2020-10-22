#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_nvl_linestring_element_query = """
UPDATE public.nvl_linestring AS nls SET read = TRUE
  WHERE ($1::BIGINT is NULL OR  nls.user_id = $1::BIGINT) AND nls.id = $2::BIGINT RETURNING *;
 """


update_nvl_linestring_element_partial_query = """
UPDATE public.nvl_linestring AS nls SET 
 user_id = $2::BIGINT,
 {}
 deleted = FALSE
WHERE npr.location_id = $1::BIGINT RETURNING *;
"""