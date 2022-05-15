import json
import pathlib


def load_airspace_geojson(path: pathlib.Path):
    with open(path) as fp:
        data = json.load(fp)

    airspaces = dict()

    for feature in data['features']:
        prop = feature['properties']
        name = prop['name']
        airspaces[name] = dict(geometry=feature['geometry'])

    return airspaces
