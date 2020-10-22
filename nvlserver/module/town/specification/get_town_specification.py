#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_town_list_query = """
SELECT twn.id         AS id,
       twn.name       AS name,
       twn.country_id AS country_id,
       cnt.name       AS country_name,
       twn.active     AS active,
       twn.deleted    AS deleted
FROM public.town AS twn
         LEFT OUTER JOIN public.country AS cnt ON cnt.id = twn.country_id
WHERE twn.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      twn.name ILIKE $1::VARCHAR || '%' OR
      twn.name ILIKE '%' || $1::VARCHAR || '%' OR
      twn.name ILIKE $1::VARCHAR || '%')

"""

get_town_list_count_query = """
SELECT count(*) AS town_count
    FROM public.town AS twn
    WHERE twn.deleted is FALSE
AND twn.active is TRUE
 AND (
      $1::VARCHAR is NULL OR
      twn.name ILIKE $1::VARCHAR || '%' OR
      twn.name ILIKE '%' || $1::VARCHAR || '%' OR
      twn.name ILIKE $1::VARCHAR || '%')
"""

get_town_element_query = """
SELECT twn.id         AS id,
       twn.name       AS name,
       twn.country_id AS country_id,
       cnt.name       AS country_name,
       twn.active     AS active,
       twn.deleted    AS deleted
FROM public.town AS twn
         LEFT OUTER JOIN public.country AS cnt ON cnt.id = twn.country_id
WHERE twn.deleted is FALSE
  AND twn.active is TRUE
AND twn.id = $1;
"""

get_town_element_by_name_query = """
SELECT twn.id         AS id,
       twn.name       AS name,
       twn.country_id AS country_id,
       cnt.name       AS country_name,
       twn.active     AS active,
       twn.deleted    AS deleted
FROM public.town AS twn
         LEFT OUTER JOIN public.country AS cnt ON cnt.id = twn.country_id
WHERE twn.deleted is FALSE
  AND twn.active is TRUE
 AND (
      $1::VARCHAR is NULL OR
      twn.name ILIKE $1::VARCHAR || '%' OR
      twn.name ILIKE '%' || $1::VARCHAR || '%' OR
      twn.name ILIKE $1::VARCHAR || '%')
    LIMIT 1;
"""
