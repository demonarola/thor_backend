#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
update_town_element_query = """
UPDATE  public.town AS twn
 SET country_id = $2, 
  name = $3,
  active = $4
 WHERE twn.id = $1::BIGINT RETURNING *;
 """
