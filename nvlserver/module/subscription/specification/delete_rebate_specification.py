#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


delete_rebate_element_query = """
UPDATE  public.rebate AS reb
 SET active = False, deleted = True
 WHERE reb.id = $1::BIGINT RETURNING *;
"""
