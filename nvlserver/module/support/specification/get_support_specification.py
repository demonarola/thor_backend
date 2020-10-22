#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_support_list_query = """
SELECT supp.id                               AS id,
       supp.email                            AS email,
       supp.user_id                          AS user_id,
       coalesce(usr.fullname, '')            AS user_fullname,
       coalesce(supp.subject, '')            AS subject,
       supp.file_name::VARCHAR               AS file_name,
       coalesce(supp.message, '')            AS message,
       supp.active                           AS active,
       supp.deleted                          AS deleted,
       supp.created_on                       AS created_on,
       supp.updated_on                       AS updated_on
FROM public.support AS supp
         LEFT OUTER JOIN public.user AS usr ON usr.id = supp.user_id
WHERE supp.deleted is FALSE
  AND (
      $1::VARCHAR is NULL OR
      supp.email ILIKE $1::VARCHAR || '%' OR
      supp.email ILIKE '%' || $1::VARCHAR || '%' OR
      supp.email ILIKE $1::VARCHAR || '%')
"""

get_support_list_count_query = """
SELECT count(*) AS support_count
FROM public.support AS supp
         LEFT OUTER JOIN public.user AS usr ON usr.id = supp.user_id
WHERE supp.deleted is FALSE
  AND (
      $1::VARCHAR is NULL OR
      supp.email ILIKE $1::VARCHAR || '%' OR
      supp.email ILIKE '%' || $1::VARCHAR || '%' OR
      supp.email ILIKE $1::VARCHAR || '%')
"""

get_support_element_query = """
SELECT supp.id                               AS id,
       supp.email                            AS email,
       supp.user_id                          AS user_id,
       coalesce(usr.fullname, '')            AS user_fullname,
       coalesce(supp.subject, '')            AS subject,
       supp.file_name::VARCHAR               AS file_name,
       coalesce(supp.message, '')            AS message,
       supp.active                           AS active,
       supp.deleted                          AS deleted,
       supp.created_on                       AS created_on,
       supp.updated_on                       AS updated_on
FROM public.support AS supp
         LEFT OUTER JOIN public.user AS usr ON usr.id = supp.user_id
WHERE supp.deleted is FALSE
AND supp.id = $1;
"""

get_support_element_by_name_query = """
SELECT supp.id                               AS id,
       supp.email                            AS email,
       supp.user_id                          AS user_id,
       coalesce(usr.fullname, '')            AS user_name,
       supp.subject                          AS subject,
       supp.file_name::VARCHAR               AS file_name,
       supp.message                          AS message,
       supp.active                           AS active,
       supp.deleted                          AS deleted,
       supp.created_on                       AS created_on,
       supp.updated_on                       AS updated_on
FROM public.support AS supp
         LEFT OUTER JOIN public.user AS usr ON usr.id = supp.user_id
WHERE supp.deleted is FALSE
  AND (
      $1::VARCHAR is NULL OR
      supp.email ILIKE $1::VARCHAR || '%' OR
      supp.email ILIKE '%' || $1::VARCHAR || '%' OR
      supp.email ILIKE $1::VARCHAR || '%')
    LIMIT 1;
"""
