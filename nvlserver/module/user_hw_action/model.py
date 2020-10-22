#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'

from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import (
    BigInteger, String, Column, Boolean, DateTime, Table, ForeignKey, func, PrimaryKeyConstraint
)


user_hw_action_location_association = Table(
    'user_hw_action_location_association', nvl_meta,
    Column('user_hw_action_id', BigInteger(), ForeignKey('user_hw_action.id'), nullable=False),
    Column('location_id', BigInteger(), ForeignKey('location.id'), nullable=False),
    PrimaryKeyConstraint('user_hw_action_id', 'location_id')
)


user_hw_action = Table(
    'user_hw_action',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('user_id', BigInteger, ForeignKey('user.id'), nullable=True),
    Column('hw_action_id', BigInteger, ForeignKey('hw_action.id'), nullable=True),
    Column('value', String(length=255), nullable=False),
    Column('active', Boolean, nullable=False),
    Column('deleted', Boolean, nullable=False),
    Column('date_from', DateTime(timezone=True)),
    Column('date_to', DateTime(timezone=True)),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
)
