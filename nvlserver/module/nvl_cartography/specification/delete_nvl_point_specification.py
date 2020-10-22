#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_nvl_point_element_query = """
UPDATE public.nvl_point AS npt SET deleted = TRUE, 
 active = FALSE WHERE ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT) AND  npt.id = $2::BIGINT RETURNING *;
 """

delete_nvl_point_element_by_location_id_query = """
UPDATE public.nvl_point AS npt SET deleted = TRUE, 
 active = FALSE WHERE ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT) AND  npt.location_id = $2::BIGINT RETURNING *;
 """
