#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'


delete_account_type_permission_association_query = """
DELETE FROM public.account_type_user_association AS atua WHERE 
atua.account_type_id = $1::BIGINT AND atua.permission_id = $2::BIGINT
 RETURNING *;
"""
