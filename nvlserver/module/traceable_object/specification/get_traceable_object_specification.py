#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_traceable_object_list_query = """
SELECT tob.id                                                             AS id,
       tob.name                                                           AS name,
       tob.traceable_object_type_id                                       AS traceable_object_type_id,
       tobt.name                                                          AS traceable_object_type_name,
       tob.user_id                                                        AS user_id,
       usr.fullname                                                       AS user_fullname,
       tob.note                                                           AS note,
       tob.show_on_map                                                    AS show_on_map,
       tob.action                                                         AS action,
       tob.collision_avoidance_system                                     AS collision_avoidance_system,
       coalesce(tob.meta_information ->> 'consumption', '')               AS consumption,
       coalesce(tob.meta_information ->> 'registration_number', '')       AS registration_number,
       coalesce(tob.meta_information ->> 'vin_number', '')                AS vin_number,
       coalesce((tob.meta_information ->> 'vehicle_brand_id')::INT, NULL) AS vehicle_brand_id,
       coalesce(tob.meta_information ->> 'vehicle_model', '')             AS vehicle_model,
       coalesce((tob.meta_information ->> 'vehicle_model_id')::INT, NULL) AS vehicle_model_id,
       coalesce(tob.meta_information ->> 'vehicle_year', '')              AS vehicle_year,
       coalesce(tob.meta_information ->> 'vehicle_default_throttle', '')  AS vehicle_default_throttle,
       (hmcs.meta_information->'action_list')::json AS                       action_list,
       tob.active                                                         AS active,
       tob.deleted                                                        AS deleted
FROM public.traceable_object AS tob
        LEFT OUTER JOIN public.hw_module_command_state AS hmcs ON hmcs.traceable_object_id = tob.id
        LEFT OUTER JOIN public.traceable_object_type AS tobt ON tobt.id = tob.traceable_object_type_id
        LEFT OUTER JOIN public.user AS usr ON usr.id = tob.user_id
WHERE tob.deleted is FALSE
  AND ($1::BIGINT is NULL OR tob.user_id = $1::BIGINT)
    AND (
      $2::VARCHAR is NULL OR
      tob.name ILIKE $2::VARCHAR || '%' OR
      tob.name ILIKE '%' || $2::VARCHAR || '%' OR
      tob.name ILIKE $2::VARCHAR || '%')
"""


get_traceable_object_list_dropdown_query = """
SELECT tob.id                       AS id,
       tob.name                     AS name
FROM public.traceable_object AS tob
WHERE tob.deleted is FALSE
 -- AND tob.active is TRUE
  AND ($1::BIGINT = 0 OR tob.user_id = $1::BIGINT)
  AND ($2::VARCHAR is NULL OR tob.name ILIKE $2::VARCHAR || '%')
"""


get_traceable_object_list_count_query = """
SELECT count(*) AS traceable_object_count
FROM public.traceable_object AS tob
        LEFT OUTER JOIN public.hw_module_command_state AS hmcs ON hmcs.traceable_object_id = tob.id
         LEFT OUTER JOIN public.traceable_object_type AS tobt ON tobt.id = tob.traceable_object_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = tob.user_id
WHERE tob.deleted is FALSE
  AND tob.active is TRUE
  AND ($1::BIGINT is NULL OR tob.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      tob.name ILIKE $2::VARCHAR || '%' OR
      tob.name ILIKE '%' || $2::VARCHAR || '%' OR
      tob.name ILIKE $2::VARCHAR || '%')
"""


get_traceable_object_element_query = """
SELECT tob.id                                                             AS id,
       tob.name                                                           AS name,
       tob.traceable_object_type_id                                       AS traceable_object_type_id,
       tobt.name                                                          AS traceable_object_type_name,
       tob.user_id                                                        AS user_id,
       usr.fullname                                                       AS user_fullname,
       tob.note                                                           AS note,
       tob.show_on_map                                                    AS show_on_map,
       tob.action                                                         AS action,
       tob.collision_avoidance_system                                     AS collision_avoidance_system,
       coalesce(tob.meta_information ->> 'consumption', '')               AS consumption,
       coalesce(tob.meta_information ->> 'registration_number', '')       AS registration_number,
       coalesce(tob.meta_information ->> 'vin_number', '')                AS vin_number,
       coalesce(tob.meta_information ->> 'vehicle_brand', '')             AS vehicle_brand,
       coalesce((tob.meta_information ->> 'vehicle_brand_id')::INT, NULL) AS vehicle_brand_id,
       coalesce(tob.meta_information ->> 'vehicle_model', '')             AS vehicle_model,
       coalesce((tob.meta_information ->> 'vehicle_model_id')::INT, NULL) AS vehicle_model_id,
       coalesce(tob.meta_information ->> 'vehicle_year', '')              AS vehicle_year,
       coalesce(tob.meta_information ->> 'vehicle_default_throttle', '')  AS vehicle_default_throttle,
       tob.active                                                         AS active,
       tob.deleted                                                        AS deleted
FROM public.traceable_object AS tob
         LEFT OUTER JOIN public.traceable_object_type AS tobt ON tobt.id = tob.traceable_object_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = tob.user_id
WHERE tob.deleted is FALSE
  -- AND tob.active is TRUE
    AND ($1::BIGINT is NULL OR tob.user_id = $1::BIGINT)
    AND tob.id = $2::BIGINT;
"""


get_traceable_object_element_by_name_query = """
SELECT tob.id                                                             AS id,
       tob.name                                                           AS name,
       tob.traceable_object_type_id                                       AS traceable_object_type_id,
       tobt.name                                                          AS traceable_object_type_name,
       tob.user_id                                                        AS user_id,
       usr.fullname                                                       AS user_fullname,
       tob.note                                                           AS note,
       tob.show_on_map                                                    AS show_on_map,
       tob.action                                                         AS action,
       tob.collision_avoidance_system                                     AS collision_avoidance_system,
       coalesce(tob.meta_information ->> 'consumption', '')               AS consumption,
       coalesce(tob.meta_information ->> 'registration_number', '')       AS registration_number,
       coalesce(tob.meta_information ->> 'vin_number', '')                AS vin_number,
       coalesce(tob.meta_information ->> 'vehicle_brand', '')             AS vehicle_brand,
       coalesce((tob.meta_information ->> 'vehicle_brand_id')::INT, NULL) AS vehicle_brand_id,
       coalesce(tob.meta_information ->> 'vehicle_model', '')             AS vehicle_model,
       coalesce((tob.meta_information ->> 'vehicle_model_id')::INT, NULL) AS vehicle_model_id,
       coalesce(tob.meta_information ->> 'vehicle_year', '')              AS vehicle_year,
       coalesce(tob.meta_information ->> 'vehicle_default_throttle', '')  AS vehicle_default_throttle,
       tob.active                                                         AS active,
       tob.deleted                                                        AS deleted
FROM public.traceable_object AS tob
         LEFT OUTER JOIN public.traceable_object_type AS tobt ON tobt.id = tob.traceable_object_type_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = tob.user_id
WHERE tob.deleted is FALSE
  -- AND tob.active is TRUE
  AND ($1::BIGINT is NULL OR tob.user_id = $1::BIGINT)
    AND (
      $2::VARCHAR is NULL OR
      tob.name ILIKE $2::VARCHAR || '%' OR
      tob.name ILIKE '%' || $1::VARCHAR || '%' OR
      tob.name ILIKE $2::VARCHAR || '%')
    LIMIT 1;
"""
