#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

create_support_element_query = """
INSERT INTO public.support AS supp
(email, user_id, subject, file_uuid, file_name, message, active, deleted)
VALUES
($1, $2, $3, $4, $5, $6, $7, FALSE) RETURNING *;
"""
