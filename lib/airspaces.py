import json
import pathlib

import pygeos
from pygeos import from_geojson






def load_airspaces_geojson(path: pathlib.Path):
    with open(path) as fp:
        data = json.load(fp)

    airspaces = dict()

    for feature in sorted(data['features'], key=lambda f: f['properties']['name']):
        prop = feature['properties']
        name = prop['name']
        geometry = feature['geometry']
        polygon = from_geojson(json.dumps(geometry))
        pygeos.prepare(polygon)
        airspaces[name] = dict(polygon=polygon, prop=prop)

    return airspaces


def save_airspaces_geojson(airspaces: dict, path: pathlib.Path):
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
