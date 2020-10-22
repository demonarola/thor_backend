#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_language_list_query = """
SELECT *
    FROM public.language AS lng
    WHERE lng.deleted is FALSE
    AND (
      $1::VARCHAR is NULL OR
      lng.name ILIKE $1::VARCHAR || '%' OR
      lng.name ILIKE '%' || $1::VARCHAR || '%' OR
      lng.name ILIKE $1::VARCHAR || '%')
"""

get_language_list_count_query = """
SELECT count(*) AS language_count
     FROM public.language AS lng
    WHERE lng.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      lng.name ILIKE $1::VARCHAR || '%' OR
      lng.name ILIKE '%' || $1::VARCHAR || '%' OR
      lng.name ILIKE $1::VARCHAR || '%')
"""

get_language_element_query = """
SELECT *
    FROM public.language AS lng
    WHERE lng.deleted is FALSE
AND lng.id = $1;
"""

get_language_element_by_name_query = """
SELECT *
    FROM public.language AS lng
    WHERE lng.deleted is FALSE
AND lng.name = $1::VARCHAR;
"""


get_language_element_by_short_code_query = """
SELECT *
    FROM public.language AS lng
    WHERE lng.deleted is FALSE
AND lng.short_code = $1::VARCHAR;
"""


get_language_count_by_name_query = """
SELECT COUNT(*)
    FROM public.language AS lng
    WHERE lng.deleted is FALSE
AND lng.name = $1
 AND ($2::INT is NULL OR lng.id=$2);
"""


get_language_list_dropdown_query = """
SELECT lng.id      AS id,
       lng.name    AS name,
       lng.short_code AS short_code,
       lng.active  AS active,
       lng.deleted AS deleted
FROM public.language AS lng
WHERE lng.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      lng.name ILIKE $1::VARCHAR || '%' OR
      lng.name ILIKE '%' || $1::VARCHAR || '%' OR
      lng.name ILIKE $1::VARCHAR || '%')
"""

