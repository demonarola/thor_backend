#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_nvl_polygon_list_query = """
SELECT npg.id          AS id,
       ST_FlipCoordinates(npg.geom)::geometry        AS geom,
       npg.label       AS label,
       npg.color       AS color,
       npg.location_id AS location_id,
       npg.user_id     AS user_id,
       npg.active      AS active,
       npg.deleted     AS deleted
FROM public.nvl_polygon AS npg
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = npg.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npg.user_id
WHERE npg.deleted is FALSE
  AND ($1::BIGINT is NULL OR  npg.user_id = $1::BIGINT)
    AND (
      $2::VARCHAR is NULL OR
      npg.label ILIKE $2::VARCHAR || '%' OR
      npg.label ILIKE '%' || $2::VARCHAR || '%' OR
      npg.label ILIKE $2::VARCHAR || '%')

"""

get_nvl_polygon_list_count_query = """
SELECT count(*) AS nvl_polygon_count
FROM public.nvl_polygon AS npg
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = npg.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npg.user_id
WHERE npg.deleted is FALSE
  AND ($1::BIGINT is NULL OR  npg.user_id = $1::BIGINT)
AND (
      $2::VARCHAR is NULL OR
      npg.label ILIKE $2::VARCHAR || '%' OR
      npg.label ILIKE '%' || $2::VARCHAR || '%' OR
      npg.label ILIKE $2::VARCHAR || '%')
"""


get_nvl_polygon_element_query = """
SELECT npg.id          AS id,
       ST_FlipCoordinates(npg.geom)::geometry        AS geom,
       npg.label       AS label,
       npg.color       AS color,
       npg.location_id AS location_id,
       npg.user_id     AS user_id,
       npg.active      AS active,
       npg.deleted     AS deleted
FROM public.nvl_polygon AS npg
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = npg.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npg.user_id
WHERE npg.deleted is FALSE
    AND ($1::BIGINT is NULL OR  npg.user_id = $1::BIGINT)
    AND npg.id = $2::BIGINT
"""


get_nvl_polygon_element_by_location_id_query = """
SELECT npg.id          AS id,
       ST_FlipCoordinates(npg.geom)::geometry        AS geom,
       npg.label       AS label,
       npg.color       AS color,
       npg.location_id AS location_id,
       npg.user_id     AS user_id,
       npg.active      AS active,
       npg.deleted     AS deleted
FROM public.nvl_polygon AS npg
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = npg.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npg.user_id
WHERE npg.deleted is FALSE
    AND ($1::BIGINT is NULL OR  npg.user_id = $1::BIGINT)
    AND npg.location_id = $2::BIGINT
ORDER BY npg.created_on DESC LIMIT 1
"""


get_nvl_polygon_list_by_user_id_query = """
SELECT npg.id                                 AS id,
       ST_FlipCoordinates(npg.geom)::geometry AS geom,
       npg.label                              AS label,
       npg.color                              AS color,
       npg.location_id                        AS location_id,
       npg.user_id                            AS user_id,
       loc.location_type_id                   AS location_type_id,
       ltp.name                               AS location_type,
       loc.user_id                            AS user_id,
       loc.name                               AS location_name,
       usr.fullname                           AS user_fullname,
       loc.show_on_map                        AS show_on_map,
       npg.active                             AS active,
       npg.deleted                            AS deleted
FROM public.nvl_polygon AS npg
         LEFT OUTER JOIN public.location AS loc ON loc.id = npg.location_id
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = npg.user_id
WHERE npg.deleted is FALSE
  AND ($1::BIGINT is NULL OR npg.user_id = $1::BIGINT)
  AND loc.deleted is FALSE
  AND loc.show_on_map IS TRUE
ORDER BY npg.created_on DESC
"""
