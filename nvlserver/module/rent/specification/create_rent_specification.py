#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_rent_element_query = """
INSERT INTO public.user_hw_command
(user_id, hw_action_id, proto_field, field_type, value, state, traceable_object_id, hw_module_id, ack_message,
 date_from, date_to,
 active, deleted, created_on, updated_on)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, FALSE, now(), now())
RETURNING *;
"""
