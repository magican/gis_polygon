#!/usr/bin/env python
# coding: utf-8

import pytest
from falcon import testing
from shapely.geometry import Polygon
from sqlalchemy.orm import sessionmaker

from .app import api
from .controllers import datetime_wkb_handler
from .models import *
from .serializers import GISPolygonSerializer

try:
    import ujson as json
except:
    import simplejson as json
finally:
    import json


@pytest.fixture
def gis_polygon_data():
    """
    Some sample Polygon Geometry.
    :return:
    """
    now = datetime.utcnow()

    # wkb_element = from_shape(Polygon([[-73.08373, 47.76313],
    #                                   [-73.07296, 47.37293],
    #                                   [-73.08303, 47.36239],
    #                                   [-73.08371, 47.36253],
    #                                   [-73.0840, 47.36266],
    #                                   [-73.08373, 47.76313]]), srid=4326)

    p = Polygon([[-73.08373, 47.76313],
                 [-73.07296, 47.37293],
                 [-73.08303, 47.36239],
                 [-73.08371, 47.36253],
                 [-73.0840, 47.36266],
                 [-73.08373, 47.76313]])
    return {
        u"class_id": 1,
        u"name": u"some_test_polygon",
        u"props": 'None',
        u"geom": ''.join(['SRID=4326;', p.to_wkt()]),  # TODO: Grab in Proj from DB or request
        u"_created": now.strftime(format='%Y-%m-%dT%H:%M:%S'),
        u"_updated": now.strftime(format='%Y-%m-%dT%H:%M:%S')
    }


@pytest.fixture
def session():
    """
    Creates DB Session
    :return:
    """
    engine = create_engine(settings.DB_PATH)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


@pytest.fixture
def gis_polygon_instance(gis_polygon_data, session, request):
    """
    Instance of a GIS Polygon Model.
    :param request:
    :param gis_polygon_data:
    :param session:
    :return:
    """

    def finalizer():
        """
        Cleans session after all the test request is done
        :return:
        """
        _cleanup_gis_polygon(session)

    # gis_polygon_obj = GISPolygon(**gis_polygon_data)
    #
    # session.add(gis_polygon_obj)
    # session.commit()

    serializer = GISPolygonSerializer(strict=True)

    # serialize data from request using marshmallow
    serialized = serializer.load(data=gis_polygon_data)

    # get serialized data itself to injest into the database
    gis_polygon_data_serialized = serialized.data

    session.add(gis_polygon_data_serialized)
    session.commit()

    request.addfinalizer(finalizer)

    return gis_polygon_data_serialized


@pytest.fixture
def client():
    """
    Shortcut for a TestClient to simulate requests to a WSGI application.
    :return:
    """
    return testing.TestClient(api)


def _cleanup_gis_polygon(session):
    """
    Cleans up the DB after the Tests session.
    :param session:
    :return:
    """
    session.query(GISPolygon).delete()
    session.commit()


def test_as_dict(session):
    """
    Testing representation of a GeoAlchemy GIS Polygon data model as a dict.
    :return:
    """
    now = datetime.utcnow()
    doc = {
        u"class_id": 1,
        u"name": u"some_test_polygon",
        u"props": None,
        u"geom": None,
        u"_created": now.strftime(format='%Y-%m-%dT%H:%M:%S'),
        u"_updated": now.strftime(format='%Y-%m-%dT%H:%M:%S')
    }

    gis_polygon_obj = GISPolygon(**doc)
    result = gis_polygon_obj.as_dict()
    result.pop('id')
    assert doc == result

    # _cleanup_gis_polygon(session)


def test_create_gis_polygon(client, session):
    """
    Testing Creation, simulating POST request.
    :param client:
    :param session:
    :return:
    """
    doc = gis_polygon_dict = gis_polygon_data()

    body = json.dumps(gis_polygon_dict, default=datetime_wkb_handler)

    headers = {"Content-Type": "application/json"}
    result = client.simulate_post('/gis_polygon/', body=body, headers=headers).json
    # result.pop('id')
    assert result == doc

    _cleanup_gis_polygon(session)


def test_get_gis_polygon(client, session, gis_polygon_instance):
    """
    Testing Reading, simulating GET request.
    :param client:
    :param session:
    :return:
    """
    doc = gis_polygon_instance.as_json_dict()
    result = client.simulate_get('/gis_polygon/%s' % gis_polygon_instance.id).json

    assert result == doc, 'No GIS Polygons data was found'

    _cleanup_gis_polygon(session)


def test_update_gis_polygon(client, gis_polygon_instance):
    body = json.dumps({
        u"class_id": 111,
    })
    doc = {'status': '200 OK'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_put(
        '/gis_polygon/%s' % gis_polygon_instance.id, body=body, headers=headers
    )
    assert result.json == doc, 'GIS Polygon has not been updated'


def test_gis_polygon_list(client, session):
    doc = {"status": "The DB is empty, please fill."}
    _cleanup_gis_polygon(session)
    result = client.simulate_get('/gis_polygon/list')
    assert result.json == doc, 'No GIS Polygons list was found'


def test_delete_gis_polygon(client, gis_polygon_instance):
    doc = {'status': '200 OK'}

    headers = {"Content-Type": "application/json"}
    result = client.simulate_delete(
        '/gis_polygon/%s' % gis_polygon_instance.id, headers=headers
    )
    assert result.json == doc, 'GIS Polygon has not been deleted'


def test_404(client):
    doc = {'status': 'Object does not exist or id is incorrect'}
    headers = {"Content-Type": "application/json"}

    result1 = client.simulate_delete(
        '/gis_polygon/', body=json.dumps({}), headers=headers
    )
    result2 = client.simulate_put(
        '/gis_polygon/-1', body=json.dumps({}), headers=headers
    )
    result3 = client.simulate_get(
        '/gis_polygon/-1', body=json.dumps({}), headers=headers
    )

    assert result1.json == doc, 'Passed a non existent request'
    assert result2.json == doc, 'Passed a non existent request'
    assert result3.json == doc, 'Passed a non existent request'


def test_400_missed(client):
    doc_missed = {'name': ['Missing data for required field.']}

    data_missed = gis_polygon_data()
    data_missed.pop('name')

    body_missed = json.dumps(data_missed, default=datetime_wkb_handler)

    headers = {"Content-Type": "application/json"}
    result_missed = client.simulate_post(
        '/gis_polygon/', body=body_missed, headers=headers
    )

    assert result_missed.json == doc_missed, 'Passed object with missed required fields'


def test_400_wrong(client):
    doc_wrong = {'class_id': ['Not a valid integer.']}

    data_wrong = gis_polygon_data()
    data_wrong['class_id'] = 'asldhnaskjdnkjasn'

    body_wrong = json.dumps(data_wrong, default=datetime_wkb_handler)

    headers = {"Content-Type": "application/json"}
    result_wrong = client.simulate_put(
        '/gis_polygon/', body=body_wrong, headers=headers
    )

    assert result_wrong.json == doc_wrong, 'Passed object with wrong field format'


def test_content_type(client, gis_polygon_data):
    body = json.dumps(gis_polygon_data, default=datetime_wkb_handler)

    doc = {'description': 'application/x-www-form-urlencoded is an unsupported media type.',
           'title': 'Unsupported media type'}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    result = client.simulate_post('/gis_polygon/', body=body, headers=headers)
    assert result.json == doc, 'Passed wrong content-type'
