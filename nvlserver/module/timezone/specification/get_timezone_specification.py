#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'


get_timezone_list_query = """
SELECT *
    FROM public.time_zone AS tmz
    WHERE tmz.deleted is FALSE
      AND (
      $1::VARCHAR is NULL OR
      tmz.name ILIKE $1::VARCHAR || '%' OR
      tmz.name ILIKE '%' || $1::VARCHAR || '%' OR
      tmz.name ILIKE $1::VARCHAR || '%')
"""

get_timezone_list_count_query = """
SELECT count(*) AS timezone_count
     FROM public.time_zone AS tmz
    WHERE tmz.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      tmz.name ILIKE $1::VARCHAR || '%' OR
      tmz.name ILIKE '%' || $1::VARCHAR || '%' OR
      tmz.name ILIKE $1::VARCHAR || '%')
"""

get_timezone_element_query = """
SELECT *
    FROM public.time_zone AS tmz
    WHERE tmz.deleted is FALSE
AND tmz.id = $1 
"""

get_timezone_element_by_name_query = """
SELECT *
    FROM public.time_zone AS tmz
    WHERE tmz.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      tmz.name ILIKE $1::VARCHAR || '%' OR
      tmz.name ILIKE '%' || $1::VARCHAR || '%' OR
      tmz.name ILIKE $1::VARCHAR || '%')
"""

get_timezone_element_by_code_query = """
SELECT *
    FROM public.time_zone AS tmz
    WHERE tmz.deleted is FALSE
AND tmz.name = $1::VARCHAR LIMIT 1;
"""

get_timezone_list_dropdown_query = """
SELECT tmz.id      AS id,
       tmz.name    AS name,
       tmz.active  AS active,
       tmz.deleted AS deleted
FROM public.time_zone AS tmz
WHERE tmz.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      tmz.name ILIKE $1::VARCHAR || '%' OR
      tmz.name ILIKE '%' || $1::VARCHAR || '%' OR
      tmz.name ILIKE $1::VARCHAR || '%')
"""
