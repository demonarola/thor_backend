#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_country_list_query = """
SELECT *
    FROM public.country AS cnt
    WHERE cnt.deleted is FALSE
AND cnt.active is TRUE
AND (
      $1::VARCHAR is NULL OR
      cnt.name ILIKE $1::VARCHAR || '%' OR
      cnt.name ILIKE '%' || $1::VARCHAR || '%' OR
      cnt.name ILIKE $1::VARCHAR || '%')
"""

get_country_list_count_query = """
SELECT count(*) AS country_count
    FROM public.country AS cnt
    WHERE cnt.deleted is FALSE
AND cnt.active is TRUE
AND (
      $1::VARCHAR is NULL OR
      cnt.name ILIKE $1::VARCHAR || '%' OR
      cnt.name ILIKE '%' || $1::VARCHAR || '%' OR
      cnt.name ILIKE $1::VARCHAR || '%')
"""

get_country_element_query = """
SELECT *
    FROM public.country AS cnt
    WHERE cnt.deleted is FALSE
AND cnt.active is TRUE
AND cnt.id = $1;
"""

get_country_element_by_name_query = """
SELECT *
    FROM public.country AS cnt
    WHERE cnt.deleted is FALSE
AND cnt.active is TRUE
AND (
      $1::VARCHAR is NULL OR
      cnt.name ILIKE $1::VARCHAR || '%' OR
      cnt.name ILIKE '%' || $1::VARCHAR || '%' OR
      cnt.name ILIKE $1::VARCHAR || '%')
    LIMIT 1;
"""
