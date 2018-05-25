#!/usr/bin/env python
# coding: utf-8

"""
Constructs new database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
from .models import Base

engine = create_engine(settings.DB_PATH)
Base.metadata.bind = engine

# TODO: Implement scoped db session for a series of operations to be closed on scope exit.
DBSession = sessionmaker(bind=engine)

# @contextmanager
# def session_scope():
#     DBSession = sessionmaker(bind=db_engine)
#     try:
#         yield DBSession
#         DBSession.commit()
#     except:
#         DBSession.rollback()
#         raise
#     finally:
# DBSession.close()
