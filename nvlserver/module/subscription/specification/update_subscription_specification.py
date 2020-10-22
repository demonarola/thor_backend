#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
update_subscription_element_query = """
UPDATE public.subscription AS sub
SET 
    user_id               = $2,
    subscription_model_id = $3,
    rebate_id             = $4,
    meta_information      = $5,
    unit_count            = $6,
    date_from             = $7,
    date_to               = $8,
    active                = $9
WHERE sub.id = $1::BIGINT
RETURNING *;
 """
