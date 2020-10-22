#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_nvl_circle_element_query = """
UPDATE public.nvl_circle AS ncr SET deleted = TRUE, 
 active = FALSE WHERE ($1::BIGINT is NULL OR  npg.user_id = $1::BIGINT) AND ncr.id = $2::BIGINT RETURNING *;
 """


# delete_nvl_circle_element_by_location_id_query = """
# UPDATE public.nvl_circle AS ncr SET deleted = TRUE,
#  active = FALSE WHERE ($1::BIGINT is NULL OR  ncr.user_id = $1::BIGINT) AND ncr.location_id = $2::BIGINT RETURNING *;
#  """


delete_nvl_circle_element_by_location_id_query = """
DELETE FROM public.nvl_circle AS ncr 
WHERE ($1::BIGINT is NULL OR  ncr.user_id = $1::BIGINT) AND ncr.location_id = $2::BIGINT RETURNING *;
"""