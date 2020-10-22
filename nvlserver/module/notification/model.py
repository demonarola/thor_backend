#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, DateTime, Table, ForeignKey, func


notification = Table(
    'notification',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False),
    Column('description', String(length=500), nullable=False),
    Column('notification_type_id', BigInteger, ForeignKey('notification_type.id'), nullable=True),
    Column('read', Boolean, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
