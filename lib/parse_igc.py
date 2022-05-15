import json
import subprocess
from pathlib import Path

from lib import IGC_TO_JSON


def parse_igc(file_path: Path) -> dict:
    assert file_path.is_file()

    p = subprocess.run(
        ['node', IGC_TO_JSON, file_path],
        capture_output=True,
        text=True,
        check=True,
    )

    igc_json_str = p.stdout
    igc_json = json.loads(igc_json_str)

    return igc_json
