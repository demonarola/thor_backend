#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_hw_module_element_query = """
UPDATE  public.hw_module AS hwm
 SET name = COALESCE($2, name), 
  module_id = $3,
  user_id = $4,
  traceable_object_id = $5,
  meta_information = $6,
  show_on_map = $7,
  active = $8
 WHERE hwm.id = $1::BIGINT RETURNING *;
 """


update_user_hw_module_element_query = """
UPDATE  public.hw_module AS hwm
 SET traceable_object_id = $3,
  meta_information = $4,
  show_on_map = $5,
  active = $6
 WHERE hwm.id = $1::BIGINT AND hwm.user_id = $2::BIGINT RETURNING *;
 """
