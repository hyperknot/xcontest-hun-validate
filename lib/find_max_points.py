import json

import numpy as np
import pygeos
from pygeos import from_geojson


def find_max_points(*, fixes: list, airspaces: dict):
    coords = [[f['longitude'], f['latitude']] for f in fixes]
    altitudes = [[f['gpsAltitude']] for f in fixes]
    points = pygeos.points(coords)
    altitudes = np.array(altitudes)

    for name, airspace_data in airspaces.items():
        max_alt = get_max_point_in_geojson(
            points=points, altitudes=altitudes, airspace=airspace_data
        )
        print(name, max_alt)


def get_max_point_in_geojson(*, points: np.array, altitudes: np.array, airspace: dict):
    polygon = airspace['polygon']
    res = pygeos.contains(polygon, points)

    if not np.any(res):
        return None

    # selected_points = points[res]
    selected_altitudes = altitudes[res]
    return selected_altitudes.max()
