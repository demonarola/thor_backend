#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, func


console = Table(
    'console',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('timestamp', DateTime(timezone=True), nullable=False),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=False),
    Column('message', String(4096), nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
