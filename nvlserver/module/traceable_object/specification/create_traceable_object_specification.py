#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_traceable_object_element_query = """
INSERT INTO public.traceable_object AS tob
(user_id, name, traceable_object_type_id, note, meta_information,
 show_on_map, action, collision_avoidance_system, active, deleted)
VALUES
($1, $2, $3, $4, $5, $6, $7, $8, $9, FALSE) RETURNING *;
"""
