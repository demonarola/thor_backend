#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_nvl_point_element_query = """
UPDATE public.nvl_point AS npt SET read = TRUE
  WHERE ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT) AND npt.id = $2::BIGINT RETURNING *;
 """

update_nvl_point_element_partial_query = """
UPDATE public.nvl_point AS npr SET 
 user_id = $2::BIGINT,
 {}
 deleted = FALSE
WHERE npr.location_id = $1::BIGINT RETURNING *;
"""