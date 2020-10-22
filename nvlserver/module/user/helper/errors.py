#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
""" Error classes used for database models"""


class UserEmailError(AttributeError):
    def __init__(self, email, *args, **kwargs):
        self.message = "E-mail: {} is already taken!".format(email)
        super().__init__(args, kwargs)
