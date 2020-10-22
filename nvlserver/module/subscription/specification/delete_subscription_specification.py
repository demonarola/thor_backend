#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_subscription_element_query = """
UPDATE  public.subscription AS sub
 SET active = False, deleted = True
 WHERE sub.id = $1::BIGINT RETURNING *;
 """
