#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

get_account_type_list_query = """
SELECT *
    FROM public.account_type AS atc
    WHERE atc.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      atc.name ILIKE $1::VARCHAR || '%' OR
      atc.name ILIKE '%' || $1::VARCHAR || '%' OR
      atc.name ILIKE $1::VARCHAR || '%')
"""

get_account_type_list_count_query = """
SELECT count(*) AS account_type_count
    FROM public.account_type AS atc
    WHERE atc.deleted is FALSE
    AND (
      $1::VARCHAR is NULL OR
      atc.name ILIKE $1::VARCHAR || '%' OR
      atc.name ILIKE '%' || $1::VARCHAR || '%' OR
      atc.name ILIKE $1::VARCHAR || '%')
"""

get_account_type_element_query = """
SELECT *
    FROM public.account_type AS atc
    WHERE atc.deleted is FALSE
AND atc.id = $1;
"""

get_account_type_element_by_name_query = """
SELECT *
    FROM public.account_type AS atc
    WHERE atc.deleted is FALSE
AND atc.name = $1 LIMIT 1;
"""

get_account_type_list_dropdown_query = """
SELECT atc.id      AS id,
       atc.name    AS name
FROM public.account_type AS atc
WHERE atc.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      atc.name ILIKE $1::VARCHAR || '%' OR
      atc.name ILIKE '%' || $1::VARCHAR || '%' OR
      atc.name ILIKE $1::VARCHAR || '%')
"""
