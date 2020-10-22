#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_notification_type_element_query = """
INSERT INTO public.notification_type AS nt
(name, active, deleted)
VALUES
($1, $2, FALSE) RETURNING *;
"""
