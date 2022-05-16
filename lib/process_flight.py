import json
from pathlib import Path

from lib import DATA_DIR
from lib.airspaces import load_airspace_geojson
from lib.find_max_points import find_max_points
from lib.parse_igc import parse_igc


def process_igc(igc_file):
    igc_json = parse_igc(Path(igc_file))
    print(f'pilóta: {igc_json["pilot"]}')

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, ensure_ascii=False, indent=2)

    airspaces_tma = load_airspace_geojson(DATA_DIR / 'tma_diffed_fixed_buffered.geojson')
    airspaces_sg = load_airspace_geojson(DATA_DIR / 'sg_buffered.geojson')
    airspaces = airspaces_tma | airspaces_sg
    find_max_points(fixes=igc_json['fixes'], airspaces=airspaces)
