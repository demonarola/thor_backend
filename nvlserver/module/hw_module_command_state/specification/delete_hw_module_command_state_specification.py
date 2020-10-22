#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

''' NOT USABLE CODE STATE CALCULATED ON POSTGRESQL SIDE
delete_hw_module_command_state_element_query = """
UPDATE  public.hw_module_command_state AS hmcs
 SET active = False, deleted = True
 WHERE hmcs.id = $1::BIGINT RETURNING *;
 """
'''