#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


# HW_MODULE_POSITION USER QUERY

get_hw_module_user_position_list_query = """
SELECT hmup.id                                     AS id,
       hmup.user_id                                AS user_id,
       u.fullname                                  AS user_fullname,
       hmup.traceable_object_id                    AS traceable_object_id,
       hmup.hw_module_id                           AS hw_module_id,
       ST_FlipCoordinates(hmup.position)::geometry AS position,
       hmup.meta_information::json                 AS meta_information,
       hmup.record_time                            AS record_time,
       hmup.show_on_map                            AS show_on_map,
       hmup.active                                 AS active,
       hmup.deleted                                AS deleted
FROM public.hw_module_user_position AS hmup
         LEFT OUTER JOIN "user" u on hmup.user_id = u.id
WHERE hmup.deleted is FALSE
  AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
  AND ($2::BIGINT is NULL OR hmup.hw_module_id = $2::BIGINT)
"""

get_hw_module_user_position_list_count_query = """
SELECT count(*) AS hw_module_user_position_count
FROM public.hw_module_user_position AS hmup
WHERE hmup.deleted is FALSE
  AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
  AND ($2::BIGINT is NULL OR hmup.hw_module_id = $2::BIGINT)
"""

get_hw_module_user_position_element_query = """
SELECT hmup.id                                     AS id,
       hmup.user_id                                AS user_id,
       u.fullname                                  AS user_fullname,
       hmup.traceable_object_id                    AS traceable_object_id,
       hmup.hw_module_id                           AS hw_module_id,
       ST_FlipCoordinates(hmup.position)::geometry AS position,
       hmup.meta_information::json                 AS meta_information,
       hmup.record_time                            AS record_time,
       hmup.show_on_map                            AS show_on_map,
       hmup.active                                 AS active,
       hmup.deleted                                AS deleted
FROM public.hw_module_user_position AS hmup
         LEFT OUTER JOIN "user" u on hmup.user_id = u.id
WHERE hmup.deleted is FALSE
  AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
  AND hmup.id = $2
"""


get_hw_module_user_last_point_element_query = """
select hmup.hw_module_id,
       tob.name AS vehicle_name,
       (now() - hmup.created_on)::interval < '5 seconds'::interval AS gprs_active,
       (jsonb_set(tob.meta_information,
        '{action_list}',
        hmcs.meta_information->'action_list'))::json as vehicle_data,
       ST_FlipCoordinates(hmup.position) as position,
       hmup.meta_information::json as data
from hmup_state AS hmups
LEFT OUTER JOIN public.hw_module_user_position AS hmup ON hmups.hw_module_user_position_id = hmup.id
LEFT OUTER JOIN public.traceable_object AS tob ON tob.id = hmup.traceable_object_id
LEFT OUTER JOIN public.hw_module_command_state AS hmcs ON hmcs.traceable_object_id = tob.id
WHERE hmup.deleted IS FALSE
  AND hmup.active IS TRUE
  AND tob.show_on_map IS TRUE
  AND (hmup.meta_information->>'gps_active')::boolean is true
  AND ($2::BIGINT is NULL OR hmups.user_id = $2::BIGINT)
  AND hmups.hw_module_id = any($1::integer[])
order by hmups.record_time desc ;
"""


get_hw_module_user_last_point_element_by_traceable_object_id_query = """
select hmup.hw_module_id,
       tob.name AS vehicle_name,
       (now() - hmup.created_on)::interval < '5 seconds'::interval AS gprs_active,
       (jsonb_set(tob.meta_information,
        '{action_list}',
        hmcs.meta_information->'action_list'))::json as vehicle_data,
       ST_FlipCoordinates(hmup.position) as position,
       hmup.meta_information::json as data
from public.hw_module_user_position AS hmup
LEFT OUTER JOIN public.traceable_object AS tob ON tob.id = hmup.traceable_object_id
LEFT OUTER JOIN public.hw_module_command_state AS hmcs ON hmcs.traceable_object_id = tob.id
WHERE hmup.deleted IS FALSE
  AND hmup.active IS TRUE
  AND tob.show_on_map IS TRUE
  AND tob.deleted IS FALSE
  AND (hmup.meta_information->>'gps_active')::boolean is true
  AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
  AND hmcs.traceable_object_id = $2::BIGINT
order by hmup.record_time desc LIMIT 1;
"""


get_hw_module_list_user_linestring_list_query = """
select ST_FlipCoordinates(st_makeline(position)) as line,
       hw_module_id
from (select hmup.hw_module_id, hmup.position
      from public.hw_module_user_position AS hmup
      WHERE hmup.deleted IS FALSE
        AND hmup.active IS TRUE
        AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
        AND hmup.hw_module_id = any ($2)
        AND (hmup.meta_information->>'gps_active')::boolean is true
        AND ($3::BIGINT is NULL OR hmup.record_time >= now() - ($3 || ' seconds')::INTERVAL)
        AND hmup.record_time < now()
      order by hmup.hw_module_id, hmup.record_time)
         as ordered_points
group by hw_module_id
"""

get_hw_module_list_user_linestring_list_timed_query = """
select ST_FlipCoordinates(st_makeline(position)) as line,
       hw_module_id
from (select hmup.hw_module_id, hmup.position
      from public.hw_module_user_position AS hmup
      WHERE hmup.deleted IS FALSE
        AND hmup.active IS TRUE
        AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
        AND hmup.hw_module_id = any ($2)
        AND (hmup.meta_information->>'gps_active')::boolean is true
        AND ($3::timestamptz is NULL OR hmup.record_time >= $3::timestamptz)
        AND ($4::timestamptz is NULL OR hmup.record_time <= $4::timestamptz)
      order by hmup.hw_module_id, hmup.record_time)
         as ordered_points
group by hw_module_id
"""

get_hw_module_user_linestring_list_query = """
select ST_FlipCoordinates(st_makeline(position)) as line,
       hw_module_id
from (select hmup.hw_module_id, hmup.position
      from public.hw_module_user_position AS hmup
      WHERE hmup.deleted IS FALSE
        AND hmup.active IS TRUE
        AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
        AND (hmup.meta_information->>'gps_active')::boolean is true
        AND ($2::BIGINT is NULL OR hmup.record_time >= now() - ($2 || ' seconds')::INTERVAL)
        AND hmup.record_time < now()
      order by hmup.hw_module_id, hmup.record_time, hmup.position)
         as ordered_points
group by hw_module_id
"""


get_hw_module_user_linestring_list_timed_query = """
select ST_FlipCoordinates(st_makeline(position)) as line,
       hw_module_id
from (select hmup.hw_module_id, hmup.position
      from public.hw_module_user_position AS hmup
      WHERE hmup.deleted IS FALSE
        AND hmup.active IS TRUE
        AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
        AND (hmup.meta_information->>'gps_active')::boolean is true
        AND ($2::timestamptz is NULL OR hmup.record_time >= $2::timestamptz)
        AND ($3::timestamptz is NULL OR hmup.record_time <= $3::timestamptz)
      order by hmup.hw_module_id, hmup.record_time, hmup.position)
         as ordered_points
group by hw_module_id
"""


get_hw_module_user_last_point_list_query = """
select DISTINCT ON (hw_module_id) hw_module_id,
                                  ST_FlipCoordinates(position) as pos
from (SELECT hw_module_id, position
      FROM (
               select hw_module_id, position
               from public.hw_module_user_position AS hmup
               WHERE hmup.deleted IS FALSE
                 AND hmup.active IS TRUE
                 AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
                 AND ($2::BIGINT is NULL OR
                      hmup.record_time >= now() - ($2 || ' seconds')::INTERVAL)
                    AND hmup.record_time < now()
               order by hmup.record_time desc)
               AS odt
      order by hw_module_id) as ordered_points
group by hw_module_id, position
"""

get_hw_module_list_user_last_point_list_query = """
select DISTINCT ON (hw_module_id) hw_module_id,
                                  ST_FlipCoordinates(position) as pos
from (SELECT hw_module_id, position
      FROM (
               select hw_module_id, position
               from public.hw_module_user_position AS hmup
               WHERE hmup.deleted IS FALSE
                 AND hmup.active IS TRUE
                 AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
                 AND hmup.hw_module_id = any ($2)
                 AND ($3::BIGINT is NULL OR
                      hmup.record_time >= now() - ($3 || ' seconds')::INTERVAL)
                     -- AND hmup.record_time < now()
               order by hmup.record_time desc)
               AS odt
      order by hw_module_id) as ordered_points
group by hw_module_id, position
"""

get_hw_module_user_position_list_count_query = """
SELECT count(*) AS hw_module_position_count
FROM public.hw_module_user_position AS hmup
WHERE hmup.deleted is FALSE
  AND ($1::BIGINT is NULL OR hmup.user_id = $1::BIGINT)
  AND ($2::BIGINT is NULL OR hmup.hw_module_id = $2::BIGINT)
"""
