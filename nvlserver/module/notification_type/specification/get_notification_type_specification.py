#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_notification_type_list_query = """
SELECT *
    FROM public.notification_type AS nt
    WHERE nt.deleted is FALSE
AND nt.active is TRUE
AND (
      $1::VARCHAR is NULL OR
      nt.name ILIKE $1::VARCHAR || '%' OR
      nt.name ILIKE '%' || $1::VARCHAR || '%' OR
      nt.name ILIKE $1::VARCHAR || '%')
"""
