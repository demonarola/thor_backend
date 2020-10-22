#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'


create_account_type_permission_association_query = """
INSERT INTO public.account_type_permission_association AS atpa
    (account_type_id, permission_id)
VALUES ($1::BIGINT, $2::BIGINT) RETURNING *;
"""
