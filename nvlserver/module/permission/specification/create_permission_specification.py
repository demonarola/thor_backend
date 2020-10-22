#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

create_permission_element_query = """
INSERT INTO public.permission AS pmr
(module, action, active, deleted, created_on, updated_on)
VALUES
($1::VARCHAR, $2::VARCHAR, $3::bool, FALSE, now(), now()) RETURNING *;
"""

create_account_type_permission_association_query = """
INSERT INTO public.account_type_permission_association AS atpa
    (account_type_id, permission_id)
VALUES ($1::BIGINT, $2::BIGINT) RETURNING *;
"""
