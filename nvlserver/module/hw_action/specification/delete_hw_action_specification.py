#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_hw_action_element_query = """
UPDATE public.hw_action AS ha SET deleted = TRUE, 
 active = FALSE WHERE ha.id = $1::BIGINT RETURNING *;
 """
