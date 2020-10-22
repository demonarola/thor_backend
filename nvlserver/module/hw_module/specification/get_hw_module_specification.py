#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_hw_module_list_query = """
SELECT hwm.id                               AS id,
       hwm.name                             AS name,
       COALESCE(hwm.module_id::VARCHAR, '') AS module_id,
       hwm.user_id                          AS user_id,
       coalesce(usr.fullname, '')           AS user_name,
       hwm.traceable_object_id              AS traceable_object_id,
       coalesce(tob.name, '')               AS traceable_object_name,
       hwm.meta_information::json           AS meta_information,
       hwm.show_on_map                      AS show_on_map,
       hwm.gprs_active                      AS gprs_active,
       hwm.active                           AS active,
       hwm.deleted                          AS deleted,
       hwm.created_on                       AS created_on,
       hwm.updated_on                       AS updated_on
FROM public.hw_module AS hwm
         LEFT OUTER JOIN public.user AS usr ON usr.id = hwm.user_id
         LEFT OUTER JOIN public.traceable_object AS tob on hwm.traceable_object_id = tob.id
WHERE hwm.deleted is FALSE
  AND ($1::BIGINT IS NULL OR hwm.user_id = $1::BIGINT)
  AND (
      $2::VARCHAR is NULL OR
      hwm.name ILIKE $2::VARCHAR || '%' OR
      hwm.name ILIKE '%' || $2::VARCHAR || '%' OR
      hwm.name ILIKE $2::VARCHAR || '%')
"""


get_hw_module_list_user_id_hw_module_id_list_query = """
SELECT hwm.id                               AS id,
       hwm.name                             AS name,
       COALESCE(hwm.module_id::VARCHAR, '') AS module_id,
       hwm.user_id                          AS user_id,
       hwm.traceable_object_id              AS traceable_object_id,
       hwm.show_on_map                      AS show_on_map,
       hwm.gprs_active                      AS gprs_active,
       hwm.active                           AS active,
       hwm.deleted                          AS deleted,
       hwm.created_on                       AS created_on,
       hwm.updated_on                       AS updated_on
FROM public.hw_module AS hwm
WHERE hwm.deleted is FALSE
  AND hwm.show_on_map IS TRUE
  AND ($1::BIGINT IS NULL OR hwm.user_id = $1::BIGINT)
  AND (array_length($2::int[], 1) IS NULL OR hwm.id = any ($2::int[]))
"""

get_hw_module_list_dropdown_query = """
SELECT hwm.id                       AS id,
       hwm.name                     AS name
FROM public.hw_module AS hwm
WHERE hwm.deleted is FALSE
    AND ($1::BIGINT IS NULL OR hwm.user_id = $1::BIGINT)
    AND (
      $2::VARCHAR is NULL OR
      hwm.name ILIKE $2::VARCHAR || '%' OR
      hwm.name ILIKE '%' || $2::VARCHAR || '%' OR
      hwm.name ILIKE $2::VARCHAR || '%')
"""

get_hw_module_list_count_query = """
SELECT count(*) AS hw_module_count
FROM public.hw_module AS hwm
         LEFT OUTER JOIN public.user AS usr ON usr.id = hwm.user_id
WHERE hwm.deleted is FALSE
    AND ($1::BIGINT is NULL OR hwm.user_id = $1::BIGINT)
    AND (
      $2::VARCHAR is NULL OR
      hwm.name ILIKE $2::VARCHAR || '%' OR
      hwm.name ILIKE '%' || $2::VARCHAR || '%' OR
      hwm.name ILIKE $2::VARCHAR || '%')
"""

get_hw_module_element_query = """
SELECT hwm.id                               AS id,
       hwm.name                             AS name,
       COALESCE(hwm.module_id::VARCHAR, '') AS module_id,
       hwm.user_id                          AS user_id,
       coalesce(usr.fullname, '')           AS user_name,
       hwm.traceable_object_id              AS traceable_object_id,
       coalesce(tob.name, '')               AS traceable_object_name,
       hwm.meta_information::json           AS meta_information,
       hwm.show_on_map                      AS show_on_map,
       hwm.gprs_active                      AS gprs_active,
       hwm.active                           AS active,
       hwm.deleted                          AS deleted,
       hwm.created_on                       AS created_on,
       hwm.updated_on                       AS updated_on
FROM public.hw_module AS hwm
         LEFT OUTER JOIN public.user AS usr ON usr.id = hwm.user_id
         LEFT OUTER JOIN public.traceable_object AS tob on hwm.traceable_object_id = tob.id
WHERE hwm.deleted is FALSE
AND hwm.id = $1;
"""


get_hw_module_element_by_traceable_object_id_query = """
SELECT hwm.id                               AS id,
       hwm.name                             AS name,
       COALESCE(hwm.module_id::VARCHAR, '') AS module_id,
       hwm.user_id                          AS user_id,
       coalesce(usr.fullname, '')           AS user_name,
       hwm.traceable_object_id              AS traceable_object_id,
       coalesce(tob.name, '')               AS traceable_object_name,
       hwm.meta_information::json           AS meta_information,
       hwm.gprs_active                      AS gprs_active,
       hwm.show_on_map                      AS show_on_map,
       hwm.active                           AS active,
       hwm.deleted                          AS deleted,
       hwm.created_on                       AS created_on,
       hwm.updated_on                       AS updated_on
FROM public.hw_module AS hwm
         LEFT OUTER JOIN public.user AS usr ON usr.id = hwm.user_id
         LEFT OUTER JOIN public.traceable_object AS tob on hwm.traceable_object_id = tob.id
WHERE hwm.deleted is FALSE
AND ($1::BIGINT is NULL OR hwm.user_id = $1::BIGINT)
AND hwm.traceable_object_id = $2;
"""


get_hw_module_element_by_name_query = """
SELECT hwm.id                               AS id,
       hwm.name                             AS name,
       COALESCE(hwm.module_id::VARCHAR, '') AS module_id,
       hwm.user_id                          AS user_id,
       coalesce(usr.fullname, '')           AS user_name,
       hwm.traceable_object_id              AS traceable_object_id,
       coalesce(tob.name, '')               AS traceable_object_name,
       hwm.meta_information::json           AS meta_information,
       hwm.gprs_active                      AS gprs_active,
       hwm.show_on_map                      AS show_on_map,
       hwm.active                           AS active,
       hwm.deleted                          AS deleted,
       hwm.created_on                       AS created_on,
       hwm.updated_on                       AS updated_on
FROM public.hw_module AS hwm
         LEFT OUTER JOIN public.user AS usr ON usr.id = hwm.user_id
         LEFT OUTER JOIN public.traceable_object AS tob on hwm.traceable_object_id = tob.id
WHERE hwm.deleted is FALSE
  AND (
      $1::VARCHAR is NULL OR
      hwm.name ILIKE $1::VARCHAR || '%' OR
      hwm.name ILIKE '%' || $1::VARCHAR || '%' OR
      hwm.name ILIKE $1::VARCHAR || '%')
    LIMIT 1;
"""
