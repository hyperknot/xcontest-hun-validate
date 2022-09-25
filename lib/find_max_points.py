import numpy as np
import pygeos


def check_all_airspaces(*, fixes: list, airspaces: dict, sg_daily_activations: set):
    fixes_with_altitude = [f for f in fixes if f['gpsAltitude']]

    coords = [[f['longitude'], f['latitude']] for f in fixes_with_altitude]
    altitudes = np.array([[f['gpsAltitude']] for f in fixes_with_altitude])
    times = np.array([[f['time']] for f in fixes_with_altitude])
    points = pygeos.points(coords)

    for name, airspace_data in airspaces.items():
        intersection_data = get_airspace_intersection(
            points=points, altitudes=altitudes, times=times, airspace=airspace_data
        )
        if not intersection_data['includes']:
            continue

        prop = airspace_data['prop']
        name = prop['name']

        limit = prop['limit']
        if name.replace(' ', '') in sg_daily_activations:
            limit = prop['limit_active']

        max_alt = intersection_data['max_altitude']
        diff = max_alt - limit
        if diff > 100:
            print(sg_daily_activations)
            print('________________________')
            print(f'{name} magassága: {limit} m')
            print(f'Emelkedesi magasságod: {max_alt} méter')
            print(f'Légtérsértésed: {diff} méter')
            print(f'Időpont: {intersection_data["time_at_max_altitude"]} UTC')
            print('________________________')


def get_airspace_intersection(
    *, points: np.array, altitudes: np.array, times: np.array, airspace: dict
):
    polygon = airspace['polygon']
    res = pygeos.contains(polygon, points)

    if not np.any(res):
        return dict(includes=False)

    selected_altitudes = altitudes[res]

    max_altitude = selected_altitudes.max()
    max_altitude_index = selected_altitudes.argmax()

    time_at_max_altitude = times[max_altitude_index][0]
    return dict(includes=True, max_altitude=max_altitude, time_at_max_altitude=time_at_max_altitude)
