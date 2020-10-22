#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


hw_module_random_str_unique_query = """
SELECT *
FROM public.hw_module_random_str AS hmrs
WHERE hmrs.unique_str
          NOT IN (SELECT module_id FROM public.hw_module)
LIMIT 1;
"""

hw_module_random_str_unique_unassigned_list_query = """
SELECT hmrs.id         AS hwrs_id,
       hmrs.unique_str AS module_id
FROM public.hw_module_random_str AS hmrs
WHERE hmrs.unique_str not in (
    SELECT module_id
    FROM hw_module AS hm
    WHERE hm.deleted IS FALSE
) AND (
      $1::VARCHAR is NULL OR
      hmrs.unique_str ILIKE $1::VARCHAR || '%' OR
      hmrs.unique_str ILIKE '%' || $1::VARCHAR || '%' OR
      hmrs.unique_str ILIKE $1::VARCHAR || '%')
"""
