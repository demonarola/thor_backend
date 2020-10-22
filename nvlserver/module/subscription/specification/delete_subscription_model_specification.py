#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
delete_subscription_model_element_query = """
UPDATE public.subscription_model AS subm
 SET active = False, deleted = True
 WHERE subm.id = $1::BIGINT RETURNING *;
 """
