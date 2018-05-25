#!/usr/bin/env python
# coding: utf-8

"""
Base Functionality to serialize/deserialize GISPolygon data using marshmallow simple serializer.
"""

from geoalchemy2.shape import to_shape
from marshmallow import Schema, fields, post_load

from .models import GISPolygon


class GeometrySerializationField(fields.Field):
    """
    Custom SQLAlchemy Geometry serializer/deserializer
    """

    # TODO: Maybe use WKBElement serialization/deserialization
    def _serialize(self, value, attr, obj):
        if value is None:
            return value
        else:
            # if isinstance(value, WKBElement):
            #     return to_shape(value)
            # else:
            #     return None
            return ''.join(['SRID=4326;', to_shape(value).to_wkt()])  # TODO: Grab in Proj from DB or request

    def _deserialize(self, value, attr, data):
        """Deserialize an ISO8601-formatted time to a :class:`datetime.time` object."""
        if not value:  # falsy values are invalid
            self.fail('invalid')

        if isinstance(value, str) and 'POLYGON' in value:
            try:
                # return from_shape(loads(value))
                return value
            except (AttributeError, TypeError, ValueError):
                self.fail('invalid')


class GISPolygonSerializer(Schema):
    """
    Base Class to serialize/deserialize GISPolygon data.
    """

    name = fields.String(required=True)
    props = fields.String(required=False)
    geom = GeometrySerializationField(required=True)
    # geom = fields.Field()
    class_id = fields.Integer()
    _created = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    _updated = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')

    @post_load
    def make_polygons(self, data):
        """
        Make GISPolygon object from dict data.
        :param data:
        :return:
        """
        return GISPolygon(**data)
