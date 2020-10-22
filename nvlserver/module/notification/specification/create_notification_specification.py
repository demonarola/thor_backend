#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_notification_element_query = """
INSERT INTO public.notification AS nt
(name, description, notification_type_id, read, active, deleted)
VALUES
($1, $2, $3, $4, $5, FALSE) RETURNING *;
"""
