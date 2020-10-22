#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


delete_hw_module_user_position_element_query = """
UPDATE  public.hw_module_user_position AS hmup
    SET active = False, deleted = True
WHERE hmup.id = $1::BIGINT RETURNING *;
 """


delete_hw_module_user_position_all_query = """
UPDATE  public.hw_module_user_position AS hmup
    SET active = False, deleted = True
WHERE hmup.active=True;
"""