#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
create_account_type_element_query = """
INSERT INTO public.account_type AS atc
(name, active, deleted)
VALUES
($1, $2, FALSE) RETURNING *;
"""
