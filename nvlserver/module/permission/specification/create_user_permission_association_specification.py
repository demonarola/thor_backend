#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

create_user_permission_association_query = """
INSERT INTO public.user_permission_association AS upa
    (user_id, permission_id)
VALUES ($1::BIGINT, $2::BIGINT) RETURNING *;
"""
