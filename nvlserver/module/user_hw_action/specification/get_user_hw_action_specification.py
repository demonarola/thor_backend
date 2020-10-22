#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


get_user_hw_action_list_query = """
SELECT hwa.id                AS id,
       uhwa.user_id          AS user_id,
       uhwa.value            as value,
       hwa.name              AS action_name,
       hwa.hw_action_type_id AS hw_action_type_id,
       hwat.name             AS hw_action_type,
       hwa.min_value         AS action_min_value,
       hwa.max_value         AS action_max_value,
       hwa.active            AS active,
       hwa.deleted           AS deleted
FROM public.user_hw_action AS uhwa
    LEFT OUTER JOIN public.hw_action AS hwa ON hwa.id =  uhwa.hw_action_id
    LEFT OUTER JOIN public.hw_action_type AS hwat ON hwat.id = hwa.hw_action_type_id
WHERE uhwa.deleted is FALSE
  AND ($1::BIGINT is NULL OR uhwa.user_id = $1::BIGINT)
      AND (
      $2::VARCHAR is NULL OR
      hwa.name ILIKE $2::VARCHAR || '%' OR
      hwa.name ILIKE '%' || $2::VARCHAR || '%' OR
      hwa.name ILIKE $2::VARCHAR || '%')
"""

get_user_hw_action_list_count_query = """
SELECT count(*) AS user_hw_action_count
FROM public.user_hw_action AS uhwa
    LEFT OUTER JOIN public.hw_action AS hwa ON hwa.id =  uhwa.hw_action_id
    LEFT OUTER JOIN public.hw_action_type AS hwat ON hwat.id = hwa.hw_action_type_id
WHERE uhwa.deleted is FALSE
  AND ($1::BIGINT is NULL OR uhwa.user_id = $1::BIGINT)
    AND (
      $2::VARCHAR is NULL OR
      hwa.name ILIKE $2::VARCHAR || '%' OR
      hwa.name ILIKE '%' || $2::VARCHAR || '%' OR
      hwa.name ILIKE $2::VARCHAR || '%')
"""


get_user_hw_action_element_query = """
SELECT hwa.id                AS id,
       uhwa.user_id          AS user_id,
       uhwa.value            as value,
       hwa.name              AS action_name,
       hwa.hw_action_type_id AS hw_action_type_id,
       hwat.name             AS hw_action_type,
       hwa.min_value         AS action_min_value,
       hwa.max_value         AS action_max_value,
       hwa.active            AS active,
       hwa.deleted           AS deleted
FROM public.user_hw_action AS uhwa
    LEFT OUTER JOIN public.hw_action AS hwa ON hwa.id =  uhwa.hw_action_id
    LEFT OUTER JOIN public.hw_action_type AS hwat ON hwat.id = hwa.hw_action_type_id
WHERE uhwa.deleted is FALSE
AND uhwa.user_id = $1::BIGINT
AND uhwa.id = $2::BIGINT
"""


get_user_hw_action_times_by_location_id_query = """
SELECT coalesce(
to_char(min(date_from), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), NULL ) AS min_date,
 coalesce(to_char(max(date_to), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), NULL) AS max_date FROM public.user_hw_action AS uha
LEFT OUTER JOIN public.user_hw_action_location_association AS uhala ON uha.id = uhala.user_hw_action_id
WHERE uhala.location_id = $1;"""
