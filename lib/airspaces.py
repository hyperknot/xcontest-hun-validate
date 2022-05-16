import json
import pathlib

import numpy as np
import pygeos
import pyproj
from pygeos import from_geojson
from pyproj import Transformer
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info


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


def buffer_airspaces(*, airspaces: dict, buffer_meter: float):
    utm_proj = pyproj.Proj(proj='utm', zone=34, ellps='WGS84')
    wgs84 = pyproj.Proj(4326)
    transformer = Transformer.from_proj(proj_from=wgs84, proj_to=utm_proj, always_xy=True)
    # res = transformer.transform(47, 18)

    for airspace_data in airspaces.values():
        polygon = airspace_data['polygon']
        coords = pygeos.get_coordinates(polygon)
        new_coords = transformer.transform(coords[:, 0], coords[:, 1])
        result = pygeos.set_coordinates(polygon, np.array(new_coords).T)
        print(result)
