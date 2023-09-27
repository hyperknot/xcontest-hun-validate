import datetime

import numpy as np
import pygeos
from box import Box

from lib.activations import calculate_activation_intersections


def check_all_airspaces(
    *,
    fixes: list,
    airspaces: dict,
    sg_activations: set,
    day_str: str,
) -> Box:
    fixes_with_altitude = [f for f in fixes if f['gpsAltitude']]

    coords = [[f['longitude'], f['latitude']] for f in fixes_with_altitude]
    altitudes = np.array([[f['gpsAltitude']] for f in fixes_with_altitude])
    times = np.array([[f['time']] for f in fixes_with_altitude])
    points = pygeos.points(coords)

    valid = True

    message = ''

    for airspace_nice_name, airspace_data in airspaces.items():
        intersection_data = get_airspace_intersection(
            points=points, altitudes=altitudes, times=times, airspace=airspace_data
        )
        if not intersection_data['includes']:
            continue

        prop = airspace_data['prop']
        assert airspace_nice_name == prop['name']

        limit = prop['limit']
        if airspace_nice_name.replace(' ', '') in sg_activations:
            limit = prop['limit_active']

        activations_inter = calculate_activation_intersections(
            day_str, airspace_nice_name, intersection_data
        )
        if activations_inter.found:
            limit = prop['limit_active']

        limit = int(limit)

        max_alt = intersection_data['max_altitude']
        diff = max_alt - limit
        if limit == 0 or diff > 100:
            valid = False
            if limit != 0:
                message += f'{airspace_nice_name} magassága: {limit} m\n'
            message += activations_inter.message
            message += f'max magasságod: {max_alt} méter\n'
            if limit != 0:
                message += f'légtérsértésed: {diff} méter\n'
            message += f'időpont: {intersection_data["time_at_max_altitude"]} UTC\n'

    abs_max_altitude = get_abs_max_altitude(altitudes=altitudes, times=times)
    if abs_max_altitude["max_altitude"] > 3000:
        valid = False
        message += f'Max magasságod: {abs_max_altitude["max_altitude"]} méter\n'
        message += f'Időpont: {abs_max_altitude["time_at_max_altitude"]} UTC\n'

    if valid:
        message += '    Légtér OK ٩(◕‿◕｡)۶\n'

    return Box(valid=valid, message=message)


def get_airspace_intersection(
    *, points: np.array, altitudes: np.array, times: np.array, airspace: dict
) -> dict:
    polygon = airspace['polygon']
    res = pygeos.contains(polygon, points)

    if not np.any(res):
        return dict(includes=False)

    selected_altitudes = altitudes[res]
    selected_times = times[res]

    max_altitude = selected_altitudes.max()
    max_altitude_index = selected_altitudes.argmax()

    start = datetime.time.fromisoformat(selected_times[0][0])
    end = datetime.time.fromisoformat(selected_times[-1][0])

    time_at_max_altitude = selected_times[max_altitude_index][0]
    return dict(
        includes=True,
        max_altitude=max_altitude,
        time_at_max_altitude=time_at_max_altitude,
        start=start,
        end=end,
    )


def get_abs_max_altitude(*, altitudes: np.array, times: np.array):
    max_altitude = altitudes.max()
    max_altitude_index = altitudes.argmax()

    time_at_max_altitude = times[max_altitude_index][0]
    return dict(max_altitude=max_altitude, time_at_max_altitude=time_at_max_altitude)
