#!/usr/bin/env python3
import pathlib

import click as click

from lib.validate_flight import validate_flight_igc


@click.group()
def cli():
    pass


@cli.command()
@click.argument('igc_file', type=click.Path(exists=True, path_type=pathlib.Path))
def check_one(igc_file):
    validate_flight_igc(igc_file)


@cli.command()
@click.argument('igc_dir', type=click.Path(exists=True, path_type=pathlib.Path))
def check_all(igc_dir):
    for file in sorted(igc_dir.iterdir()):
        if '.igc' in file.name.lower():
            validate_flight_igc(file)


if __name__ == '__main__':
    cli()
