#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_traceable_object_type_element_query = """
UPDATE public.traceable_object_type AS tobt
 SET active = False, deleted = True
 WHERE tobt.id = $2::BIGINT RETURNING *;
 """
