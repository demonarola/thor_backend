#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


get_hw_action_list_query = """
SELECT hwa.id                AS hw_action_id,
       hwa.name              AS name,
       hwa.min_value         AS min_value,
       hwa.max_value         AS max_value,
       hwa.active            AS active,
       hwa.deleted           AS deleted
FROM public.hw_action AS hwa
WHERE hwa.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      hwa.name ILIKE $1::VARCHAR || '%' OR
      hwa.name ILIKE '%' || $1::VARCHAR || '%' OR
      hwa.name ILIKE $1::VARCHAR || '%')
AND (
      $2::VARCHAR is NULL OR
      hwa.meta_information ->> 'action_type'::VARCHAR ILIKE $2::VARCHAR || '%' OR
      hwa.meta_information ->> 'action_type'::VARCHAR ILIKE '%' || $2::VARCHAR || '%' OR
      hwa.meta_information ->> 'action_type'::VARCHAR ILIKE $2::VARCHAR || '%')
"""

get_hw_action_list_count_query = """
SELECT count(*) AS hw_action_count
FROM public.hw_action AS hwa
WHERE hwa.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      hwa.name ILIKE $1::VARCHAR || '%' OR
      hwa.name ILIKE '%' || $1::VARCHAR || '%' OR
      hwa.name ILIKE $1::VARCHAR || '%')
AND (
      $2::VARCHAR is NULL OR
      hwa.meta_information ->> 'action_type'::VARCHAR ILIKE $2::VARCHAR || '%' OR
      hwa.meta_information ->> 'action_type'::VARCHAR ILIKE '%' || $2::VARCHAR || '%' OR
      hwa.meta_information ->> 'action_type'::VARCHAR ILIKE $2::VARCHAR || '%')
"""


get_hw_action_element_query = """
SELECT hwa.id                     AS id,
       hwa.name                   AS name,
       hwa.meta_information::json AS action,
       hwa.min_value              AS min_value,
       hwa.max_value              AS max_value,
       hwa.proto_field            AS proto_field,
       hwa.active                 AS active,
       hwa.deleted                AS deleted
FROM public.hw_action AS hwa
WHERE hwa.deleted is FALSE
AND hwa.id = $1::BIGINT
"""

get_hw_action_list_user_type_query = """
SELECT hwa.id                     AS hw_action_id,
       hwa.name                   AS name,
       (hwa.meta_information ->> 'icon')::VARCHAR AS icon,
       (hwa.meta_information ->> 'type')::VARCHAR  AS data_type,
       (hwa.meta_information ->> 'frontend_action_type')::VARCHAR  AS type,
       'user'                     AS action_type,
       hwa.min_value::INT         AS min_value,
       hwa.max_value::INT         AS max_value,
      -- hwa.proto_field            AS proto_field,
       FALSE                      AS disabled,
       FALSE                      AS state
FROM public.hw_action AS hwa
WHERE hwa.deleted IS FALSE
  AND hwa.active IS TRUE
  AND hwa.meta_information ->> 'action_type'::VARCHAR = 'user';
"""