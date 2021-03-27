import json
from pathlib import Path


def load_xcontest_airspace(file: Path):
    assert file.is_file()

    with open(file) as infile:
        data = json.load(infile)

    airspaces = data['airspaces']

    for airspace in airspaces:
        name = airspace['airname']

        airlower = airspace['airlower']
        airupper = airspace['airupper']

        lower_ft = airlower['height']
        upper_ft = airupper['height']

        lower_m = lower_ft * 0.3048
        upper_m = upper_ft * 0.3048

        if airlower['type'] == 'AGL':
            if airlower['height'] == 0:
                lower_m = 0
            if name == 'Košice TMA 2':
                lower_m = 1194

        upper_round = round_to_10(upper_m)
        lower_round = round_to_10(lower_m)

        print(name, lower_round, upper_round)


def round_to_10(value):
    return round(value / 10) * 10
