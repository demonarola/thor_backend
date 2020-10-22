#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_console_element_query = """
INSERT INTO public.console_view AS csl
(timestamp, user_id, message, active, deleted)
VALUES
($1, $2, $3, $4, FALSE) RETURNING *;
"""
