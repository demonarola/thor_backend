#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_user_element_permanent_query = 'DELETE FROM public."user" AS usr WHERE usr.id = $1 RETURNING *;'

delete_user_element_query = """
UPDATE public."user" AS usr SET deleted = TRUE, 
 active = FALSE WHERE usr.id = $1 RETURNING *;
 """
