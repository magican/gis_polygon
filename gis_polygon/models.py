#!/usr/bin/env python
# coding: utf-8

"""
GISPolygon Data Model for the CRUD API.
"""

from geoalchemy2.types import Geometry
from sqlalchemy import create_engine, Column, String, TIMESTAMP, JSON, INTEGER
from sqlalchemy.ext.declarative import declarative_base

import settings

Base = declarative_base()


class GISPolygon(Base):
    """
    GeoAlchemy Polygon data model for the CRUD API.
    """
    __tablename__ = 'gis_polygon'

    _created = Column(TIMESTAMP)
    _updated = Column(TIMESTAMP)
    id = Column(INTEGER, primary_key=True)
    class_id = Column(INTEGER)
    name = Column(String)
    props = Column(JSON)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))

    def as_dict(self):
        """
        Represent as Dict.
        :return:
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


if __name__ == "__main__":
    engine = create_engine(settings.DB_PATH)
    Base.metadata.create_all(engine)
