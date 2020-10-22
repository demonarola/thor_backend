# coding: utf-8
import uvloop
import asyncio
from aiologger import Logger
from copy import deepcopy

from web_backend.config import (
    DATABASE,
    EMAIL_HOSTNAME,
    EMAIL_USER,
    EMAIL_PASSWORD,
    SUPPORT_EMAIL
)
from dateutil import tz
from asyncpg import create_pool
import aiosmtplib
from email.mime.text import MIMEText
from asyncio import sleep


pg = None
logger = None
db_conf = deepcopy(DATABASE)
DEBUG = True
conn_uri = '{0}://{1}:{2}@{3}:{4}/{5}'.format(
    'postgres',
    db_conf['user'], db_conf['password'], db_conf['host'],
    db_conf['port'], db_conf['database'])

from_zone = tz.gettz('UTC')


get_email_task_element_query = '''
SELECT sup.id       AS id,
       sup.message  AS email_body,
       sup.subject  AS email_subject,
       sup.email    AS email_sender,
       usr.fullname AS user_full_name
FROM public.support AS sup
         LEFT OUTER JOIN public.user AS usr ON sup.user_id = usr.id
WHERE sup.email_sent IS FALSE
  AND sup.active IS TRUE
ORDER by sup.created_on
LIMIT 1;
'''

update_email_task_element_query = '''
UPDATE public.email_sent AS sup SET
 email_sent = True 
 WHERE sup.id = $1::BIGINT RETURNING *;
'''


async def create_pg_pool():
    """ Create default pg pool"""
    global pg
    pg = await create_pool(conn_uri, min_size=1, max_size=5, server_settings={'application_name': 'mail_sender'})


async def send_email(
        message_text, hostname='smtp.gmail.com',
        port=587, start_tls=True,
        username='', password='') -> bool:
    """ Simple wrapper around smtp lib that monitors if the email is sent.
    On error function returns False

    :param message_text: str
    :param hostname: str
    :param port: int
    :param start_tls: bool
    :param username: str
    :param password: str
    :return: bool
    """

    global logger
    ret_val = False

    try:
        await aiosmtplib.send(
            message_text, hostname=hostname, port=port, start_tls=start_tls,
            username=username, password=password)
        ret_val = True
    except Exception as sm_err:
        await logger.error('update_unsent_error_state erred with: {}'.format(sm_err))

    return ret_val


async def compose_email(
        message_body: str = '', message_subject: str = '',
        sender: str = '', receiver: str = '') -> object:
    """

    :return:
    """
    global logger

    ret_val = False
    try:
        message_text = MIMEText(
            '<html><body>{}</body></html>'.format(message_body),
            'html', 'utf-8'
        )
        message_text["Subject"] = message_subject
        message_text["From"] = sender
        message_text["To"] = receiver

        ret_val = message_text
    except Exception as ce_err:
        await logger.error('compose_email erred with: {}'.format(ce_err))

    return ret_val


async def get_unsent_mail_from_db() -> dict:
    """ Get unsent mail from database. Table is error_email_task and
    We are getting email one by one in datetime asc order with flag email_sent is false.

    :return:
    """

    global pg
    global logger
    ret_val = {}

    try:
        query = get_email_task_element_query
        async with pg.acquire() as connection:
            error_email_task_row = await connection.fetchrow(query)
            if error_email_task_row:
                ret_val = dict(error_email_task_row)
    except Exception as gumfb_err:
        await logger.error('get_unsent_mail_from_db erred with: {}'.format(gumfb_err))
    return ret_val


async def update_email_error_task(error_email_task_id: int = 0) -> dict:
    """ Update email task state.

    :param error_email_task_id: int
    :return:
    """

    global pg
    global logger
    ret_val = {}

    try:
        query = update_email_task_element_query
        async with pg.acquire() as connection:
            error_email_task_row = await connection.fetchrow(query, error_email_task_id)
            if error_email_task_row:
                ret_val = dict(error_email_task_row)
    except Exception as gumfb_err:
        await logger.error('update_email_error_task erred with: {}'.format(gumfb_err))
    return ret_val


async def device_status_checker_service():
    """ Main process used to query all unsent email for errors that happened on the system.

    :return:
    """

    while True:
        print(1)
        # GET LIST OF ALL ERRORS REPORTED BY DEVICES ON  SYSTEM.
        # QUERIED TABLE IS: DEVICE_ERROR_STATE. DATA RETURNED MUST HAVE email_sent = False
        unsent_email_element = await get_unsent_mail_from_db()
        if unsent_email_element:
            msg_composed = await compose_email(
                message_body=unsent_email_element.get('email_body'),
                message_subject='TICKET FROM USER: {}, {}'.format(
                    unsent_email_element.get('user_full_name'),
                    unsent_email_element.get('email_subject')),
                sender=unsent_email_element.get('email_sender'),
                receiver=SUPPORT_EMAIL
            )
            if msg_composed:
                msg_sent = await send_email(
                    message_text=msg_composed, hostname=EMAIL_HOSTNAME,
                    port=587, start_tls=True, username=EMAIL_USER, password=EMAIL_PASSWORD)

                if msg_sent:
                    await update_email_error_task(unsent_email_element.get('id'))

            await sleep(2)


async def run_code_blocks():
    # INIT THE LOGGER
    global logger
    logger = Logger.with_default_handlers(name='nvltracker_email_sender')
    # CREATE THE POOL
    await create_pg_pool()
    # RUN CHECKER LOOP
    await device_status_checker_service()
    await logger.shutdown()


if __name__ == '__main__':

    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_code_blocks())
    loop.close()
