#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
update_timezone_element_query = """
UPDATE public.time_zone AS tz SET
 ('name', abbrev, utc_offset, is_dst, active) = ($2, $3, $4, $5, $6) WHERE tz.id = $1 RETURNING *;
"""
