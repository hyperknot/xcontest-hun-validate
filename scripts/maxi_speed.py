#!/usr/bin/env python3
import json
import pathlib

from vincenty import vincenty

from lib.parse_igc import parse_igc

IGC_DIR = pathlib.Path('/Users/user/Documents/dev/paragliding/legter_check/samples/t5_20220804')

turnpoint_a41 = {
    "lat": 42.4865417,
    "lon": 21.8957194,
}

turnpoint_a26 = {
    "lat": 42.8713450,
    "lon": 21.8957060,
}

ESS_RADIUS = 2


def main():
    for file in sorted(IGC_DIR.glob('*.igc'))[:5]:
        get_maxi_speed(file)


def get_maxi_speed(file):
    print(file.name)
    igc_json = parse_igc(file)
    print(f'pilot: {igc_json["pilot"]}')

    turnpoint = turnpoint_a26

    with open('debug.json', 'w') as fp:
        json.dump(igc_json, fp, ensure_ascii=False, indent=2)

    fix_1 = get_first_point_in(igc_json['fixes'], turnpoint, ESS_RADIUS + 1.05)
    fix_2 = get_first_point_in(igc_json['fixes'], turnpoint, ESS_RADIUS + 0.05)

    if fix_1 and fix_2:
        time_delta_hours = (fix_2['timestamp'] - fix_1['timestamp']) / 1000 / 60 / 60
        distance_km = vincenty(
            (fix_1['latitude'], fix_1['longitude']), (fix_2['latitude'], fix_2['longitude'])
        )
        speed_kmh = distance_km / time_delta_hours
        return speed_kmh


def get_first_point_in(fixes, turnpoint, radius_km):
    tp = (turnpoint['lat'], turnpoint['lon'])
    for fix in fixes:
        point = (fix['latitude'], fix['longitude'])
        distance = vincenty(point, tp)
        if distance < radius_km:
            return fix


main()
