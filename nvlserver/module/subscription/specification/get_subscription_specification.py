#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_subscription_list_query = """
SELECT sub.id                                    AS id,
       sub.subscription_uuid::VARCHAR            AS subscription_uuid,
       sub.user_id                               AS user_id,
       usr.fullname                              AS user_fullname,
       sub.subscription_model_id                 AS subscription_model_id,
       subm.description                          AS subscription_model_description,
       sub.rebate_id                             AS rebate_id,
       coalesce(reb.rebate_is_fixed, FALSE)      AS rebate_is_fixed,
       coalesce(reb.value, 0)::NUMERIC           AS rebate_value,
       sub.meta_information::json                AS meta_information,
       sub.unit_count                            AS unit_count,
       sub.date_from                             AS date_from,
       sub.date_to                               AS date_to,
       sub.active                                AS active,
       sub.deleted                               AS deleted
FROM public.subscription AS sub
         LEFT OUTER JOIN public.subscription_model AS subm ON subm.id = sub.subscription_model_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = sub.user_id
         LEFT OUTER JOIN public.rebate AS reb ON reb.id = sub.rebate_id
WHERE sub.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      sub.subscription_uuid::VARCHAR ILIKE $1::VARCHAR || '%' OR
      sub.subscription_uuid::VARCHAR ILIKE '%' || $1::VARCHAR || '%' OR
      sub.subscription_uuid::VARCHAR ILIKE $1::VARCHAR || '%')
  AND ($2::VARCHAR is NULL OR sub.user_id = $2::BIGINT)
  AND ($3::VARCHAR is NULL OR sub.subscription_model_id = $3::BIGINT)
"""

get_subscription_list_count_query = """
SELECT count(*) AS subscription_count
FROM public.subscription AS sub
         LEFT OUTER JOIN public.subscription_model AS subm ON subm.id = sub.subscription_model_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = sub.user_id
         LEFT OUTER JOIN public.rebate AS reb ON reb.id = sub.rebate_id
WHERE sub.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      sub.subscription_uuid::VARCHAR ILIKE $1::VARCHAR || '%' OR
      sub.subscription_uuid::VARCHAR ILIKE '%' || $1::VARCHAR || '%' OR
      sub.subscription_uuid::VARCHAR ILIKE $1::VARCHAR || '%')
  AND ($2::VARCHAR is NULL OR sub.user_id = $2::BIGINT)
  AND ($3::VARCHAR is NULL OR sub.subscription_model_id = $3::BIGINT)
"""

get_subscription_element_query = """
SELECT sub.id                                    AS id,
       sub.subscription_uuid::VARCHAR            AS subscription_id,
       sub.user_id                               AS user_id,
       usr.fullname                              AS user_fullname,
       sub.subscription_model_id                 AS subscription_model_id,
       subm.description                          AS subscription_model_description,
       sub.rebate_id                             AS rebate_id,
       coalesce(reb.rebate_is_fixed, FALSE)      AS rebate_is_fixed,
       coalesce(reb.value, 0)::NUMERIC           AS rebate_value,
       sub.meta_information::json                AS meta_information,
       sub.unit_count                            AS unit_count,
       sub.date_from                             AS date_from,
       sub.date_to                               AS date_to,
       sub.active                                AS active,
       sub.deleted                               AS deleted
FROM public.subscription AS sub
         LEFT OUTER JOIN public.subscription_model AS subm ON subm.id = sub.subscription_model_id
         LEFT OUTER JOIN public.user AS usr ON usr.id = sub.user_id
         LEFT OUTER JOIN public.rebate AS reb ON reb.id = sub.rebate_id
WHERE sub.deleted is FALSE
AND sub.id = $1;
"""
