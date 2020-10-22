#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, DateTime, Table
from sqlalchemy.sql.functions import func


request_logger = Table(
    'request_logger',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('route', String(500)),
    Column('request_data', String(12000)),
    Column('response_data', String(12000)),
    Column('active', Boolean, default=True, nullable=False),
    Column('deleted', Boolean, default=False, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)
