#!/usr/bin/env python3
import json

import pygeos

from lib import DATA_DIR
from lib.airspaces import load_airspace_geojson, save_airspace_geojson, buffer_airspaces


def main():
    with open(DATA_DIR / 'sg_dissolved.geojson') as fp:
        sg_dissolved = pygeos.from_geojson(fp.read())
        pygeos.prepare(sg_dissolved)

    # sg_airspaces = load_airspace_geojson(DATA_DIR / 'sg.geojson')
    # for name, airspace_data in sg_airspaces.items():
    #     print(name, airspace_data)

    tma_airspaces = load_airspace_geojson(DATA_DIR / 'tma.geojson')
    for name, airspace_data in tma_airspaces.items():
        polygon = airspace_data['polygon']
        if not pygeos.intersects(sg_dissolved, polygon):
            continue

        airspace_data['polygon'] = pygeos.difference(polygon, sg_dissolved)

    save_airspace_geojson(tma_airspaces, DATA_DIR / 'tma_diffed.geojson')

    # MANUAL mapshaper filter-slivers min-area=1km2

    tma_airspaces = load_airspace_geojson(DATA_DIR / 'tma_diffed_fixed.geojson')
    buffer_airspaces(airspaces=tma_airspaces, buffer_meter=100)


main()
