# Simple PostGIS/SQLAlchemy/GeoAlchemy2 Polygon CRUD REST API

CRUD REST API for GIS Polygons management.

## INSTALLING

Clone project from repo:
`git clone git@github.com:magican/gis_polygon.git`

Move to project directory:
`cd gis_polygon`

Install virtual environment 3+ python version:
`virtualenv .env`

Activate environment:
`. .env/bin/activate`

Install requirements:
`pip install -r requirements`

Setup database:

`export PYTHONPATH=$PWD:$PYTHONPATH`

`python gis_polygon/models.py`

## TESTING

`pytest --cov=gis_polygon gis_polygon/tests.py -v`

## USING

Run server:
`gunicorn --reload gis_polygon.app`

_NB!: One could use python uWSGI for better efficiency_

Endpoints:

'/gis_polygon' - Allows

    POST method for GIS Polygon creating

'/gis_polygon/{gis_polygon_id}' - Allows:

    GET - detailed gis_polygon information 
    PUT - update gis_polygon object
    DELETE - delete gis_polygon object

'/gis_polygon/list/' - Allows GET for getting gis_polygon list

All endpoints return JSON data type.

Accepted Content-Type - application/json

### USAGE EXAMPLES

    curl -X GET "127.0.0.1:8000/gis_polygon"
    curl -X GET "127.0.0.1:8000/gis_polygon/list"
    curl -X GET "127.0.0.1:8000/gis_polygon/transform?out_proj="
    curl -X GET "127.0.0.1:8000/gis_polygon/transform?id=401&out_proj=32644"
