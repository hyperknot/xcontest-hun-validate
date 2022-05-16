#!/usr/bin/env python3

import click as click

from lib import PROCESS_DIR
from lib.process_flight import process_igc


@click.group()
def cli():
    pass


@cli.command('process-igc')
@click.argument('igc_file', type=click.Path(exists=True))
def process_igc_(igc_file):
    process_igc(igc_file)


@cli.command()
def process_all():
    for file in sorted(PROCESS_DIR.glob('*.igc')):
        print(file.name)
        process_igc(file)


if __name__ == '__main__':
    cli()
