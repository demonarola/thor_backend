#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_traceable_object_element_query = """
UPDATE public.traceable_object AS tob
SET name                       = $3,
    traceable_object_type_id   = $4,
    user_id                    = $1,
    note                       = $5,
    meta_information           = $6,
    show_on_map                = $7,
    action                     = $8,
    collision_avoidance_system = $9,
    active                     = $10
WHERE ($1::BIGINT is NULL OR tob.user_id = $1::BIGINT)
  AND tob.id = $2::BIGINT
RETURNING *;
 """
