#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

update_user_element_query = """
UPDATE public."user" AS usr SET
 (email, password, fullname, locked, language_id,
  meta_information, account_type_id, active, deleted)
  = ($2, $3, $4, $5, $6, $7, $8, $9, FALSE) WHERE usr.id = $1::BIGINT RETURNING *;
"""

update_user_element_language_query = """
UPDATE public."user" AS usr SET
 language_id = $2::BIGINT
 WHERE usr.id = $1 RETURNING *;
"""

update_user_element_timezone_query = """
UPDATE public."user" AS usr SET
 meta_information = $2
  WHERE usr.id = $1::BIGINT RETURNING *;
"""

update_user_element_map_pool_time_query = """
UPDATE public."user" AS usr SET
 meta_information = $2
  WHERE usr.id = $1::BIGINT RETURNING *;
"""