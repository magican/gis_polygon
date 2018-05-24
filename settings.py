#!/usr/bin/env pythonmake_engine
# coding: utf-8

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.getenv('DATABASE_URL', 'postgres://gis_polygon_user:12345678@localhost:5432/gis_polygon_db')

sys.path.append(PROJECT_ROOT)
