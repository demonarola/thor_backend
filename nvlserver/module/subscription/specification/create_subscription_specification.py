#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'


create_subscription_model_element_query = """
INSERT INTO public.subscription_model AS subm
(description, duration_month, price_per_unit, meta_information, active, deleted)
VALUES
($1, $2, $3, $4, $5, FALSE) RETURNING *;
"""

create_subscription_element_query = """
INSERT INTO public.subscription AS sub
(subscription_uuid, user_id, subscription_model_id, rebate_id, meta_information,
 unit_count, date_from, date_to, active, deleted)
VALUES
($1, $2, $3, $4, $5, $6, $7, $8, $9, FALSE) RETURNING *;
"""
