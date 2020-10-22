#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_hw_action_element_query = """
INSERT INTO public.hw_action AS hwa
(name, proto_field, meta_information, min_value, max_value, active, deleted, created_on, updated_on)
VALUES
($1, $2, $3, $4, $5, $6, FALSE, now(), now()) RETURNING *;
"""
