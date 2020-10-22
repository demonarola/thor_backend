#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
create_timezone_element_query = """
INSERT INTO public.time_zone AS tz
(name, abbrev, utc_offset, is_dst, active, deleted)
VALUES
($1, $2, $3, $4, $5, FALSE) RETURNING *;
"""
