#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
delete_account_type_element_permanent_query = "DELETE FROM public.account_type AS atc WHERE atc.id = $1 RETURNING *;"

delete_account_type_element_query = """
UPDATE public.account_type AS atc SET deleted = TRUE, 
 active = FALSE WHERE atc.id = $1 RETURNING *;
 """
