#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import (
    BigInteger, String, Column, Boolean, DateTime, Table, ForeignKey, func, LargeBinary, PrimaryKeyConstraint,
    Numeric
)
from sqlalchemy.dialects.postgresql import JSONB


hw_command = Table(
    'user_hw_command',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('hw_action_id', BigInteger, ForeignKey('hw_action.id'), nullable=True),
    Column('traceable_object_id', BigInteger, ForeignKey('traceable_object.id'), nullable=True),
    Column('hw_module_id', BigInteger, ForeignKey('hw_module.id'), nullable=True),
    Column('proto_field', String(length=255), nullable=False, default=''),
    Column('field_type', String(length=32), nullable=False, default=''),
    Column('proto_field', String(length=255), nullable=False, default=''),
    Column('state', String(length=32), nullable=False, default=''),
    Column('ack_message', Boolean, nullable=False, default=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('date_from', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('date_to', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
