#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, DateTime, Table, ForeignKey, func
from geoalchemy2.types import Geometry
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import JSONB

nvl_linestring = Table(
    'nvl_linestring',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('geom', Geometry('LINESTRING', srid=4326)),
    Column('label', String(length=255), nullable=False),
    Column('color', String(length=32), nullable=False),
    Column('location_id', BigInteger, ForeignKey('location.id'), nullable=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)

nvl_point = Table(
    'nvl_point',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('geom', Geometry('POINT', srid=4326)),
    Column('label', String(length=255), nullable=False),
    Column('color', String(length=32), nullable=False),
    Column('icon', String(length=32), nullable=False),
    Column('location_id', BigInteger, ForeignKey('location.id'), nullable=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)


nvl_circle = Table(
    'nvl_circle',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('geom', Geometry('POINT', srid=4326)),
    Column('radius', Numeric, nullable=False),
    Column('label', String(length=255), nullable=False),
    Column('color', String(length=32), nullable=False),
    Column('location_id', BigInteger, ForeignKey('location.id'), nullable=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)


nvl_polygon = Table(
    'nvl_polygon',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('geom', Geometry('POLYGON', srid=4326)),
    Column('label', String(length=255), nullable=False),
    Column('color', String(length=32), nullable=False),
    Column('location_id', BigInteger, ForeignKey('location.id'), nullable=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
