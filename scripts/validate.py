#!/usr/bin/env python3
import pathlib

import click as click

from lib import PROCESS_ALL_DIR
from lib.validate_flight import validate_flight_igc


@click.group()
def cli():
    pass


@cli.command()
@click.argument('igc_file', type=click.Path(exists=True))
def check_igc(igc_file):
    validate_flight_igc(pathlib.Path(igc_file))


@cli.command()
def check_all():
    for file in sorted(PROCESS_ALL_DIR.iterdir()):
        if '.igc' in file.name.lower():
            validate_flight_igc(file)


if __name__ == '__main__':
    cli()
