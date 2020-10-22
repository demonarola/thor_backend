#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_nvl_polygon_element_query = """
UPDATE public.nvl_polygon AS npg SET deleted = TRUE, 
 active = FALSE WHERE ($1::BIGINT = 0 OR  npg.user_id = $1::BIGINT) AND npg.id = $2::BIGINT RETURNING *;
 """


# delete_nvl_polygon_element_by_location_id_query = """
# UPDATE public.nvl_polygon AS npg SET deleted = TRUE,
#  active = FALSE WHERE ($1::BIGINT = 0 OR  npg.user_id = $1::BIGINT) AND  npg.location_id = $2::BIGINT RETURNING *;
#  """


delete_nvl_polygon_element_by_location_id_query = """
DELETE FROM public.nvl_polygon AS npg 
 WHERE ($1::BIGINT = 0 OR npg.user_id = $1::BIGINT) AND  npg.location_id = $2::BIGINT RETURNING *;
 """