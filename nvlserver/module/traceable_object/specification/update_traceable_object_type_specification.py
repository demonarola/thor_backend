#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_traceable_object_type_element_query = """
UPDATE  public.traceable_object_type AS tobt
 SET name = $2, 
  active = $3
 WHERE tobt.id = $1::BIGINT RETURNING *;
 """
