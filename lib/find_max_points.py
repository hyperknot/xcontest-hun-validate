import numpy as np
import pygeos


def find_max_points(*, fixes: list, airspaces: dict):
    coords = [[f['longitude'], f['latitude']] for f in fixes]
    altitudes = [[f['gpsAltitude']] for f in fixes]
    points = pygeos.points(coords)
    altitudes = np.array(altitudes)

    for name, airspace_data in airspaces.items():
        max_alt = get_max_point_in_geojson(
            points=points, altitudes=altitudes, airspace=airspace_data
        )
        if max_alt is None:
            continue

        prop = airspace_data['prop']
        name = prop['name']
        if name.startswith('SG '):
            limit = prop['upperCeiling']['value'] * 0.3048
        else:
            limit = prop['lowerCeiling']['value'] * 0.3048

        limit_rounded = int(round(limit / 10) * 10)
        diff = max_alt - limit_rounded
        if diff > 100:
            print(
                f'A {name} légtérben {diff} méterrel légtereztél. Max magasságod {max_alt} m volt, megengedett magasság {limit_rounded} m volt.'
            )


def get_max_point_in_geojson(*, points: np.array, altitudes: np.array, airspace: dict):
    polygon = airspace['polygon']
    res = pygeos.contains(polygon, points)

    if not np.any(res):
        return None

    # selected_points = points[res]
    selected_altitudes = altitudes[res]
    return selected_altitudes.max()
