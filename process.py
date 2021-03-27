#!/usr/bin/env python3
import pathlib
import sys
from pathlib import Path

import click as click

from lib.parse_igc import parse_igc


@click.command()
@click.argument('igc_file', type=click.Path(exists=True))
def cli(igc_file):
    igc_json = parse_igc(Path(igc_file))


if __name__ == '__main__':
    sys.exit(cli())
