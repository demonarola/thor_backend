#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
update_language_element_query = """
UPDATE public.language AS lng SET
 (name, short_code, default_language, active) = ($2, $3, $4, $5) WHERE lng.id = $1 RETURNING *;
"""
