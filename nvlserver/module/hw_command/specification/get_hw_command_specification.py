#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_hw_command_list_query = """
SELECT uhc.id                                           AS id,
       usr.id                                           AS user_id,
       usr.fullname                                     AS user_fullname,
       ha.id                                            AS action_id,
       ha.name                                          AS action_name,
       (ha.meta_information ->> 'action_type')          AS action_type,
       uhc.hw_module_id                                 AS hw_module_id,
       uhc.traceable_object_id                          AS traceable_object_id,
       uhc.active                                       AS active,
       uhc.state                                        AS state,
       uhc.value                                        AS value,
       ha.min_value                                     AS min_value,
       ha.max_value                                     AS max_value,
       to_char(uhc.date_from, 'DD Mon YYYY HH24:MI:SS') AS date_from,
       to_char(uhc.date_to, 'DD Mon YYYY HH24:MI:SS')   AS date_to,
       uhc.active                                       AS active,
       uhc.deleted                                      AS deleted
FROM public.user_hw_command AS uhc
         LEFT OUTER JOIN public.user AS usr ON uhc.user_id = usr.id
         LEFT OUTER JOIN public.hw_action AS ha on ha.id = uhc.hw_action_id
WHERE uhc.deleted IS FALSE
  AND ($1::BIGINT = 0 OR usr.id = $1::BIGINT)
  AND (
        $2::VARCHAR is NULL OR
        ha.name ILIKE $2::VARCHAR || '%' OR
        ha.name ILIKE '%' || $2::VARCHAR || '%' OR
        ha.name ILIKE $2::VARCHAR || '%')
  AND (
        $3::VARCHAR is NULL OR
        (ha.meta_information ->> 'action_type')::VARCHAR ILIKE $3::VARCHAR || '%' OR
        (ha.meta_information ->> 'action_type')::VARCHAR ILIKE '%' || $3::VARCHAR || '%' OR
        (ha.meta_information ->> 'action_type')::VARCHAR ILIKE $3::VARCHAR || '%'
    )
  AND (
        $4::VARCHAR IS NULL OR
        uhc.state::VARCHAR ILIKE $4::VARCHAR || '%' OR
        uhc.state::VARCHAR ILIKE '%' || $4::VARCHAR || '%' OR
        uhc.state::VARCHAR ILIKE $4::VARCHAR || '%'
    )
"""

get_hw_command_list_count_query = """
SELECT count(*) AS user_hw_command_count
FROM public.user_hw_command AS uhc
         LEFT OUTER JOIN public.user AS usr ON uhc.user_id = usr.id
         LEFT OUTER JOIN public.hw_action AS ha on ha.id = uhc.hw_action_id
WHERE uhc.deleted IS FALSE
 AND ($1::BIGINT = 0 OR usr.id = $1::BIGINT)
  AND (
        $2::VARCHAR is NULL OR
        ha.name ILIKE $2::VARCHAR || '%' OR
        ha.name ILIKE '%' || $2::VARCHAR || '%' OR
        ha.name ILIKE $2::VARCHAR || '%')
  AND (
        $3::VARCHAR is NULL OR
        (ha.meta_information ->> 'action_type')::VARCHAR ILIKE $3::VARCHAR || '%' OR
        (ha.meta_information ->> 'action_type')::VARCHAR ILIKE '%' || $3::VARCHAR || '%' OR
        (ha.meta_information ->> 'action_type')::VARCHAR ILIKE $3::VARCHAR || '%'
    )
  AND (
        $4::VARCHAR IS NULL OR
        uhc.state::VARCHAR ILIKE $4::VARCHAR || '%' OR
        uhc.state::VARCHAR ILIKE '%' || $4::VARCHAR || '%' OR
        uhc.state::VARCHAR ILIKE $4::VARCHAR || '%'
    )
"""

get_hw_command_state_by_hw_module_id_query = """
    SELECT (hmcs.meta_information->'action_list')::json AS action_list
     FROM 
     public.hw_module_command_state AS hmcs WHERE hmcs.traceable_object_id = $1
"""