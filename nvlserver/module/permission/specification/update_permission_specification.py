#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

update_permission_element_query = """
UPDATE public.permission AS pmr
SET (module, action, active, updated_on) = (
$2::VARCHAR, $3::VARCHAR, $4::BOOLEAN, now())
WHERE pmr.id::BIGINT = $1
RETURNING *;
"""
