#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_hw_module_user_position_element_query = """
UPDATE  public.hw_module_user_position AS hmp
 SET user_id = $2, 
  traceable_object_id = $3,
  hw_module_id = $4,
  position = $5,
  raw_nmea = $6,
  meta_information = $7,
  show_on_map = $8,
  active = $9
 WHERE hmp.id = $1::BIGINT RETURNING *;
 """
