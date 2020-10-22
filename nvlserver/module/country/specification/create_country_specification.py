#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_country_element_query = """
INSERT INTO public.country AS cnt
(name, active, deleted)
VALUES
($1, $2, FALSE) RETURNING *;
"""
