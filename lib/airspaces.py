import json
import pathlib

import psycopg2
import pygeos
from psycopg2._json import Json
from pygeos import from_geojson

conn = None


def load_airspace_geojson(path: pathlib.Path):
    with open(path) as fp:
        data = json.load(fp)

    airspaces = dict()

    for feature in data['features']:
        prop = feature['properties']
        name = prop['name']
        geometry = feature['geometry']
        polygon = from_geojson(json.dumps(geometry))
        pygeos.prepare(polygon)
        airspaces[name] = dict(polygon=polygon, prop=prop)

    return airspaces


def save_airspace_geojson(airspaces: dict, path: pathlib.Path):
    geojson = {
        'type': 'FeatureCollection',
        'features': [],
    }

    for name, airspace_data in airspaces.items():
        feature = {
            'type': "Feature",
            'properties': airspace_data['prop'],
            'geometry': json.loads(pygeos.to_geojson(airspace_data['polygon'])),
        }
        geojson['features'].append(feature)

    with open(path, 'w') as fp:
        json.dump(geojson, fp, indent=2, ensure_ascii=False)


def buffer_geojson_file(in_file: pathlib.Path, out_file: pathlib.Path, buffer_meters: float):
    with open(in_file) as fp:
        geojson = json.load(fp)
    buffer_geojson_fc(geojson, buffer_meters)
    with open(out_file, 'w') as fp:
        json.dump(geojson, fp, ensure_ascii=False, indent=2)


def buffer_geojson_fc(geojson: dict, buffer_meters: float):
    for feature in geojson['features']:
        feature['geometry'] = buffer_geom_postgis(feature['geometry'], buffer_meters)


def buffer_geom_postgis(geojson: dict, buffer_meters: float):
    global conn

    if conn is None:
        conn = psycopg2.connect("dbname=user")

    query = 'SELECT ST_AsGeoJSON(ST_Buffer(ST_GeomFromGeoJSON(%s)::geography, %s), 6)'

    cur = conn.cursor()
    cur.execute(query, (Json(geojson), buffer_meters))

    records = cur.fetchone()
    cur.close()

    return json.loads(records[0])
