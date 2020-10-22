#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_language_element_query = """
INSERT INTO public.language AS lng
(name, short_code, default_language, active, deleted)
VALUES
($1, $2, $3, $4, FALSE) RETURNING *;
"""
