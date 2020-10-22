#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
update_console_element_query = """
UPDATE  public.console AS csl
 SET timestamp = $2, 
  user_id = $3,
  message = $4,
  active = $5
 WHERE csl.id = $1::BIGINT RETURNING *;
 """
