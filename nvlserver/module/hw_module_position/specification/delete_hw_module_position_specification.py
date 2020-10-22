#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


delete_hw_module_position_element_query = """
UPDATE  public.hw_module_position AS hmp
    SET active = False, deleted = True
WHERE hmp.id = $1::BIGINT RETURNING *;
 """

delete_hw_module_position_all_query = """
UPDATE  public.hw_module_position AS hmp
    SET active = False, deleted = True
WHERE hmp.active=True;
UPDATE  public.hw_module_position AS hmup
    SET active = False, deleted = True
WHERE hmup.active=True;
"""
