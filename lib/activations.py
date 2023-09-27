import datetime
import json

import requests as requests

from lib import FULL_DAILY_DIR, SG_DAILY_DIR, json_fx

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


def check_airspace_activation_by_time(
    day_str: str, airspace_nice_name: str, intersection_data: dict
) -> bool:
    airspace_short_name = CHECKED_AIRSPACES.get(airspace_nice_name)
    if not airspace_short_name:
        return False

    full_activations = get_full_daily_activations(day_str)

    activation_data = full_activations.get(airspace_short_name)
    if not activation_data:
        return False

    intersects = False

    for act in activation_data['activations']:
        act_from = datetime.datetime.fromisoformat(act['from']).time()
        act_to = datetime.datetime.fromisoformat(act['to']).time()

        if intervals_intersect(
            intersection_data['start'], intersection_data['end'], act_from, act_to
        ):
            intersects = True

    return intersects


def intervals_intersect(start1, end1, start2, end2) -> bool:
    return start1 < end2 and start2 < end1
