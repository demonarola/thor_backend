#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


get_traceable_object_type_list_query = """
SELECT tobt.id                       AS id,
       tobt.name                     AS name,
       tobt.active                   AS active,
       tobt.deleted                  AS deleted
FROM public.traceable_object_type AS tobt
WHERE tobt.deleted is FALSE
   AND (
      $1::VARCHAR is NULL OR
      tobt.name ILIKE $1::VARCHAR || '%' OR
      tobt.name ILIKE '%' || $1::VARCHAR || '%' OR
      tobt.name ILIKE $1::VARCHAR || '%')
"""


get_traceable_object_type_list_dropdown_query = """
SELECT tobt.id                       AS id,
       tobt.name                     AS name
FROM public.traceable_object_type AS tobt
WHERE tobt.deleted is FALSE
   AND (
      $1::VARCHAR is NULL OR
      tobt.name ILIKE $1::VARCHAR || '%' OR
      tobt.name ILIKE '%' || $1::VARCHAR || '%' OR
      tobt.name ILIKE $1::VARCHAR || '%')
"""


get_traceable_object_type_element_by_name_query = """
SELECT tobt.id                       AS id,
       tobt.name                     AS name,
       tobt.active                   AS active,
       tobt.deleted                  AS deleted
FROM public.traceable_object_type AS tobt
WHERE tobt.deleted is FALSE
   AND (
      $1::VARCHAR is NULL OR
      tobt.name ILIKE $1::VARCHAR || '%' OR
      tobt.name ILIKE '%' || $1::VARCHAR || '%' OR
      tobt.name ILIKE $1::VARCHAR || '%')
    LIMIT 1;
"""


get_traceable_object_type_element_query = """
SELECT tobt.id                       AS id,
       tobt.name                     AS name,
       tobt.active                   AS active,
       tobt.deleted                  AS deleted
FROM public.traceable_object_type AS tobt
WHERE tobt.deleted is FALSE
  -- AND tobt.active is TRUE
AND tobt.id = $1;
"""


get_traceable_object_type_list_count_query = """
SELECT count(*) AS traceable_object_type_count
FROM public.traceable_object_type AS tobt
WHERE tobt.deleted is FALSE
   AND (
      $1::VARCHAR is NULL OR
      tobt.name ILIKE $1::VARCHAR || '%' OR
      tobt.name ILIKE '%' || $1::VARCHAR || '%' OR
      tobt.name ILIKE $1::VARCHAR || '%')
"""
