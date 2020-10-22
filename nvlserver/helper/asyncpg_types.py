#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = '1.0.1'
from typing import Any

import shapely.geometry
import shapely.wkb
from shapely.geometry.base import BaseGeometry
from shapely import geos
from shapely.geometry import mapping

__all__ = [
    # SERVICES WORKING ON HW MODULE TABLE
    'encode_geometry', 'decode_geometry'
]


def encode_geometry(
        geometry: Any) -> bytes:
    if not hasattr(geometry, '__geo_interface__'):
        raise TypeError(f'{geometry} does not conform to geo interface')
    shape = shapely.geometry.asShape(geometry)
    # print('encode_geometry: {}'.format(shape))
    geos.lgeos.GEOSSetSRID(shape._geom, 4326)
    return shapely.wkb.dumps(shape, include_srid=True)


def decode_geometry(
        wkb: bytes) -> BaseGeometry:
    # print('decode_geometry: {}'.format(shapely.wkb.loads(wkb)))
    return mapping(shapely.wkb.loads(wkb))
