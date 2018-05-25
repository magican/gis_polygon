#!/usr/bin/env python
# coding: utf-8

"""
Middlware to allow on the fly conversion between two coordinate systems (CSs).
"""

from functools import partial

import pyproj
from shapely import wkt
from shapely.ops import transform


# TODO: Grab in/out Proj from DB or request
# pyproj.Proj(init='epsg:' + str(srid))
# pyproj.Proj(init='epsg:' + str(req_srid)))

def cs_transform(polygon_wkt, in_proj=None, out_proj=None):
    """
    Transform between two coordinate systems defined by the Proj instances.
    :param in_proj:
    :param out_proj:
    :param polygon:
    :return:
    """
    in_proj = 'epsg:4326' if in_proj is None else in_proj
    out_proj = 'epsg:32644' if out_proj is None else out_proj

    polygon = wkt.loads(polygon_wkt)

    in_proj = pyproj.Proj(init=in_proj)
    out_proj = pyproj.Proj(init=out_proj)
    # TODO: Check if polygon is correctly specified
    project_db_to_req = partial(pyproj.transform, in_proj, out_proj)

    # Apply projection transform to Polygon 'pol' and convert to wkt
    return transform(project_db_to_req, polygon).to_wkt()

    # print(pol.area)  # Area in square meters
    # print(pol2.area)


    # from geoalchemy2.shape import to_shape, from_shape
    # wkb_element = from_shape(pol, srid=4326)
    #
    # to_shape(wkb_element)
