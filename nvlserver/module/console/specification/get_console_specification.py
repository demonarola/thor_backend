#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

get_console_list_query = """
SELECT cls.id              AS id,
       cls.timestamp       AS timestamp,
       cls.user_id         AS user_id,
       usr.fullname        AS user_fullname,
       cls.message         AS message,
       cls.active          AS active,
       cls.deleted         AS deleted
--FROM public.console_view AS cls
FROM  public.console AS cls
         LEFT OUTER JOIN public.user AS usr ON usr.id = cls.user_id
WHERE cls.deleted is FALSE
"""

get_console_list_count_query = """
SELECT count(*) AS console_count
--FROM public.console_view AS cls
FROM  public.console AS cls
         LEFT OUTER JOIN public.user AS usr ON usr.id = cls.user_id
WHERE cls.deleted is FALSE
"""

get_console_element_query = """
SELECT cls.id              AS id,
       cls.timestamp       AS timestamp,
       cls.user_id         AS user_id,
       usr.fullname        AS user_fullname,
       cls.message         AS message,
       cls.active          AS active,
       cls.deleted         AS deleted
--FROM public.console_view AS cls
 FROM  public.console AS cls
         LEFT OUTER JOIN public.user AS usr ON usr.id = cls.user_id
WHERE cls.deleted is FALSE
AND cls.id = $1;
"""

get_console_element_by_name_query = """
SELECT cls.id              AS id,
       cls.timestamp       AS timestamp,
       cls.user_id         AS user_id,
       usr.fullname        AS user_fullname,
       cls.message         AS message,
       cls.active          AS active,
       cls.deleted         AS deleted
--FROM public.console_view AS cls
FROM  public.console AS cls
         LEFT OUTER JOIN public.user AS usr ON usr.id = cls.user_id
WHERE cls.deleted is FALSE
    LIMIT 1;
"""
