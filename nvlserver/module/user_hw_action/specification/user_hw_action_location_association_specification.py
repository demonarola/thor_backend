#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'


get_location_id_list_for_user_hw_action_query = """
SELECT location_id
FROM public.user_hw_action_location_association AS uhala
LEFT OUTER JOIN public.user_hw_action AS uha ON uha.id = uhala.user_hw_action_id
WHERE uha.hw_action_id = $1:INT;
"""

get_location_list_for_user_hw_action_query = """
SELECT 
       l.id                 AS id,
       l.name               AS name,
       l.location_type_id   AS location_type_id,
       lt.name              AS location_type_name,
       l.user_id            AS user_id,
       l.show_on_map        AS show_on_map,
       l.active             AS active
FROM public.user_hw_action_location_association AS uhala
         LEFT OUTER JOIN public.location l on uhala.location_id = l.id
         LEFT OUTER JOIN public.location_type lt on lt.id = l.location_type_id
         LEFT OUTER JOIN public.user_hw_action AS uha ON uha.id = uhala.user_hw_action_id
WHERE uha.hw_action_id = $1::INT;
"""

get_user_hw_action_id_list_for_location_query = """
SELECT uha.hw_action_id
FROM public.user_hw_action_location_association AS uhala
LEFT OUTER JOIN public.user_hw_action AS uha ON uha.id = uhala.user_hw_action_id
WHERE uhala.location_id = $1::INT;
"""


get_attached_user_hw_action_list_for_location_query = """
SELECT DISTINCT uhwa.id                   AS id,
                ha.name                   AS name,
                coalesce(ha.meta_information ->> 'action_type', '')       AS action_type,
                uhwa.hw_action_id         AS hw_action_id,
                ha.min_value              AS min_value,
                ha.max_value              AS max_value,
                uhwa.value                AS value,
                uhwa.active               AS active,
                uhwa.deleted              AS deleted
FROM public.user_hw_action AS uhwa
LEFT OUTER JOIN public.hw_action AS ha ON ha.id = uhwa.hw_action_id
WHERE uhwa.id IN
      (SELECT uhala.user_hw_action_id
       FROM public.user_hw_action_location_association AS uhala
       WHERE uhala.location_id = $2::BIGINT)
AND ($1::BIGINT IS NULL OR uhwa.user_id = $1::BIGINT)
"""

get_unattached_user_hw_action_list_for_location_query = """
SELECT DISTINCT uhwa.id                   AS id,
                uhwa.name                 AS name,
                uhwa.active               AS active,
                uhwa.deleted              AS deleted,
                uhwa.created_on           AS created_on,
                uhwa.updated_on           AS updated_on
FROM public.user_hw_action AS uhwa
WHERE uhwa.id NOT IN
      (SELECT uha.hw_action_id
       FROM public.user_hw_action_location_association AS uhala
       LEFT OUTER JOIN public.user_hw_action AS uha ON uha.id = uhala.user_hw_action_id
       WHERE location_id = $1::INT);
"""

get_unattached_user_hw_action_list_count_for_location_query = """
SELECT count(DISTINCT uhwa.id)
FROM public.user_hw_action AS uhwa
WHERE uhwa.id NOT IN
      (SELECT hw_action_id
       FROM public.user_hw_action_location_association
       WHERE location_id = $1::INT)
"""

get_attached_user_hw_action_list_count_for_location_query = """
SELECT count(DISTINCT uhwa.id)
FROM public.user_hw_action AS uhwa
WHERE uhwa.id IN
      (SELECT hw_action_id
       FROM public.user_hw_action_location_association
       WHERE location_id = $1::INT)
"""

get_attached_hw_action_id_list_for_location_query = """
SELECT user_hw_action_id
       FROM public.user_hw_action_location_association
       WHERE location_id = $1::INT 
"""

get_unattached_hw_action_id_list_for_location_query = """
SELECT DISTINCT uhwa.id AS id
FROM public.user_hw_action AS uhwa
WHERE uhwa.id NOT IN
      (SELECT user_hw_action_id
       FROM public.user_hw_action_location_association
       WHERE location_id = $1::INT)
"""


get_user_hw_action_location_element_query = """
SELECT 
    uhala.user_hw_action_id     AS user_hw_action_id,
    uhala.location_id           AS location_id
FROM public.user_hw_action_location_association AS uhala
 WHERE uhala.user_hw_action_id = $1::BIGINT AND uhala.location_id = $2::BIGINT
"""

create_user_hw_action_location_element_query = """
INSERT INTO public.user_hw_action_location_association AS uhala
    (user_hw_action_id, location_id)
VALUES ($1, $2)
RETURNING *;
"""

delete_user_hw_action_location_element_query = """
DELETE
FROM public.user_hw_action_location_association AS uhala
WHERE ($1::INT = 0 OR uhala.user_hw_action_id = $1::INT)
  AND uhala.location_id = $2::INT
RETURNING TRUE;
"""


delete_attached_user_hw_action_list_for_location_query = """
DELETE FROM public.user_hw_action AS uhwa
WHERE uhwa.id = any($1)
RETURNING TRUE;
"""