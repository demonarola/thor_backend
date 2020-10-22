#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey, DateTime, Integer, func
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID


rebate = Table(
    'rebate',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('value', Numeric, nullable=False),
    Column('rebate_is_fixed', Boolean, nullable=False, default=True),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)


subscription_model = Table(
    'subscription_model',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('description', String(255), nullable=False),
    Column('duration_month', Integer, nullable=False),
    Column('price_per_unit', Numeric, nullable=False),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)


subscription = Table(
    'subscription',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('subscription_uuid', UUID(as_uuid=True), nullable=False),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=False),
    Column('subscription_model_id', BigInteger, ForeignKey('subscription_model.id'), nullable=False),
    Column('rebate_id', BigInteger, ForeignKey('rebate.id'), nullable=False),
    Column('meta_information', JSONB, default=lambda: {}, nullable=False),
    Column('unit_count', Numeric, nullable=False),
    Column('date_from', DateTime(timezone=True)),
    Column('date_to', DateTime(timezone=True)),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)
