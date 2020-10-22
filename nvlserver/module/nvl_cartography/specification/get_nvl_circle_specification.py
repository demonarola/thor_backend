#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_nvl_circle_list_query = """
SELECT ncr.id          AS id,
       ST_FlipCoordinates(ncr.geom)::geometry        AS geom,
       ncr.label       AS label,
       ncr.color       AS color,
       ncr.radius      AS radius,
       ncr.location_id AS location_id,
       ncr.user_id     AS user_id,
       ncr.active      AS active,
       ncr.deleted     AS deleted
FROM public.nvl_circle AS ncr
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = ncr.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = ncr.user_id
WHERE ncr.deleted is FALSE
  AND ($1::BIGINT is NULL OR  ncr.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      ncr.label ILIKE $2::VARCHAR || '%' OR
      ncr.label ILIKE '%' || $2::VARCHAR || '%' OR
      ncr.label ILIKE $2::VARCHAR || '%')
"""

get_nvl_circle_list_count_query = """
SELECT count(*) AS nvl_circle_count
FROM public.nvl_circle AS ncr
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = ncr.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = ncr.user_id
WHERE ncr.deleted is FALSE
AND (
      $2::VARCHAR is NULL OR
      ncr.label ILIKE $2::VARCHAR || '%' OR
      ncr.label ILIKE '%' || $2::VARCHAR || '%' OR
      ncr.label ILIKE $2::VARCHAR || '%')
"""


get_nvl_circle_element_query = """
SELECT ncr.id          AS id,
       ST_FlipCoordinates(ncr.geom)::geometry        AS geom,
       ncr.label       AS label,
       ncr.color       AS color,
       ncr.radius      AS radius,
       ncr.location_id AS location_id,
       ncr.user_id     AS user_id,
       ncr.active      AS active,
       ncr.deleted     AS deleted
FROM public.nvl_circle AS ncr
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = ncr.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = ncr.user_id
WHERE ncr.deleted is FALSE
  AND ($1::BIGINT is NULL OR  ncr.user_id = $1::BIGINT)
AND ncr.id = $2::BIGINT
"""


get_nvl_circle_element_by_location_id_query = """
SELECT ncr.id          AS id,
       ST_FlipCoordinates(ncr.geom)::geometry        AS geom,
       ncr.label       AS label,
       ncr.color       AS color,
       ncr.radius      AS radius,
       ncr.location_id AS location_id,
       ncr.user_id     AS user_id,
       ncr.active      AS active,
       ncr.deleted     AS deleted
FROM public.nvl_circle AS ncr
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = ncr.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = ncr.user_id
WHERE ncr.deleted is FALSE
  AND ($1::BIGINT is NULL OR  ncr.user_id = $1::BIGINT)
AND ncr.location_id = $2::BIGINT
ORDER BY ncr.created_on DESC LIMIT 1
"""


get_nvl_circle_list_by_user_id_query = """
SELECT ncr.id                                 AS id,
       ST_FlipCoordinates(ncr.geom)::geometry AS geom,
       ncr.label                              AS label,
       ncr.color                              AS color,
       ncr.location_id                        AS location_id,
       ncr.user_id                            AS user_id,
       ncr.radius                             AS radius,
       loc.location_type_id                   AS location_type_id,
       ltp.name                               AS location_type,
       loc.user_id                            AS user_id,
       loc.name                               AS location_name,
       usr.fullname                           AS user_fullname,
       loc.show_on_map                        AS show_on_map,
       ncr.active                             AS active,
       ncr.deleted                            AS deleted
FROM public.nvl_circle AS ncr
         LEFT OUTER JOIN public.location AS loc ON loc.id = ncr.location_id
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = ncr.user_id
WHERE ncr.deleted is FALSE
  AND loc.deleted is FALSE
  AND ($1::BIGINT is NULL OR ncr.user_id = $1::BIGINT)
  AND loc.show_on_map IS TRUE
ORDER BY ncr.created_on DESC
"""
