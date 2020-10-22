#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


get_location_list_query = """
SELECT loc.id               AS id,
       loc.name             AS name,
       loc.location_type_id AS location_type_id,
       ltp.name             AS location_type,
       loc.user_id          AS user_id,
       usr.fullname         AS user_fullname,
       loc.show_on_map      AS show_on_map,
       loc.active           AS active,
       loc.deleted          AS deleted
FROM public.location AS loc
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = loc.user_id
WHERE loc.deleted is FALSE
  AND (
      $1::VARCHAR is NULL OR
      loc.name ILIKE $1::VARCHAR || '%' OR
      loc.name ILIKE '%' || $1::VARCHAR || '%' OR
      loc.name ILIKE $1::VARCHAR || '%')
  AND ($2::BIGINT is NULL OR loc.user_id = $2::BIGINT)
"""


get_location_geography_list_query = """
SELECT loc.id               AS id,
       loc.name             AS name,
       loc.location_type_id AS location_type_id,
       ltp.name             AS location_type,
       loc.user_id          AS user_id,
       usr.fullname         AS user_fullname,
       loc.show_on_map      AS show_on_map,
       loc.active           AS active,
       loc.deleted          AS deleted
FROM public.location AS loc
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = loc.user_id
WHERE loc.deleted is FALSE
  AND loc.show_on_map IS TRUE
  AND ($1::BIGINT is NULL OR loc.user_id = $1::BIGINT)
"""

get_location_list_count_query = """
SELECT count(*) AS location_count
FROM public.location AS loc
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = loc.user_id
WHERE loc.deleted is FALSE
  AND (
      $1::VARCHAR is NULL OR
      loc.name ILIKE $1::VARCHAR || '%' OR
      loc.name ILIKE '%' || $1::VARCHAR || '%' OR
      loc.name ILIKE $1::VARCHAR || '%')
  AND ($2::BIGINT is NULL OR loc.user_id = $2::BIGINT)
"""


get_location_element_query = """
SELECT loc.id               AS id,
       loc.name             AS name,
       loc.location_type_id AS location_type_id,
       ltp.name             AS location_type,
       loc.user_id          AS user_id,
       (loc.meta_information ->> 'modules')::json AS  modules,
       usr.fullname         AS user_fullname,
       loc.show_on_map      AS show_on_map,
       loc.active           AS active,
       loc.deleted          AS deleted
FROM public.location AS loc
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = loc.user_id
WHERE loc.deleted is FALSE
AND ($1::BIGINT is NULL OR $1::BIGINT = 0 OR usr.id = $1::BIGINT)
AND loc.id = $2::BIGINT
"""
