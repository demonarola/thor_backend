#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from operator import itemgetter

__all__ = [
    # SERVICES WORKING ON HW MODULE TABLE
    'sub_dict'
]


def sub_dict(d, ks):
    vals = []
    if len(ks) >= 1:
        vals = itemgetter(*ks)(d)
        if len(ks) == 1:
            vals = [vals]
    return dict(zip(ks, vals))
