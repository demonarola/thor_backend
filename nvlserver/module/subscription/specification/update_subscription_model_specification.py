#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
update_subscription_model_element_query = """
UPDATE public.subscription_model AS subm
SET description      = $2,
    duration_month   = $3,
    price_per_unit   = $4,
    meta_information = $5,
    active           = $6
WHERE subm.id = $1::BIGINT
RETURNING *;
 """
