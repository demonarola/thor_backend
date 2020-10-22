#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_notification_list_query = """
SELECT 
    nt.id AS id,
    nt.name AS name,
    nt.description AS description,
    nt.notification_type_id AS notification_type_id,
    nty.name                AS notification_type,
    nt.read                 AS read,
    nt.active               AS active,
    nt.deleted              AS deleted
    FROM public.notification AS nt
    LEFT OUTER JOIN public.notification_type AS nty ON nty.id = nt.notification_type_id
    WHERE nt.deleted is FALSE
AND nt.active is TRUE
AND (
      $1::VARCHAR is NULL OR
      nt.name ILIKE $1::VARCHAR || '%' OR
      nt.name ILIKE '%' || $1::VARCHAR || '%' OR
      nt.name ILIKE $1::VARCHAR || '%')
"""

get_notification_list_count_query = """
SELECT count(*) AS notification_count
    FROM public.notification AS nt
    LEFT OUTER JOIN public.notification_type AS nty ON nty.id = nt.notification_type_id
    WHERE nt.deleted is FALSE
AND nt.active is TRUE
AND (
      $1::VARCHAR is NULL OR
      nt.name ILIKE $1::VARCHAR || '%' OR
      nt.name ILIKE '%' || $1::VARCHAR || '%' OR
      nt.name ILIKE $1::VARCHAR || '%')
"""

get_notification_list_unread_count_query = """
SELECT count(*) AS notification_count
    FROM public.notification AS nt
    LEFT OUTER JOIN public.notification_type AS nty ON nty.id = nt.notification_type_id
    WHERE nt.deleted is FALSE
AND nt.active is TRUE
AND nt.read is FALSE
"""

get_notification_element_query = """
SELECT 
    nt.id AS id,
    nt.name AS name,
    nt.description AS description,
    nt.notification_type_id AS notification_type_id,
    nty.name                AS notification_type,
    nt.read                 AS read,
    nt.active               AS active,
    nt.deleted              AS deleted
    FROM public.notification AS nt
    LEFT OUTER JOIN public.notification_type AS nty ON nty.id = nt.notification_type_id
    WHERE nt.deleted is FALSE
AND nt.active is TRUE
AND nt.id = $1::BIGINT
"""
