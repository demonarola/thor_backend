#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import (
    BigInteger, String, Column, Boolean, DateTime, Table, func,
    Numeric
)
from sqlalchemy.dialects.postgresql import JSONB


hw_action = Table(
    'hw_action',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False),
    Column('proto_field', String(length=255), nullable=False),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('min_value', Numeric(), nullable=False),
    Column('max_value', Numeric(), nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
