#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

get_permission_list_query = """
SELECT pmr.id         AS id,
       pmr.module     AS module,
       pmr.action     AS action,
       pmr.created_on AS created_on,
       pmr.updated_on AS updated_on
FROM public.permission AS pmr
WHERE pmr.deleted is FALSE
  AND pmr.active is TRUE
    AND (
      $1::VARCHAR is NULL OR
      pmr.module ILIKE $1::VARCHAR || '%' OR
      pmr.module ILIKE '%' || $1::VARCHAR || '%' OR
      pmr.module ILIKE $1::VARCHAR || '%')
  AND (
      $2::VARCHAR is NULL OR
      pmr.action ILIKE $2::VARCHAR || '%' OR
      pmr.action ILIKE '%' || $2::VARCHAR || '%' OR
      pmr.action ILIKE $2::VARCHAR || '%')
"""

get_permission_list_count_query = """
SELECT count(*) AS permission_count
FROM public.permission AS pmr
WHERE pmr.deleted is FALSE
  AND pmr.active is TRUE
  AND (
      $1::VARCHAR is NULL OR
      pmr.module ILIKE $1::VARCHAR || '%' OR
      pmr.module ILIKE '%' || $1::VARCHAR || '%' OR
      pmr.module ILIKE $1::VARCHAR || '%')
  AND (
      $2::VARCHAR is NULL OR
      pmr.action ILIKE $2::VARCHAR || '%' OR
      pmr.action ILIKE '%' || $2::VARCHAR || '%' OR
      pmr.action ILIKE $2::VARCHAR || '%')
"""

get_permission_element_query = """
SELECT pmr.id         AS id,
       pmr.module     AS module,
       pmr.action     AS action,
       pmr.created_on AS created_on,
       pmr.updated_on AS updated_on
FROM public.permission AS pmr
WHERE pmr.deleted is FALSE
  AND pmr.active is TRUE
  AND pmr.id = $1;
"""


get_permission_list_by_user_id_query = """
SELECT usr.account_type_id                            AS acount_type_id,
       p.id                                           AS permission_id,
       p.module || ':' || p.action AS permission
FROM public.user AS usr
         LEFT OUTER JOIN account_type AS act ON act.id = usr.account_type_id
         LEFT OUTER JOIN public.user_permission_association AS upa ON upa.user_id = usr.id
         LEFT OUTER JOIN account_type_permission_association AS atpa ON atpa.account_type_id = usr.account_type_id
         LEFT OUTER JOIN permission p on upa.permission_id = p.id
WHERE atpa.permission_id = upa.permission_id
  AND usr.id = $1::BIGINT
"""


get_permission_module_list_by_user_id_query = """
SELECT DISTINCT(p.module) AS module_name
FROM public.user AS usr
         LEFT OUTER JOIN account_type AS act ON act.id = usr.account_type_id
         LEFT OUTER JOIN public.user_permission_association AS upa ON upa.user_id = usr.id
         LEFT OUTER JOIN account_type_permission_association AS atpa ON atpa.account_type_id = usr.account_type_id
         LEFT OUTER JOIN permission p on upa.permission_id = p.id
WHERE atpa.permission_id = upa.permission_id
  AND usr.id = $1::BIGINT
"""
