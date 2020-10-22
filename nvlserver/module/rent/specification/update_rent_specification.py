#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_rent_element_query = """
UPDATE public.user_hw_command AS rnt SET 
   user_id = $2::BIGINT,
    hw_action_id = $3::BIGINT,
    proto_field = $4::VARCHAR,
    field_type = $5::VARCHAR,
    "value" = $6::VARCHAR,
    state = $7::VARCHAR,
    traceable_object_id = $8::BIGINT,
    hw_module_id = $9::BIGINT,
    ack_message = $10::BOOLEAN,
    date_from = $11::TIMESTAMPTZ,
    date_to = $12::TIMESTAMPTZ,
    active = $13::BOOLEAN,
   updated_on = now()
 WHERE rnt.id = $1::BIGINT RETURNING *;
"""
