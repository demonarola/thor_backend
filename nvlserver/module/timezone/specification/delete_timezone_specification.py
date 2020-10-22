#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
delete_timezone_element_permanent_query = "DELETE FROM public.time_zone AS tz WHERE tz.id = $1 RETURNING *;"

delete_timezone_element_query = """
UPDATE public.time_zone AS tz SET deleted = TRUE, 
 active = FALSE WHERE tz.id = $1 RETURNING *;
 """
