#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
update_account_type_element_query = """
UPDATE public.account_type AS atc SET
 (name, active) = ($2, $3) WHERE atc.id = $1 RETURNING *;
"""
