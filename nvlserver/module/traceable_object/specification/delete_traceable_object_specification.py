#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

delete_traceable_object_element_query = """
UPDATE  public.traceable_object AS tob
 SET active = False, deleted = True
 WHERE ($1::BIGINT is NULL OR  tob.user_id = $1::BIGINT) AND tob.id = $2::BIGINT RETURNING *;
 """
