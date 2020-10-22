#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from web_backend.nvlserver.module import nvl_meta
from sqlalchemy import BigInteger, String, Column, Boolean, Table, ForeignKey


town = Table(
    'town',
    nvl_meta,
    Column('id', BigInteger, primary_key=True),
    Column('country_id', BigInteger, ForeignKey('country.id'), nullable=False),
    Column('name', String(length=255), nullable=False, default=''),
    Column('active', Boolean, default=True),
    Column('deleted', Boolean, default=False)
)
