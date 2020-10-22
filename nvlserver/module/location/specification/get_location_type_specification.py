#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


get_location_type_list_query = """
SELECT ltp.id      AS id,
       ltp.name    AS name,
       ltp.active  AS active,
       ltp.deleted AS deleted
FROM public.location_type AS ltp
WHERE ltp.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      ltp.name ILIKE $1::VARCHAR || '%' OR
      ltp.name ILIKE '%' || $1::VARCHAR || '%' OR
      ltp.name ILIKE $1::VARCHAR || '%')
"""

get_location_type_list_count_query = """
SELECT count(*) AS location_type_count
FROM public.location_type AS ltp
WHERE ltp.deleted is FALSE
  AND ltp.active is TRUE
  AND (
      $1::VARCHAR is NULL OR
      ltp.name ILIKE $1::VARCHAR || '%' OR
      ltp.name ILIKE '%' || $1::VARCHAR || '%' OR
      ltp.name ILIKE $1::VARCHAR || '%')
"""


get_location_type_element_query = """
SELECT ltp.id      AS id,
       ltp.name    AS name,
       ltp.active  AS active,
       ltp.deleted AS deleted
FROM public.location_type AS ltp
WHERE ltp.deleted is FALSE
AND ltp.id = $1::BIGINT
"""


get_location_type_element_by_name_query = """
SELECT ltp.id      AS id,
       ltp.name    AS name,
       ltp.active  AS active,
       ltp.deleted AS deleted
FROM public.location_type AS ltp
WHERE ltp.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      ltp.name ILIKE $1::VARCHAR || '%' OR
      ltp.name ILIKE '%' || $1::VARCHAR || '%' OR
      ltp.name ILIKE $1::VARCHAR || '%')
 LIMIT 1;
"""

get_location_type_list_dropdown_query = """
SELECT ltp.id      AS id,
       ltp.name    AS name,
       ltp.active  AS active,
       ltp.deleted AS deleted
FROM public.location_type AS ltp
WHERE ltp.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      ltp.name ILIKE $1::VARCHAR || '%' OR
      ltp.name ILIKE '%' || $1::VARCHAR || '%' OR
      ltp.name ILIKE $1::VARCHAR || '%')
"""
