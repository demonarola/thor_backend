#!/usr/bin/env python3                    # if user.get('user_id') and user.get('is_superuser'):
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_traceable_object_type_element_query = """
INSERT INTO public.traceable_object_type AS tobt
(name, active, deleted)
VALUES
($1, $2, FALSE) RETURNING *;
"""
