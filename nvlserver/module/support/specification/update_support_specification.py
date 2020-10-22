#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


update_support_element_query = """
UPDATE  public.support AS supp
 SET email = $2, 
  user_id = $3,
  subject = $4,
  file_uuid = $5,
  file_name = $6,
  message = $7,
  active = $8
 WHERE supp.id = $1::BIGINT RETURNING *;
 """
