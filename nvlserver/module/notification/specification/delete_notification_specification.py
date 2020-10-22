#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_notification_element_query = """
UPDATE public.notification AS nt SET deleted = TRUE, 
 active = FALSE WHERE nt.id = $1::BIGINT RETURNING *;
 """
