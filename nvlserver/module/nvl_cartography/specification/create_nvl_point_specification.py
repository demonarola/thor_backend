#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_nvl_point_element_query = """
INSERT INTO public.nvl_point AS npt
(user_id, geom, label, color, icon, location_id, meta_information, active, deleted)
VALUES
($1, $2::geometry, $3, $4, $5, $6, $7, $8, FALSE) RETURNING *;
"""
