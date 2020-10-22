#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_rent_element_query = """
UPDATE public.user_hw_command AS rnt SET deleted = TRUE, 
 active = FALSE WHERE rnt.id = $1::BIGINT RETURNING *;
"""
