#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
get_request_log_by_route_query = """
SELECT rlg.id            AS id,
       rlg.route         AS route,
       rlg.request_data  AS request_data,
       rlg.response_data AS response_data,
       rlg.created_on    AS created_on,
       rlg.updated_on    AS updated_on,
       rlg.active        AS active,
       rlg.deleted       AS deleted
FROM public.request_logger AS rlg
WHERE rlg.deleted is FALSE
  AND rlg.active is TRUE
  AND ($1::VARCHAR is NULL OR rlg.route ILIKE $1::VARCHAR || '%')
"""
