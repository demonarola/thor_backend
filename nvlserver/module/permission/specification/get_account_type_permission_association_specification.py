#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'


get_permission_list_by_account_type_id_query = """
SELECT act.id                        AS acount_type_id,
       p.id                          AS permission_id,
       p.module || ':' || p.action   AS permission
FROM public.account_type AS act
    LEFT OUTER JOIN public.account_type_permission_association AS atpa ON  act.id = atpa.account_type_id
    LEFT OUTER JOIN public.permission p on p.id = atpa.permission_id
WHERE act.id = $1::BIGINT
"""
