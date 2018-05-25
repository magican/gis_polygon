#!/usr/bin/env python
# coding: utf-8

"""

"""

from functools import partial

import pyproj
from shapely.geometry import Polygon
from shapely.ops import transform

# TODO: Grab in/out Proj from DB or request
# pyproj.Proj(init='epsg:' + str(srid))
# pyproj.Proj(init='epsg:' + str(req_srid)))
#  Transform between two coordinate systems defined by the Proj instances
inProj = pyproj.Proj(init='epsg:4326')
outProj = pyproj.Proj(init='epsg:32644')
project_db_to_req = partial(pyproj.transform, inProj, outProj)

# Polygon outline
pol = Polygon(
    [[-73.08373, 47.76313],
     [-73.07296, 47.37293],
     [-73.08303, 47.36239],
     [-73.08371, 47.36253],
     [-73.0840, 47.36266],
     [-73.08373, 47.76313]])

# Apply projection transform to Polygon 'pol'
pol2 = transform(project_db_to_req, pol)

# print(pol.area)  # Area in square meters
# print(pol2.area)


# from geoalchemy2.shape import to_shape, from_shape
# wkb_element = from_shape(pol, srid=4326)
#
# to_shape(wkb_element)
