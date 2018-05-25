#!/usr/bin/env python
# coding: utf-8

import falcon

from .controllers import GISPolygonList, GISPolygonCRUD

api = application = falcon.API()

gis_polygon_list = GISPolygonList()
gis_polygon_crud = GISPolygonCRUD()

api.add_route('/gis_polygon', gis_polygon_crud)
api.add_route('/gis_polygon/{gis_polygon_id}', gis_polygon_crud)
api.add_route('/gis_polygon/list/', gis_polygon_list)
