#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_nvl_polygon_element_query = """
INSERT INTO public.nvl_polygon AS npg
(user_id, geom, label, color, location_id, meta_information, active, deleted)
VALUES
($1, $2::geometry, $3, $4, $5, $6, $7, FALSE) RETURNING *;
"""
