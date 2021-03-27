import json
from pathlib import Path

from shapely.geometry.polygon import Polygon

UTM_FOR_HUNGARY = 34


def load_xcontest_airspace(file: Path) -> list:
    assert file.is_file()

    with open(file) as infile:
        data = json.load(infile)

    airspaces = data['airspaces']

    airspace_list = []

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

        geom = Polygon([(y, x) for x, y in airspace['components']])

        data = dict(name=name, upper=upper_round, lower=lower_round, geom=geom)

        airspace_list.append(data)

    return airspace_list


def buffer_100_meter(geom):
    return geom


def round_to_10(value):
    return round(value / 10) * 10
