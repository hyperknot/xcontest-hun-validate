import datetime
import json

import requests as requests
from box import Box

from lib import FULL_DAILY_DIR, SG_DAILY_DIR

CHECKED_AIRSPACES = {
    'Dunaújváros DZ': 'SDZLHDV',
}


def get_sg_daily_activations(day_str) -> set:
    SG_DAILY_DIR.mkdir(exist_ok=True)
    cache_file = SG_DAILY_DIR / f'{day_str}.json'

    if cache_file.is_file():
        with open(cache_file) as fp:
            return set(json.load(fp))

    res = requests.get(f'https://legter.hyperknot.com/data/sg/{day_str}.json')
    res.raise_for_status()

    data = res.json()
    with open(cache_file, 'w') as fp:
        json.dump(data, fp)

    return set(data)


def get_full_daily_activations(day_str) -> dict:
    FULL_DAILY_DIR.mkdir(exist_ok=True)
    cache_file = FULL_DAILY_DIR / f'{day_str}.json'

    if cache_file.is_file():
        with open(cache_file) as fp:
            return json.load(fp)

    res = requests.get(f'https://legter.hyperknot.com/data/daily/{day_str}.json')
    res.raise_for_status()

    data = res.json()
    with open(cache_file, 'w') as fp:
        json.dump(data, fp)

    return data


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

        message += f'légtér aktív: {act_from}-{act_to}\n'

        inter = interval_intersection(
            intersection_data['start'], intersection_data['end'], act_from, act_to
        )
        if inter:
            intersect_list.append(inter)
            message += f'légtérben repültél: {inter[0]}-{inter[1]}\n'

    if not intersect_list:
        return Box(found=False)

    return Box(
        found=True,
        list=intersect_list,
        message=message,
    )


def interval_intersection(start1, end1, start2, end2):
    """
    Find the intersection of two intervals.

    :param start1: Starting point of the first interval.
    :param end1: Ending point of the first interval.
    :param start2: Starting point of the second interval.
    :param end2: Ending point of the second interval.
    :return: A tuple representing the intersection of the two intervals or None if there is no intersection.
    """

    if end1 < start2 or end2 < start1:
        return None
    else:
        return max(start1, start2), min(end1, end2)
