#!/usr/bin/env python
# coding: utf-8

"""
GISPolygon CRUD Controller allowing:
    - Create on POST
    - Retrieve on GET
    - Update on PUT
    - Delete on DELETE
"""

from datetime import datetime

try:
    import ujson as json
except:
    import simplejson as json
finally:
    import json

import falcon
from marshmallow import Schema, fields, ValidationError

from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement

from autologging import logged
import logging

from .db_session import DBSession
from .models import GISPolygon
from .serializers import GISPolygonSerializer
from .middleware import cs_transform


def datetime_wkb_handler(x):
    """
    Handles json dumps of datetime/WKBElement objects in str format.
    :param x:
    :return:
    """
    # TODO: One could try using isoformat in Models or write a decorator
    if isinstance(x, datetime):
        return x.isoformat()
    if isinstance(x, WKBElement):
        return to_shape(x).to_wkt()
    return x


class UserSchema(Schema):
    outProj = fields.Str(missing='32644')
    id = fields.Integer(missing=None)


# TODO: ADD Logger
logging.basicConfig(level=logging.INFO, filename="/tmp/gis_polygon.log",
                    format="%(levelname)s:%(name)s:%(funcName)s: %(message)s")

logger = logging.getLogger('gis_polygon')


# TODO: Optimize for speed

class BaseGISPolygonController(object):
    """
    General implementations for GISPolygon CRUD Controller Classes.
    """

    serializer = GISPolygonSerializer(strict=True)

    @staticmethod
    def response_404(resp):
        resp.body = json.dumps({"status": "Object does not exist or id is incorrect"})
        resp.status = falcon.HTTP_404

    @staticmethod
    def response_400(resp, err):
        resp.body = json.dumps(err.messages)
        resp.status = falcon.HTTP_400

    @staticmethod
    def get_gis_polygon(session, gis_polygon_id):
        if gis_polygon_id:
            return session.query(GISPolygon).get(gis_polygon_id)


class GISPolygonCRUD(BaseGISPolygonController):
    """
    Allows:
        Create gis_polygon on POST
        Retrieve detailed info about gis_polygon on GET
        Update gis_polygon info on PUT
        Delete gis_polygon info on DELETE
    Returns data in JSON format.
    """

    def on_get(self, req, resp, gis_polygon_id=None):
        """
        Retrieve detailed info about gis_polygon.
        :param req:
        :param resp:
        :param gis_polygon_id:
        :return:
        """
        session = DBSession()
        gis_polygon = self.get_gis_polygon(session, gis_polygon_id)

        if gis_polygon:
            gis_polygon = gis_polygon.as_json_dict()
        else:
            return self.response_404(resp)

        resp.body = json.dumps(gis_polygon, ensure_ascii=False, default=datetime_wkb_handler)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """
        Create gis_polygon info.
        :param req:
        :param resp:
        :return:
        """

        session = DBSession()
        data = req.media

        # serialize data from request using marshmallow
        try:
            serialized = self.serializer.load(data=data)
        except ValidationError as err:
            return self.response_400(resp, err)

        # get serialized data itself to injest into the database
        gis_polygon = serialized.data

        session.add(gis_polygon)
        session.commit()

        # resp.body = json.dumps(gis_polygon.as_dict(), default=datetime_handler)
        resp.body = json.dumps(self.serializer.dump(gis_polygon).data, default=datetime_wkb_handler)
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, gis_polygon_id=None):
        """
        Update gis_polygon info.
        :param req:
        :param resp:
        :param gis_polygon_id:
        :return:
        """

        session = DBSession()
        data = req.media

        try:
            serialized = self.serializer.load(data=data, partial=True)
        except ValidationError as err:
            return self.response_400(resp, err)

        serialized_data = serialized.data.as_dict()
        gis_polygon = self.get_gis_polygon(session, gis_polygon_id)

        if gis_polygon:
            for name, value in serialized_data.items():
                if value:
                    setattr(gis_polygon, name, value)
        else:
            return self.response_404(resp)

        session.commit()

        resp.body = json.dumps({"status": "200 OK"})
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, gis_polygon_id=None):
        """
        Delete gis_polygon info.
        :param req:
        :param resp:
        :param gis_polygon_id:
        :return:
        """
        session = DBSession()
        gis_polygon = self.get_gis_polygon(session, gis_polygon_id)

        if gis_polygon:
            session.delete(gis_polygon)
            session.commit()
        else:
            return self.response_404(resp)

        resp.body = json.dumps({"status": "200 OK"})
        resp.status = falcon.HTTP_200


class GISPolygonList(BaseGISPolygonController):
    """
    Controller to display the list of all gis_polygons upon GET request.
    """

    def on_get(self, req, resp):
        session = DBSession(autocommit=True)

        gis_polygons = session.query(GISPolygon).all()
        gis_polygons = [gis_polygon.as_dict() for gis_polygon in gis_polygons]

        if not gis_polygons:
            resp.body = json.dumps({"status": "The DB is empty, please fill."})
        else:
            resp.body = json.dumps(gis_polygons, ensure_ascii=False, default=datetime_wkb_handler)

        resp.status = falcon.HTTP_200


@logged(logger)
class GISPolygonTransform(BaseGISPolygonController):
    """
    Controller to display the list of all gis_polygons upon GET request.
    """

    from webargs.falconparser import use_args

    @use_args(UserSchema(strict=True))
    def on_get(self, req, resp, args):
        """
        Retrieve detailed info abP gis_polygon projected between coordinate systems.
        :param req:
        :param resp:
        :param gis_polygon_id:
        :return:
        """

        self.__log.info('{0} {1} {2} {3}'.format(req.method, req.relative_uri, resp.status[:3], args))

        session = DBSession()
        gis_polygon = self.get_gis_polygon(session, args['id'])

        if gis_polygon:
            gis_polygon = gis_polygon.as_json_dict()
        else:
            return self.response_404(resp)

        if args['outProj']:
            gis_polygon['geom'] = cs_transform(gis_polygon['geom'], in_proj='epsg:4326',
                                               out_proj=''.join(['epsg:', args['outProj']]))
        elif args['outProj'] is None:
            resp.status = falcon.HTTP_400
            resp.body = 'No output projection s specified'
        else:
            resp.status = falcon.HTTP_200
            resp.body = 'NOT Hoorrayy!!!!'

        resp.body = json.dumps(gis_polygon, ensure_ascii=False, default=datetime_wkb_handler)
        resp.status = falcon.HTTP_200
