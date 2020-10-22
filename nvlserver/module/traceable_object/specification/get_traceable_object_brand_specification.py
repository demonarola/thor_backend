#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_traceable_object_brand_list_dropdown_query = """
SELECT tobb.id                       AS id,
       tobb.name                     AS name
FROM public.traceable_object_brand AS tobb
WHERE tobb.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      tobb.name ILIKE $1::VARCHAR || '%' OR
      tobb.name ILIKE '%' || $1::VARCHAR || '%' OR
      tobb.name ILIKE $1::VARCHAR || '%')
"""
