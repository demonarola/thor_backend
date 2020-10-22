#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_traceable_object_model_list_dropdown_query = """
SELECT tobm.id                       AS id,
       tobm.name                     AS name
FROM public.traceable_object_model AS tobm
WHERE tobm.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      tobm.name ILIKE $1::VARCHAR || '%' OR
      tobm.name ILIKE '%' || $1::VARCHAR || '%' OR
      tobm.name ILIKE $1::VARCHAR || '%')
  AND ($2::BIGINT is NULL OR tobm.traceable_object_brand_id = $2::BIGINT)
"""
