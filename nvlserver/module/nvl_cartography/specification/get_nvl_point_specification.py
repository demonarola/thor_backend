#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_nvl_point_list_query = """
SELECT npt.id          AS id,
       ST_FlipCoordinates(npt.geom)::geometry        AS geom,
       npt.label       AS label,
       npt.color       AS color,
       npt.icon        AS icon,
       npt.location_id AS location_id,
       npt.user_id     AS user_id,
       npt.active      AS active,
       npt.deleted     AS deleted
FROM public.nvl_point AS npt
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = npt.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npt.user_id
WHERE npt.deleted is FALSE
  AND ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      npt.label ILIKE $2::VARCHAR || '%' OR
      npt.label ILIKE '%' || $2::VARCHAR || '%' OR
      npt.label ILIKE $2::VARCHAR || '%')
"""

get_nvl_point_list_count_query = """
SELECT count(*) AS nvl_point_count
FROM public.nvl_point AS npt
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = npt.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npt.user_id
WHERE npt.deleted is FALSE
  AND ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      npt.label ILIKE $2::VARCHAR || '%' OR
      npt.label ILIKE '%' || $2::VARCHAR || '%' OR
      npt.label ILIKE $2::VARCHAR || '%')
"""


get_nvl_point_element_query = """
SELECT npt.id          AS id,
       ST_FlipCoordinates(npt.geom)::geometry        AS geom,
       npt.label       AS label,
       npt.color       AS color,
       npt.icon        AS icon,
       npt.location_id AS location_id,
       npt.user_id     AS user_id,
       npt.active      AS active,
       npt.deleted     AS deleted
FROM public.nvl_point AS npt
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = npt.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npt.user_id
WHERE npt.deleted is FALSE
  AND ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT)
    AND npt.id = $2::BIGINT
"""

get_nvl_point_element_by_location_id_query = """
SELECT npt.id          AS id,
       ST_FlipCoordinates(npt.geom)::geometry        AS geom,
       npt.label       AS label,
       npt.color       AS color,
       npt.icon        AS icon,
       npt.location_id AS location_id,
       npt.user_id     AS user_id,
       npt.active      AS active,
       npt.deleted     AS deleted
FROM public.nvl_point AS npt
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = npt.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npt.user_id
WHERE npt.deleted is FALSE
  AND ($1::BIGINT is NULL OR  npt.user_id = $1::BIGINT)
    AND npt.location_id = $2::BIGINT
ORDER BY npt.created_on DESC LIMIT 1
"""


get_nvl_point_list_by_user_id_query = """
SELECT npt.id                                 AS id,
       ST_FlipCoordinates(npt.geom)::geometry AS geom,
       npt.label                              AS label,
       npt.color                              AS color,
       npt.location_id                        AS location_id,
       npt.user_id                            AS user_id,
       npt.icon                               AS icon,
       loc.location_type_id                   AS location_type_id,
       ltp.name                               AS location_type,
       loc.user_id                            AS user_id,
       loc.name                               AS location_name,
       usr.fullname                           AS user_fullname,
       loc.show_on_map                        AS show_on_map,
       npt.active                             AS active,
       npt.deleted                            AS deleted
FROM public.nvl_point AS npt
         LEFT OUTER JOIN public.location AS loc ON loc.id = npt.location_id
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npt.user_id
WHERE npt.deleted is FALSE
  AND loc.deleted is FALSE
  AND ($1::BIGINT is NULL OR npt.user_id = $1::BIGINT)
  AND loc.show_on_map IS TRUE
ORDER BY npt.created_on DESC
"""