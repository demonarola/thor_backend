#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


support = Table(
    'support',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('email', String(length=255), nullable=False, default=''),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('subject', String(length=255), nullable=False, default=''),
    Column('file_name', String(length=255)),
    Column('file_uuid', UUID(as_uuid=True)),
    Column('message', String(length=8192), nullable=False, default=''),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)
