#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '0.1.0'

update_expired_commands_state_query = """
UPDATE public.user_hw_command AS uhc SET
state = 'expired' 
WHERE uhc.id in (
SELECT id FROM user_hw_command WHERE state='pending' AND date_to <= now() - '10 seconds':: interval
)
"""
