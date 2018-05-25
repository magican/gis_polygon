#!/usr/bin/env python
# coding: utf-8

"""
GISPolygon Data Model for the CRUD API.
"""

from datetime import datetime

from geoalchemy2.types import Geometry
from sqlalchemy import create_engine, Column, String, TIMESTAMP, JSON, INTEGER
from sqlalchemy.ext.declarative import declarative_base

import settings

Base = declarative_base()


class GISPolygon(Base):
    """
    GeoAlchemy GIS Polygon data model for the CRUD API.
    """
    __tablename__ = 'gis_polygon'

    now = datetime.utcnow()

    _created = Column(TIMESTAMP, nullable=False, default=now.strftime(format='%Y-%m-%dT%H:%M:%S'))
    _updated = Column(TIMESTAMP, nullable=False, default=now.strftime(format='%Y-%m-%dT%H:%M:%S'),
                      onupdate=datetime.utcnow().strftime(format='%Y-%m-%dT%H:%M:%S'))
    id = Column(INTEGER, primary_key=True)
    class_id = Column(INTEGER, default=1)
    name = Column(String)
    props = Column(JSON)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))

    def as_dict(self):
        """
        Represent data model as Dict.
        :return:
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

        # def as_json_dict(self):
        #     return {c.name: serialize(getattr(self, c.name)) for c in self.__table__.columns}


if __name__ == "__main__":
    engine = create_engine(settings.DB_PATH)
    Base.metadata.create_all(engine)
