#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from gis_polygon.models import Base

engine = create_engine(settings.DB_PATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
