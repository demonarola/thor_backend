#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, DateTime, Table
from sqlalchemy.sql.functions import func


language = Table(
    'language',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(128), nullable=False),
    Column('short_code', String(3), nullable=False),
    Column('default_language', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False)
)
