#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, DateTime, Table, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB


location_type = Table(
    'location_type',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)


location = Table(
    'location',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False),
    Column('location_type_id', BigInteger, ForeignKey('location_type.id'), nullable=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('show_on_map', Boolean, nullable=False, default=True),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
