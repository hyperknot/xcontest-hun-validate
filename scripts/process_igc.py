#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import click as click

from lib import DATA_DIR
from lib.airspaces import load_airspace_geojson
from lib.find_max_points import find_max_points
from lib.parse_igc import parse_igc


@click.command()
@click.argument('igc_file', type=click.Path(exists=True))
def cli(igc_file):
    igc_json = parse_igc(Path(igc_file))
    airspaces = load_airspace_geojson(DATA_DIR / 'tma.geojson')
    find_max_points(fixes=igc_json['fixes'], airspaces=airspaces)

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, indent=2)


if __name__ == '__main__':
    sys.exit(cli())