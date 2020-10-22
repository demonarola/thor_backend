#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_rebate_element_query = """
INSERT INTO public.rebate AS reb
(value, rebate_is_fixed, meta_information, active, deleted)
VALUES
($1, $2, $3, $4,  FALSE) RETURNING *;
"""
