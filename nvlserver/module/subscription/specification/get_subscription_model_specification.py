#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_subscription_model_list_query = """
SELECT subm.id                     AS id,
       subm.description            AS description,
       subm.duration_month         AS duration_month,
       subm.price_per_unit         AS price_per_unit,
       subm.meta_information::json AS meta_information,
       subm.active                 AS active,
       subm.deleted                AS deleted
FROM public.subscription_model AS subm
WHERE subm.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      subm.description ILIKE $1::VARCHAR || '%' OR
      subm.description ILIKE '%' || $1::VARCHAR || '%' OR
      subm.description ILIKE $1::VARCHAR || '%')
  AND ($2::VARCHAR is NULL OR subm.duration_month = $2::BIGINT)
  AND ($3::VARCHAR is NULL OR subm.price_per_unit = $3::BIGINT)
"""

get_subscription_model_list_dropdown_query = """
SELECT subm.id                       AS id,
       subm.description              AS description
FROM public.subscription_model AS subm
WHERE subm.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      subm.description ILIKE $1::VARCHAR || '%' OR
      subm.description ILIKE '%' || $1::VARCHAR || '%' OR
      subm.description ILIKE $1::VARCHAR || '%')
"""

get_subscription_model_list_count_query = """
SELECT count(*) AS subscription_model_count
FROM public.subscription_model AS subm
WHERE subm.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      subm.description ILIKE $1::VARCHAR || '%' OR
      subm.description ILIKE '%' || $1::VARCHAR || '%' OR
      subm.description ILIKE $1::VARCHAR || '%')
  AND ($2::VARCHAR is NULL OR subm.duration_month = $2::BIGINT)
  AND ($3::VARCHAR is NULL OR subm.price_per_unit = $3::BIGINT)
"""

get_subscription_model_element_query = """
SELECT subm.id                     AS id,
       subm.description            AS description,
       subm.duration_month         AS duration_month,
       subm.price_per_unit         AS price_per_unit,
       subm.meta_information::json AS meta_information,
       subm.active                 AS active,
       subm.deleted                AS deleted
FROM public.subscription_model AS subm
WHERE subm.deleted is FALSE
AND subm.id = $1;
"""
