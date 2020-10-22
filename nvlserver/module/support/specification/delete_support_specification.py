#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_support_element_query = """
UPDATE  public.support AS supp
 SET active = False, deleted = True
 WHERE supp.id = $1::BIGINT RETURNING *;
 """
