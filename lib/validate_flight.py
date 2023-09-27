import json
import pathlib
from pathlib import Path
from pprint import pprint

from lib import DATA_DIR
from lib.activations import get_full_daily_activations, get_sg_daily_activations
from lib.airspaces import load_airspaces_geojson
from lib.intersection import check_all_airspaces
from lib.parse_igc import parse_igc


def validate_flight_igc(igc_file: pathlib.Path):
    print('\n\n\n')
    print(igc_file.name)
    igc_json = parse_igc(Path(igc_file))

    day_str = igc_json['date']

    print(f'{day_str} {igc_json["pilot"]}')
    print(f'{igc_json["loggerManufacturer"]} - {igc_json["loggerType"]}')

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, ensure_ascii=False, indent=2)

    airspaces = load_airspaces_geojson(DATA_DIR / 'limits.geojson')

    sg_activations = get_sg_daily_activations(day_str)

    check_all_airspaces(
        fixes=igc_json['fixes'],
        airspaces=airspaces,
        sg_activations=sg_activations,
        day_str=day_str,
    )
    #
    # igc_json.pop('fixes', None)
    # igc_json.pop('task', None)
    # igc_json.pop('security', None)
    # igc_json.pop('dataRecords', None)
    # pprint(igc_json)
