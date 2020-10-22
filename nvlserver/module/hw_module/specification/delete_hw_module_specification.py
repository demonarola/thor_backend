#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_hw_module_element_query = """
UPDATE  public.hw_module AS hwm
 SET active = False, deleted = True
 WHERE hwm.id = $1::BIGINT RETURNING *;
 """
