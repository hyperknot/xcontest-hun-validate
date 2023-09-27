## Validation script for Hungarian XContest

### Install
run `source prepare-virtualenv.sh` or follow the lines inside the file. Needs Python and node.

### Usage

Use `./validate.py`.

#### Human readable
`validate.py check-one example.igc` -> output human message for one IGC file
`validate.py check-all igc_folder` -> output human message for all IGC files in a folder

#### Machine readdable
`validate.py check-json example.igc` -> output JSON message, keys: valid, message

For example:

```
{
  "valid": true,
  "message": "2023-03-21-XCT-DAR-01.igc\n2023-03-21 Example Pilot\nXCTrack - Hisense Hisense A2T 7.1.2\n\n    Légtér OK ٩(◕‿◕｡)۶\n"
}
```

or

```
{
  "valid": false,
  "message": "2023-09-12-XFH-000-01.IGC\n2023-09-12 Example Pilot\nFlyskyhy - Flyskyhy,8.0\n\nBudapest TMA 3\nlégtér magassága: 1070 m\nmax magasságod: 1215 méter\nlégtérsértésed: 145 méter\nidőpont: 12:57:38 UTC\n"
}
```
