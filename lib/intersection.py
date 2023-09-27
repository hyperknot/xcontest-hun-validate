import datetime

import numpy as np
import pygeos
from box import Box

from lib.download_activations import get_full_daily_activations
from lib.lib import interval_intersection

CHECKED_AIRSPACES = {
    'Dunaújváros DZ': 'SDZLHDV',
}


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
            message += f'{airspace_nice_name}\n'

            if limit != 0:
                message += f'légtér magassága: {limit} m\n'

            if activations_inter.found:
                message += activations_inter.message

            message += f'max magasságod: {max_alt} méter\n'

            if limit != 0:
                message += f'légtérsértésed: {diff} méter\n'

            if not activations_inter.found:
                message += f'időpont: {intersection_data["time_at_max_altitude"]} UTC\n'

    abs_max_altitude = get_abs_max_altitude(altitudes=altitudes, times=times)
    if abs_max_altitude["max_altitude"] > 3000:
        valid = False
        message += f'Max magasságod: {abs_max_altitude["max_altitude"]} méter\n'
        message += f'Időpont: {abs_max_altitude["time_at_max_altitude"]} UTC\n'

    if valid:
        message += '    Légtér OK ٩(◕‿◕｡)۶\n'
    else:
        message += '\nHa nem értesz egyet vagy volt engedélyed berepülni, írj az mkksupport@gmail.com-ra.\n'

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


def calculate_activation_intersections(
    day_str: str, airspace_nice_name: str, intersection_data: dict
) -> Box:
    airspace_short_name = CHECKED_AIRSPACES.get(airspace_nice_name)
    if not airspace_short_name:
        return Box(found=False)

    full_activations = get_full_daily_activations(day_str)

    activation_data = full_activations.get(airspace_short_name)
    if not activation_data:
        return Box(found=False)

    intersect_list = []

    message = ''

    for act in activation_data['activations']:
        act_from = datetime.datetime.fromisoformat(act['from']).time()
        act_to = datetime.datetime.fromisoformat(act['to']).time()

        message += f'légtér aktív: {act_from} - {act_to} UTC\n'

        inter = interval_intersection(
            intersection_data['start'], intersection_data['end'], act_from, act_to
        )
        if inter:
            intersect_list.append(inter)
            message += f'légtérben repültél: {inter[0]} - {inter[1]} UTC\n'

    if not intersect_list:
        return Box(found=False)

    return Box(
        found=True,
        list=intersect_list,
        message=message,
    )
