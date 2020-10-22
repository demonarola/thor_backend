#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
""" This module exports the db meta data."""

from sqlalchemy import MetaData
# from sqlalchemy import create_engine
# from web_backend.config import DATABASE


# engine = create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(
#     DATABASE['type'],
#     DATABASE['user'], DATABASE['password'], DATABASE['host'],
#     DATABASE['port'], DATABASE['database'])
#     # pool_size=250, max_overflow=20
# )
# nvl_meta = MetaData(bind=engine)
nvl_meta = MetaData()
