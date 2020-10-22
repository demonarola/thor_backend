#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_location_type_element_query = """
INSERT INTO public.location_type AS ltp
(name, active, deleted)
VALUES
($1, $2, FALSE) RETURNING *;
"""
