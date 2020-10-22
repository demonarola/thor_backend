#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

user_data_by_id_query = '''
SELECT usr.id                                                   AS user_id,
       usr.email                                                AS email,
       usr.password                                             AS password,
       usr.fullname                                             AS fullname,
       usr.locked                                               AS locked,
       usr.active                                               AS active,
       (usr.meta_information->'timezone_id'#>>'{}')::BIGINT     AS timezone_id,
       usr.meta_information->'timezone_name'#>>'{}'             AS timezone_name,
       (usr.meta_information->'map_pool_time'#>>'{}')::BIGINT   AS map_pool_time,
       lng.id                                                   AS language_id,
       lng.name                                                 AS language_name,
       lng.short_code                                           AS language_short_code,
       usr.account_type_id                                      AS account_type_id,
       coalesce(act.name, '')                                   AS account_type_name
FROM public.user AS usr
         LEFT OUTER JOIN public.language AS lng ON lng.id = usr.language_id
         LEFT OUTER JOIN public.account_type as act on act.id = usr.account_type_id
WHERE usr.id = $1::BIGINT
  AND usr.deleted is FALSE
  AND usr.active is TRUE
  AND usr.locked is FALSE
'''

user_login_by_email_query = '''
SELECT usr.id                                                   AS user_id,
       usr.email                                                AS email,
       usr.password                                             AS password,
       usr.fullname                                             AS fullname,
       usr.locked                                               AS locked,
       usr.active                                               AS active,
       (usr.meta_information->'timezone_id'#>>'{}')::BIGINT     AS timezone_id,
       usr.meta_information->'timezone_name'#>>'{}'             AS timezone_name,
       (usr.meta_information->'map_pool_time'#>>'{}')::BIGINT   AS map_pool_time,
       lng.id                                                   AS language_id,
       lng.name                                                 AS language_name,
       lng.short_code                                           AS language_short_code,
       usr.account_type_id                                      AS account_type_id,
       coalesce(act.name, '')                                   AS account_type_name
FROM public.user AS usr
         LEFT OUTER JOIN public.language AS lng ON lng.id = usr.language_id
         LEFT OUTER JOIN public.account_type as act on act.id = usr.account_type_id
WHERE usr.email = $1::VARCHAR
  AND usr.deleted is FALSE
  AND usr.active is TRUE
  AND usr.locked is FALSE
LIMIT 1;
'''

get_user_list_query = '''
SELECT usr.id                                                   AS id,
       usr.email                                                AS email,
       usr.password                                             AS password,
       usr.fullname                                             AS fullname,
       usr.locked                                               AS locked,
       usr.active                                               AS active,
       (usr.meta_information->'timezone_id'#>>'{}')::BIGINT     AS timezone_id,
       usr.meta_information->'timezone_name'#>>'{}'             AS timezone_name,
       (usr.meta_information->'map_pool_time'#>>'{}')::BIGINT   AS map_pool_time,
       lng.id                                                   AS language_id,
       lng.name                                                 AS language_name,
       lng.short_code                                           AS language_short_code,
       usr.account_type_id                                      AS account_type_id,
       coalesce(act.name, '')                                   AS account_type_name
FROM public.user AS usr
         LEFT OUTER JOIN public.language AS lng ON lng.id = usr.language_id
         LEFT OUTER JOIN public.account_type as act on act.id = usr.account_type_id
WHERE usr.deleted is FALSE
 AND (
      $1::VARCHAR is NULL OR
      usr.email ILIKE $1::VARCHAR || '%' OR
      usr.email ILIKE '%' || $1::VARCHAR || '%' OR
      usr.email ILIKE $1::VARCHAR || '%')
      AND (
      $2::VARCHAR is NULL OR
      usr.fullname ILIKE $2::VARCHAR || '%' OR
      usr.fullname ILIKE '%' || $2::VARCHAR || '%' OR
      usr.fullname ILIKE $2::VARCHAR || '%')
'''

get_user_list_by_fullname_query = '''
SELECT usr.id                                                   AS id,
       usr.fullname                                             AS fullname
FROM public.user AS usr
WHERE usr.deleted is FALSE
  AND ($1::VARCHAR is NULL OR usr.fullname ILIKE $1::VARCHAR || '%')
'''

get_user_list_count_query = '''
SELECT count(*) AS city_count
FROM public."user" AS usr
WHERE usr.deleted is FALSE
AND (
      $1::VARCHAR is NULL OR
      usr.email ILIKE $1::VARCHAR || '%' OR
      usr.email ILIKE '%' || $1::VARCHAR || '%' OR
      usr.email ILIKE $1::VARCHAR || '%')
      AND (
      $2::VARCHAR is NULL OR
      usr.fullname ILIKE $2::VARCHAR || '%' OR
      usr.fullname ILIKE '%' || $2::VARCHAR || '%' OR
      usr.fullname ILIKE $2::VARCHAR || '%')
'''

get_user_element_query = '''
SELECT usr.id                                                   AS id,
       usr.email                                                AS email,
       usr.fullname                                             AS fullname,
       usr.password                                             AS password,
       usr.fullname                                             AS fullname,
       usr.locked                                               AS locked,
       usr.active                                               AS active,
       (usr.meta_information->'timezone_id'#>>'{}')::BIGINT     AS timezone_id,
       usr.meta_information->'timezone_name'#>>'{}'             AS timezone_name,
       (usr.meta_information->'map_pool_time'#>>'{}')::BIGINT   AS map_pool_time,
       lng.id                                                   AS language_id,
       lng.name                                                 AS language_name,
       lng.short_code                                           AS language_short_code,
       usr.account_type_id                                      AS account_type_id,
       coalesce(act.name, '')                                   AS account_type_name
FROM public.user AS usr
         LEFT OUTER JOIN public.language AS lng ON lng.id = usr.language_id
         LEFT OUTER JOIN public.account_type as act on act.id = usr.account_type_id
WHERE usr.deleted is FALSE
  AND usr.id = $1;
'''
