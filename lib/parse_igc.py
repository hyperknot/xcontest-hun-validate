import json
import subprocess
from pathlib import Path

from config import IGC_TO_JSON_JS


def parse_igc(file_path: Path) -> dict:
    if not file_path.is_file():
        raise ValueError('file missing')

    p = subprocess.run(
        ['node', IGC_TO_JSON_JS, file_path],
        capture_output=True,
        text=True,
        check=True,
    )

    igc_json_str = p.stdout
    igc_json = json.loads(igc_json_str)

    return igc_json
