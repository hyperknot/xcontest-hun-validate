import json

import numpy as np
import pygeos
from pygeos import from_geojson


def find_max_points(*, fixes: list, airspaces: dict):
    coords = [[f['longitude'], f['latitude'], f['gpsAltitude']] for f in fixes]
    points = pygeos.points(coords)

    for name, airspace_data in airspaces.items():
        print(name)
        get_max_point_in_geojson(points=points, airspace=airspace_data)


def get_max_point_in_geojson(*, points, airspace: dict):
    polygon = from_geojson(json.dumps(airspace['geometry']))
    pygeos.prepare(polygon)
    res = pygeos.contains(polygon, points)
