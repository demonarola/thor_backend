#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_console_element_query = """
UPDATE  public.console AS csl
 SET active = False, deleted = True
 WHERE csl.id = $1::BIGINT RETURNING *;
 """
