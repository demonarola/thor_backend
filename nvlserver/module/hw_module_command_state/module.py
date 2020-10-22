#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB


hw_module_command_state = Table(
    'hw_module_command_state',
    nvl_meta,
    Column('state_id', BigInteger, primary_key=True),
    Column('traceable_object_id', BigInteger, ForeignKey('traceable_object.id'), nullable=False),
    Column('hw_module_id', BigInteger, ForeignKey('hw_module.id'), nullable=False),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),

)
