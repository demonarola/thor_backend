#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2.types import Geometry


hw_module_random_str = Table(
    'hw_module_random_str',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('unique_str', String(length=16), nullable=False, default='')
)

hw_module = Table(
    'hw_module',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(length=255), nullable=False, default=''),
    Column('module_id', String(length=16), nullable=False, unique=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('traceable_object_id', BigInteger, ForeignKey('traceable_object.id'), nullable=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('show_on_map', Boolean, default=False),
    Column('gprs_active', Boolean, default=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)


hw_cas = Table(
    'hw_cas',
    nvl_meta,
    Column('hw_module_id', BigInteger, ForeignKey('hw_module.id'), unique=True, nullable=False),
    Column('position', Geometry('POINT', srid=4326)),
    Column('record_time', DateTime(timezone=True), nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False),
    Column('collision_detect', Boolean, default=True)
)
