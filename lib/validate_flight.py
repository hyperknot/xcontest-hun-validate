import json
import pathlib
from pathlib import Path

from box import Box

from lib import MAP_FILE
from lib.download_activations import get_sg_daily_activations
from lib.airspaces import load_airspaces_geojson
from lib.intersection import check_all_airspaces
from lib.parse_igc import parse_igc


def validate_flight_igc(igc_file: pathlib.Path):
    message = ''

    message += igc_file.name + '\n'
    igc_json = parse_igc(Path(igc_file))

    day_str = igc_json['date']

    message += f'{day_str} {igc_json["pilot"]}\n'
    message += f'{igc_json["loggerManufacturer"]} - {igc_json["loggerType"]}\n\n'

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, ensure_ascii=False, indent=2)

    airspaces = load_airspaces_geojson(MAP_FILE)

    sg_activations = get_sg_daily_activations(day_str)

    result = check_all_airspaces(
        fixes=igc_json['fixes'],
        airspaces=airspaces,
        sg_activations=sg_activations,
        day_str=day_str,
    )

    message += result.message

    return Box(valid=result.valid, message=message)
