#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_user_hw_action_element_query = """
INSERT INTO public.user_hw_action AS uhwa
(user_id, hw_action_id, value, date_from, date_to, active, deleted)
VALUES
($1, $2, $3, $4, $5, $6, FALSE) RETURNING *;
"""
