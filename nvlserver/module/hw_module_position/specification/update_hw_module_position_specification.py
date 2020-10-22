#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


update_hw_module_position_element_query = """
UPDATE  public.hw_module_position AS hmp
 SET traceable_object_id = $2, 
  hw_module_id = $3,
  position = $4,
  raw_nmea = $5,
  meta_information = $6,
  show_on_map = $7,
  active = $8
 WHERE hmp.id = $1::BIGINT RETURNING *;
 """
