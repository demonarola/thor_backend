#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
# HW_MODULE POSITION QUERY

get_hw_module_position_list_query = """
SELECT hmp.id                                     AS id,
       hmp.traceable_object_id                    AS traceable_object_id,
       hmp.hw_module_id                           AS hw_module_id,
       ST_FlipCoordinates(hmp.position)::geometry AS position,
       hmp.raw_nmea                               AS raw_nmea,
       hmp.meta_information::json                 AS meta_information,
       hmp.raw_nmea                               AS raw_nmea,
       hmp.record_time                            AS record_time,
       hmp.show_on_map                            AS show_on_map,
       hmp.active                                 AS active,
       hmp.deleted                                AS deleted
FROM public.hw_module_position AS hmp
WHERE hmp.deleted is FALSE
  AND ($1::BIGINT is NULL OR hmp.hw_module_id = $1::BIGINT)
"""

get_hw_module_linestring_list_query = """
select ST_FlipCoordinates(st_makeline(position)) as line,
       hw_module_id
from (select hmp.hw_module_id, hmp.position
      from public.hw_module_position AS hmp
      WHERE hmp.deleted IS FALSE
        AND hmp.active IS TRUE
        AND ($1::BIGINT is NULL OR hmp.hw_module_id = $1::BIGINT)
      order by hmup.hw_module_id, hmup.created_on, hmup.position)
         as ordered_points
group by hw_module_id
"""

get_hw_module_last_point_list_query = """
select DISTINCT ON (hw_module_id) hw_module_id,
                                  ST_FlipCoordinates(position) as pos
from (SELECT hw_module_id, position
      FROM (
               select hw_module_id, position
               from public.hw_module_position AS hmp
               WHERE hmp.deleted IS FALSE
                 AND hmp.active IS TRUE
                 AND ($1::BIGINT is NULL OR hmp.hw_module_id = $1::BIGINT)
               order by hmp.created_on desc)
               AS odt
      order by hw_module_id) as ordered_points
group by hw_module_id, position
"""

get_hw_module_position_list_count_query = """
SELECT count(*) AS hw_module_position_count
FROM public.hw_module_position AS hmp
WHERE hmp.deleted is FALSE
  AND ($2::BIGINT is NULL OR hmp.hw_module_id = $2::BIGINT)
"""

get_hw_module_position_element_query = """
SELECT hmps.id                                     AS id,
       hmp.traceable_object_id                    AS traceable_object_id,
       hmp.hw_module_id                           AS hw_module_id,
       ST_FlipCoordinates(hmp.position)::geometry AS position,
       hmp.raw_nmea                               AS raw_nmea,
       hmp.record_time                            AS record_time,
       hmp.meta_information::json                 AS meta_information,
       hmp.raw_nmea                               AS raw_nmea,
       hmp.show_on_map                            AS show_on_map,
       hmp.active                                 AS active,
       hmp.deleted                                AS deleted
FROM public.hw_module_position AS hmp
WHERE hmp.deleted is FALSE
  AND hmp.id = $1
"""
