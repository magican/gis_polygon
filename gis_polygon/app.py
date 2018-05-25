#!/usr/bin/env python
# coding: utf-8

import falcon
from falcon_cors import CORS

from .controllers import GISPolygonList, GISPolygonCRUD, GISPolygonTransform

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_origins_list=['*'],
            allow_all_methods=True)

api = application = falcon.API(middleware=[cors.middleware])

gis_polygon_list = GISPolygonList()
gis_polygon_crud = GISPolygonCRUD()
gis_polygon_transform = GISPolygonTransform()

api.add_route('/gis_polygon', gis_polygon_crud)
api.add_route('/gis_polygon/{gis_polygon_id}', gis_polygon_crud)

api.add_route('/gis_polygon/transform', gis_polygon_transform)

api.add_route('/gis_polygon/list/', gis_polygon_list)
