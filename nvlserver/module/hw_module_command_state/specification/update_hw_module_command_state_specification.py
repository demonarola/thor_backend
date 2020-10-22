#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

''' 
NOT USABLE CODE STATE CALCULATED ON POSTGRESQL SIDE
update_hw_module_command_state_element_query = """
UPDATE  public.hw_module_command_state AS hmcs
 SET hw_module_id = COALESCE($2, hw_module_id),
  sound_buzzer_state = COALESCE($3::BOOLEAN, sound_buzzer_state),
  sound_buzzer_lock = COALESCE($4::BOOLEAN, sound_buzzer_lock),
  stop_engine_state = COALESCE($5::BOOLEAN, stop_engine_state),
  stop_engine_lock = COALESCE($6::BOOLEAN, stop_engine_lock),
  disable_engine_start_state = COALESCE($7::BOOLEAN, disable_engine_start_state),
  disable_engine_start_lock = COALESCE($8::BOOLEAN, disable_engine_start_lock),
  active = $9::BOOLEAN,
  updated_on = now()
 WHERE hmcs.id = $1::BIGINT
  --AND  (
  --    param_1 IS NOT NULL AND param_1 IS DISTINCT FROM column_1 OR
  --    param_2 IS NOT NULL AND param_2 IS DISTINCT FROM column_2 OR
  --   )
  RETURNING *;
 """

update_hw_module_command_state_sound_buzzer_by_hw_module_id_query = """
UPDATE  public.hw_module_command_state AS hmcs
 SET
  sound_buzzer_state = COALESCE($2::BOOLEAN, sound_buzzer_state),
  sound_buzzer_lock = COALESCE($3::BOOLEAN, sound_buzzer_lock),
  updated_on = now()
 WHERE hmcs.hw_module_id = $1::BIGINT RETURNING *;
 """

update_hw_module_command_state_stop_engine_by_hw_module_id_query = """
UPDATE  public.hw_module_command_state AS hmcs
 SET
  stop_engine_state = COALESCE($2::BOOLEAN, stop_engine_state),
  stop_engine_lock = COALESCE($3::BOOLEAN, stop_engine_lock),
  updated_on = now()
 WHERE hmcs.hw_module_id = $1::BIGINT RETURNING *;
 """

update_hw_module_command_state_disable_engine_start_by_hw_module_id_query = """
UPDATE  public.hw_module_command_state AS hmcs
 SET 
  disable_engine_start_state = COALESCE($2::BOOLEAN, disable_engine_start_state),
  disable_engine_start_lock = COALESCE($3::BOOLEAN, disable_engine_start_lock),
  updated_on = now()
 WHERE hmcs.hw_module_id = $1::BIGINT RETURNING *;
 """
'''