#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_nvl_linestring_list_query = """
SELECT nls.id          AS id,
       ST_FlipCoordinates(nls.geom)::geometry        AS geom,
       nls.label       AS label,
       nls.color       AS color,
       nls.location_id AS location_id,
       nls.user_id     AS user_id,
       nls.active      AS active,
       nls.deleted     AS deleted
FROM public.nvl_linestring AS nls
         LEFT OUTER JOIN  public.location AS nloc ON nloc.id = nls.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = nls.user_id
WHERE nls.deleted is FALSE
  AND ($1::BIGINT is NULL OR  nls.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      nls.label ILIKE $2::VARCHAR || '%' OR
      nls.label ILIKE '%' || $2::VARCHAR || '%' OR
      nls.label ILIKE $2::VARCHAR || '%')
"""

get_nvl_linestring_list_count_query = """
SELECT count(*) AS nvl_linestring_count
FROM public.nvl_linestring AS nls
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = nls.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = nls.user_id
WHERE nls.deleted is FALSE
  AND ($1::BIGINT is NULL OR nls.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      nls.label ILIKE $2::VARCHAR || '%' OR
      nls.label ILIKE '%' || $2::VARCHAR || '%' OR
      nls.label ILIKE $2::VARCHAR || '%') 
"""


get_nvl_linestring_element_query = """
SELECT nls.id                                 AS id,
       ST_FlipCoordinates(nls.geom)::geometry AS geom,
       nls.label                              AS label,
       nls.color                              AS color,
       nls.location_id                        AS location_id,
       nls.user_id                            AS user_id,
       nls.active                             AS active,
       nls.deleted                            AS deleted
FROM public.nvl_linestring AS nls
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = nls.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = nls.user_id
WHERE nls.deleted is FALSE
  AND ($1::BIGINT is NULL OR nls.user_id = $1::BIGINT)
  AND nls.id = $2::BIGINT
"""

get_nvl_linestring_element_by_location_id_query = """
SELECT nls.id                                 AS id,
       ST_FlipCoordinates(nls.geom)::geometry AS geom,
       nls.label                              AS label,
       nls.color                              AS color,
       nls.location_id                        AS location_id,
       nls.user_id                            AS user_id,
       nls.active                             AS active,
       nls.deleted                            AS deleted
FROM public.nvl_linestring AS nls
         LEFT OUTER JOIN public.location AS nloc ON nloc.id = nls.location_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = nls.user_id
WHERE nls.deleted is FALSE
  AND ($1::BIGINT is NULL OR nls.user_id = $1::BIGINT)
  AND nls.location_id = $2::BIGINT
ORDER BY nls.created_on DESC
LIMIT 1
"""


get_nvl_linestring_list_by_user_id_query = """
SELECT nls.id                                 AS id,
       ST_FlipCoordinates(nls.geom)::geometry AS geom,
       nls.label                              AS label,
       nls.color                              AS color,
       nls.location_id                        AS location_id,
       nls.user_id                            AS user_id,
       loc.location_type_id                   AS location_type_id,
       ltp.name                               AS location_type,
       loc.user_id                            AS user_id,
       loc.name                               AS location_name,
       usr.fullname                           AS user_fullname,
       loc.show_on_map                        AS show_on_map,
       nls.active                             AS active,
       nls.deleted                            AS deleted
FROM public.nvl_linestring AS nls
         LEFT OUTER JOIN public.location AS loc ON loc.id = nls.location_id
         LEFT OUTER JOIN public.location_type AS ltp ON ltp.id = loc.location_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = nls.user_id
WHERE nls.deleted is FALSE
  AND loc.deleted is FALSE
  AND ($1::BIGINT is NULL OR nls.user_id = $1::BIGINT)
  AND loc.show_on_map IS TRUE
ORDER BY nls.created_on DESC
"""