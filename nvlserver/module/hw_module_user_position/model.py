#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, func
from geoalchemy2.types import Geometry
from sqlalchemy.dialects.postgresql import JSONB


hw_module_user_position = Table(
    'hw_module_user_position',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=False),
    Column('traceable_object_id', BigInteger, ForeignKey('traceable_object.id'), nullable=False),
    Column('hw_module_id', BigInteger, ForeignKey('hw_module.id'), nullable=False),
    Column('position', Geometry('POINT', srid=4326)),
    Column('raw_nmea', String(length=128)),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('show_on_map', Boolean, default=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('record_time', DateTime(timezone=False)),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)
