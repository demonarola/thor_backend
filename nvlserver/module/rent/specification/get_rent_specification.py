#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_rent_list_query = """
SELECT rnt.id                                                                     AS id,
       usr.id                                                                     AS user_id,
       usr.fullname                                                               AS user_fullname,
       ha.id                                                                      AS hw_action_id,
       ha.name                                                                    AS hw_action_name,
       (ha.meta_information ->> 'action_type')                                    AS hw_action_type,
       rnt.hw_module_id                                                           AS hw_module_id,
       rnt.traceable_object_id                                                    AS traceable_object_id,
       rnt.active                                                                 AS active,
       rnt.state                                                                  AS state,
       rnt.value                                                                  AS value,
       coalesce(to_char(min(rnt.date_from), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), NULL) AS date_from,
       coalesce(to_char(min(rnt.date_to), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), NULL)   AS date_to,
       rnt.active                                                                 AS active,
       rnt.deleted                                                                AS deleted
FROM public.user_hw_command AS rnt
         LEFT OUTER JOIN public.user AS usr ON rnt.user_id = usr.id
         LEFT OUTER JOIN public.hw_action AS ha on ha.id = rnt.hw_action_id
WHERE rnt.deleted IS FALSE
  AND ($1::BIGINT = 0 OR usr.id = $1::BIGINT)
  AND ha.name = 'TIMER'::VARCHAR
  AND (ha.meta_information ->> 'action_type')::VARCHAR = 'timed_service'::VARCHAR
  AND ($2::timestamptz is NULL OR rnt.date_from >= $2::timestamptz)
  AND ($3::timestamptz is NULL OR rnt.date_to <= $3::timestamptz)
group by rnt.id, usr.id, ha.id
"""

get_rent_list_count_query = """
SELECT count(*) AS rent_count
FROM public.user_hw_command AS rnt
         LEFT OUTER JOIN public.user AS usr ON rnt.user_id = usr.id
         LEFT OUTER JOIN public.hw_action AS ha on ha.id = rnt.hw_action_id
WHERE rnt.deleted IS FALSE
  AND ($1::BIGINT = 0 OR usr.id = $1::BIGINT)
  AND ($2::timestamptz is NULL OR rnt.date_from >= $2::timestamptz)
  AND ($3::timestamptz is NULL OR rnt.date_to <= $3::timestamptz)
  AND ha.name = 'TIMER'::VARCHAR
  AND (ha.meta_information ->> 'action_type')::VARCHAR = 'timed_service'::VARCHAR
"""


get_rent_element_query = """
SELECT rnt.id                                                                     AS id,
       usr.id                                                                     AS user_id,
       usr.fullname                                                               AS user_fullname,
       ha.id                                                                      AS hw_action_id,
       ha.name                                                                    AS hw_action_name,
       (ha.meta_information ->> 'action_type')                                    AS hw_action_type,
       rnt.hw_module_id                                                           AS hw_module_id,
       rnt.traceable_object_id                                                    AS traceable_object_id,
       rnt.active                                                                 AS active,
       rnt.state                                                                  AS state,
       rnt.value                                                                  AS value,
       coalesce(to_char(min(rnt.date_from), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), NULL) AS date_from,
       coalesce(to_char(min(rnt.date_to), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), NULL)   AS date_to,
       rnt.active                                                                 AS active,
       rnt.deleted                                                                AS deleted
FROM public.user_hw_command AS rnt
         LEFT OUTER JOIN public.user AS usr ON rnt.user_id = usr.id
         LEFT OUTER JOIN public.hw_action AS ha on ha.id = rnt.hw_action_id
WHERE rnt.deleted IS FALSE
  AND ha.name = 'TIMER'::VARCHAR
  AND (ha.meta_information ->> 'action_type')::VARCHAR = 'timed_service'::VARCHAR
AND rnt.id = $1::BIGINT
group by rnt.id, usr.id, ha.id
"""
