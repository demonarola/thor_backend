#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_nvl_position_list_query = """
SELECT hmup.id                                     AS id,
       hmup.user_id                                AS user_id,
       hmup.traceable_object_id                    AS traceable_object_id,
       hmup.hw_module_id                           AS hw_module_id,
       ST_FlipCoordinates(hmup.position)::geometry AS geom,
       hmup.show_on_map                            AS show_on_map,
       hmup.active                                 AS active,
       hmup.meta_information::json                 AS meta_information,
       hmup.record_time                            AS record_time,
       polygon_detect(hmup.id)                     AS in_geofence,
       parse_gps_timestamp(
           (hmup.meta_information ->> 'date')::VARCHAR,
           (hmup.meta_information ->> 'time')::VARCHAR ) AS event_time
FROM public.hw_module_user_position AS hmup
--LEFT OUTER JOIN public.user_hw_action_coolection AS uhac ON uhac.user_id = hmup.user_id 
WHERE ($1::BIGINT = 0 OR hmup.user_id = $1::BIGINT)
  AND ($2::BIGINT = 0 OR hmup.traceable_object_id = $2::BIGINT)
  AND ($3::timestamptz is NULL OR (hmup.created_on >= $3::timestamptz ))
  AND ($4::timestamptz is NULL OR (hmup.created_on <= $4::timestamptz ))
  AND ST_IsEmpty(hmup.position) IS FALSE
"""

get_nvl_position_list_count_query = """
SELECT count(*) AS record_count
FROM public.hw_module_user_position AS hmup
WHERE ($1::BIGINT = 0 OR hmup.user_id = $1::BIGINT)
  AND ($2::BIGINT = 0 OR hmup.traceable_object_id = $2::BIGINT)
  AND ($3::timestamptz is NULL OR (hmup.created_on >= $3::timestamptz ))
  AND ($4::timestamptz is NULL OR (hmup.created_on <= $4::timestamptz))
    AND ST_IsEmpty(hmup.position) IS FALSE
"""


get_nvl_distance_query = """
SELECT
     st_length(ST_Transform(ST_FlipCoordinates(
        st_makeline(position)::geometry), 4326
    )::geography
)
as distance
FROM (
SELECT  hmup.position AS position,
        hmup.record_time
FROM public.hw_module_user_position AS hmup
WHERE ($1::BIGINT = 0 OR hmup.user_id = $1::BIGINT)
  AND ($2::BIGINT = 0 OR hmup.traceable_object_id = $2::BIGINT)
  AND ($3::timestamptz is NULL OR (hmup.created_on >= $3::timestamptz))
  AND ($4::timestamptz is NULL OR (hmup.created_on <= $4::timestamptz))
    AND ST_IsEmpty(hmup.position) IS FALSE
    GROUP BY hmup.record_time, hmup.position
) AS r;
"""
