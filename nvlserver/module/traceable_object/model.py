#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB


traceable_object_type = Table(
    'traceable_object_type',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False, default=''),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)


traceable_object = Table(
    'traceable_object',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False, default=''),
    Column('traceable_object_type_id', BigInteger, ForeignKey('traceable_object_type.id'), nullable=False),
    Column('user_id', BigInteger, ForeignKey('user.id')),
    Column('note', String(length=4096), nullable=False, default=''),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('show_on_map', Boolean, default=False),
    Column('collision_avoidance_system', Boolean, default=True),
    Column('action', Boolean, default=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)


traceable_object_brand = Table(
    'traceable_object_brand',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False, default=''),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('traceable_object_type_id', BigInteger, ForeignKey('traceable_object_type.id'), nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)

traceable_object_model = Table(
    'traceable_object_model',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False, default=''),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('traceable_object_brand_id', BigInteger, ForeignKey('traceable_object_brand.id'), nullable=False),
    Column('traceable_object_type_id', BigInteger, ForeignKey('traceable_object_type.id'), nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)
