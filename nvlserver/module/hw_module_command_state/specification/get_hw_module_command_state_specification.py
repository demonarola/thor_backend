#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

''' NOT USABLE CODE STATE CALCULATED ON POSTGRESQL SIDE
get_hw_module_command_state_element_query = """
SELECT hmcs.id                         AS id,
       hmcs.hw_module_id               AS hw_module_id,
       hmcs.sound_buzzer_state         AS sound_buzzer_state,
       hmcs.sound_buzzer_lock          AS sound_buzzer_lock,
       hmcs.stop_engine_state          AS stop_engine_state,
       hmcs.stop_engine_lock           AS stop_engine_lock,
       hmcs.disable_engine_start_state AS disable_engine_start_state,
       hmcs.disable_engine_start_lock  AS disable_engine_start_lock,
       hmcs.active                     AS active,
       hmcs.deleted                    AS deleted,
       hmcs.created_on                 AS created_on,
       hmcs.updated_on                 AS updated_on
FROM public.hw_module_command_state AS hmcs
         LEFT OUTER JOIN public.hw_module AS hm ON hm.id = hmcs.hw_module_id
         LEFT OUTER JOIN public.traceable_object AS tob on hm.traceable_object_id = tob.id
WHERE hmcs.deleted is FALSE
AND hmcs.id = $1::BIGINT;
"""


get_hw_module_command_state_element_by_hw_module_id_query = """
SELECT hmcs.id                         AS id,
       hmcs.hw_module_id               AS hw_module_id,
       hmcs.sound_buzzer_state         AS sound_buzzer_state,
       hmcs.sound_buzzer_lock          AS sound_buzzer_lock,
       hmcs.stop_engine_state          AS stop_engine_state,
       hmcs.stop_engine_lock           AS stop_engine_lock,
       hmcs.disable_engine_start_state AS disable_engine_start_state,
       hmcs.disable_engine_start_lock  AS disable_engine_start_lock,
       hmcs.active                     AS active,
       hmcs.deleted                    AS deleted,
       hmcs.created_on                 AS created_on,
       hmcs.updated_on                 AS updated_on
FROM public.hw_module_command_state AS hmcs
         LEFT OUTER JOIN public.hw_module AS hm ON hm.id = hmcs.hw_module_id
WHERE hmcs.deleted IS FALSE
AND hw.deleted IS FALSE
AND hmcs.hw_module_id = $1::BIGINT
"""

get_hw_module_command_state_element_by_traceable_object_id_query = """
SELECT hmcs.id                         AS id,
       hmcs.hw_module_id               AS hw_module_id,
       hmcs.sound_buzzer_state         AS sound_buzzer_state,
       hmcs.sound_buzzer_lock          AS sound_buzzer_lock,
       hmcs.stop_engine_state          AS stop_engine_state,
       hmcs.stop_engine_lock           AS stop_engine_lock,
       hmcs.disable_engine_start_state AS disable_engine_start_state,
       hmcs.disable_engine_start_lock  AS disable_engine_start_lock,
       hmcs.active                     AS active,
       hmcs.deleted                    AS deleted,
       hmcs.created_on                 AS created_on,
       hmcs.updated_on                 AS updated_on
FROM public.hw_module_command_state AS hmcs
         LEFT OUTER JOIN public.hw_module AS hm ON hm.id = hmcs.hw_module_id
         LEFT OUTER JOIN public.traceable_object AS tob on hm.traceable_object_id = tob.id
WHERE hmcs.deleted is FALSE
AND tob.id = $1::BIGINT

'''