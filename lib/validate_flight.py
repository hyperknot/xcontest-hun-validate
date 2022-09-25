import json
import pathlib
from pathlib import Path

from lib import DATA_DIR
from lib.airspaces import load_airspaces_geojson
from lib.find_max_points import check_all_airspaces
from lib.parse_igc import parse_igc


def validate_flight_igc(igc_file: pathlib.Path):
    print('\n\n\n')
    print(igc_file.name)
    igc_json = parse_igc(Path(igc_file))
    print(f'{igc_json["date"]} {igc_json["pilot"]}')
    print(f'{igc_json["loggerManufacturer"]} - {igc_json["loggerType"]}')

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, ensure_ascii=False, indent=2)

    airspaces = load_airspaces_geojson(DATA_DIR / 'limits.geojson')
    check_all_airspaces(fixes=igc_json['fixes'], airspaces=airspaces)

    igc_json.pop('fixes', None)
    igc_json.pop('task', None)
    igc_json.pop('security', None)
    igc_json.pop('dataRecords', None)
    # pprint(igc_json)
