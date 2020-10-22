#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_hw_module_element_query = """
INSERT INTO public.hw_module AS hwm
(name, module_id, user_id, traceable_object_id, meta_information, show_on_map, active, deleted)
VALUES
($1, $2, $3, $4, $5, $6, $7, FALSE) RETURNING *;
"""
