#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
update_notification_element_read_query = """
UPDATE public.notification AS nt SET read = TRUE
 WHERE nt.id = $1::BIGINT RETURNING *;
 """
