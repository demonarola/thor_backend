#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_town_element_query = """
UPDATE  public.town AS twn
 SET active = False, deleted = True
 WHERE twn.id = $1::BIGINT RETURNING *;
 """
