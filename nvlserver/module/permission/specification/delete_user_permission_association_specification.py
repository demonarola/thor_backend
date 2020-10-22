#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'

delete_user_permission_association_query = """
DELETE FROM public.user_permission_association AS upa WHERE upa.user_id = $1::BIGINT AND upa.permission_id = $2::BIGINT
 RETURNING *;
"""

delete_user_permission_association_by_user_id_query = """
DELETE FROM public.user_permission_association AS upa WHERE upa.user_id = $1::BIGINT RETURNING *;
"""

