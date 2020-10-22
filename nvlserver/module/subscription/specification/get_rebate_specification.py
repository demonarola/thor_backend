#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_rebate_list_query = """
SELECT reb.id                     AS id,
       reb.value                  AS value,
       reb.rebate_is_fixed        AS rebate_is_fixed,
       reb.meta_information::json AS meta_information,
       reb.active                 AS active,
       reb.deleted                AS deleted
FROM public.rebate AS reb
WHERE reb.deleted is FALSE
--  AND reb.active is TRUE
  AND ($1::NUMERIC is NULL OR reb.value = $1::NUMERIC)
  AND ($2::BOOLEAN is NULL OR reb.rebate_is_fixed = $2::BOOLEAN)
"""

get_rebate_list_dropdown_query = """
SELECT reb.id                       AS id,
       reb.value                    AS value,
       reb.rebate_is_fixed          AS rebate_is_fixed
FROM public.rebate AS reb
WHERE reb.deleted is FALSE
  AND ($1::NUMERIC is NULL OR reb.value = $1::NUMERIC)
  AND reb.rebate_is_fixed = $2
"""

get_rebate_list_count_query = """
SELECT count(*) AS rebate_count
FROM public.rebate AS reb
WHERE reb.deleted is FALSE
  AND ($1::NUMERIC is NULL OR reb.value = $1::NUMERIC)
  AND ($2::BOOLEAN is NULL OR reb.rebate_is_fixed = $2::BOOLEAN)
"""

get_rebate_element_query = """
SELECT reb.id                     AS id,
       reb.value                  AS value,
       reb.rebate_is_fixed        AS rebate_is_fixed,
       reb.meta_information::json AS meta_information,
       reb.active                 AS active,
       reb.deleted                AS deleted
FROM public.rebate AS reb
WHERE reb.deleted is FALSE
AND reb.id = $1;
"""
