#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
create_request_logger_element_query = """
INSERT INTO public.request_logger AS rlg
(route, request_data, response_data, active, deleted)
VALUES
($1, $2, $3, $4, FALSE) RETURNING *;
"""
