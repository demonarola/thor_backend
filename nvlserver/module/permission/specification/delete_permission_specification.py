#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

delete_permission_element_permanent_query = """
DELETE
FROM public.permission AS pmr
WHERE pmr.id = $1::BIGINT
RETURNING *;
"""

delete_permission_element_query = """
UPDATE public.permission AS pmr
SET deleted = TRUE,
    active  = FALSE
WHERE pmr.id = $1
RETURNING *;
"""

