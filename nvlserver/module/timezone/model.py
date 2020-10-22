#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, DateTime, Table, Interval
from sqlalchemy.sql.functions import func

time_zone = Table(
    'time_zone',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(64)),
    Column('abbrev', String(16)),
    Column('abbrev', String(16)),
    Column('utc_offset', Interval),
    Column('is_dst', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False)
)
