#!/usr/bin/env python3
import json
import pathlib

import click as click

from lib.parse_igc import parse_igc


@click.group()
def cli():
    pass


@cli.command()
@click.argument('igc_file', type=click.Path(exists=True))
@click.argument('task_json', type=click.Path())
def get_task(igc_file, task_json):
    igc_file_ = pathlib.Path(igc_file)
    task_json_ = pathlib.Path(task_json)

    igc_json = parse_igc(igc_file_)
    print(f'pilot: {igc_json["pilot"]}')

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, ensure_ascii=False, indent=2)

    with open(task_json_, 'w') as fp:
        json.dump(igc_json['task'], fp, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    cli()
