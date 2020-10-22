#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_town_element_query = """
INSERT INTO public.town AS twn
(country_id, name, active, deleted)
VALUES
($1, $2, $3, FALSE) RETURNING *;
"""
