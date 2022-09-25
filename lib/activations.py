import json

import requests as requests

from lib import SG_DAILY_DIR


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
