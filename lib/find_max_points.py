import numpy as np
import pygeos


def find_max_points(*, fixes: list, airspaces: dict):
    coords = [[f['longitude'], f['latitude']] for f in fixes if f['gpsAltitude']]
    altitudes = [[f['gpsAltitude']] for f in fixes if f['gpsAltitude']]
    points = pygeos.points(coords)
    altitudes = np.array(altitudes)

    flight_ok = True

    print(
        'Szia, tegnap benézted a légteret, mint sokan mások beleértve engem is. Írtam egy scriptet, ami egyszer talán majd autómatikus lesz, de addig is ide beírom amit kidob.'
    )

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
            flight_ok = False
            print(
                f'A {name} légtérben {diff} méterrel légtereztél. Max magasságod {max_alt} m volt, megengedett magasság {limit_rounded} m volt.'
            )

    if flight_ok:
        print('Légtér OK')

    print('\n\n')


def get_max_point_in_geojson(*, points: np.array, altitudes: np.array, airspace: dict):
    polygon = airspace['polygon']
    res = pygeos.contains(polygon, points)

    if not np.any(res):
        return None

    # selected_points = points[res]
    selected_altitudes = altitudes[res]
    return selected_altitudes.max()
