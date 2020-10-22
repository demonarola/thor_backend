#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_language_element_permanent_query = "DELETE FROM public.language AS lng WHERE lng.id = $1 RETURNING *;"

delete_language_element_query = """
UPDATE public.language AS lng SET deleted = TRUE, 
 active = FALSE WHERE lng.id = $1 RETURNING *;
 """
