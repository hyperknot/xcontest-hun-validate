#!/usr/bin/env python3
import sys
from pathlib import Path

import click as click

from lib.legter import load_xcontest_airspace
from lib.parse_igc import parse_igc


@click.command()
@click.argument('igc_file', type=click.Path(exists=True))
def cli(igc_file):
    igc_json = parse_igc(Path(igc_file))

    load_xcontest_airspace(Path('legter/r.json'))
    load_xcontest_airspace(Path('legter/sg.json'))
    load_xcontest_airspace(Path('legter/tma.json'))


if __name__ == '__main__':
    sys.exit(cli())
