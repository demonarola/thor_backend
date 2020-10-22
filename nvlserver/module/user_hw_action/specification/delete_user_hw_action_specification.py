#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_user_hw_action_element_query = """
UPDATE public.user_hw_action AS uha SET deleted = TRUE, 
 active = FALSE WHERE 
 uha.user_id = $1::BIGINT AND uha.id = $1::BIGINT RETURNING *;
"""
