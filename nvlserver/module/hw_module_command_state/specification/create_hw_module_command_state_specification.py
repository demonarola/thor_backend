#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

''' NOT USABLE CODE STATE CALCULATED ON POSTGRESQL SIDE
create_hw_module_command_state_element_query = """
INSERT INTO public.hw_module_command_state AS hmcs
(hw_module_id, sound_buzzer_state, sound_buzzer_lock, stop_engine_state, stop_engine_lock,
 disable_engine_start_state, disable_engine_start_lock, active, deleted, created_on, updated_on)
VALUES
($1, $2, $3, $4, $5, $6, $7, FALSE, now(), now()) RETURNING *;
"""
'''