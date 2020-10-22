#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_hw_module_position_element_query = """
INSERT INTO public.hw_module_position AS hmp
(traceable_object_id, hw_module_id, position, raw_nmea, meta_information, record_time, show_on_map, active, deleted)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, FALSE)
RETURNING *;
"""
