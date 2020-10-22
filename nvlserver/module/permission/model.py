#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__license__ = ''
__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy.sql.functions import func
from sqlalchemy import (
    ForeignKey,
    DateTime, BigInteger,
    Boolean,  Column, String, Table, PrimaryKeyConstraint
)

account_type_permission_association = Table(
    'account_type_permission_association', nvl_meta,
    Column('account_type_id', BigInteger(), ForeignKey('account_type.id'),  nullable=False),
    Column('permission_id', BigInteger(), ForeignKey('permission.id'), nullable=False),
    PrimaryKeyConstraint('account_type_id', 'permission_id')
)

user_permission_association = Table(
    'user_permission_association', nvl_meta,
    Column('user_id', BigInteger(), ForeignKey('user.id'), nullable=False),
    Column('permission_id', BigInteger(), ForeignKey('permission.id'), nullable=False),
    PrimaryKeyConstraint('user_id', 'permission_id')
)

permission = Table(
    'permission',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('module', String(32)),
    Column('action', String(64)),
    Column('active', Boolean, default=True, nullable=False),
    Column('deleted', Boolean, default=False, nullable=False),
    Column('created_on', DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column('updated_on', DateTime(timezone=True),
           server_default=func.now(), onupdate=func.now(), nullable=False)
)
