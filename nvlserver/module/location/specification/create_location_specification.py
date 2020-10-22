#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_location_element_query = """
INSERT INTO public.location AS loc
(name, location_type_id, user_id, meta_information, show_on_map, active, deleted)
VALUES
($1, $2, $3, $4, $5, $6, FALSE) RETURNING *;
"""
