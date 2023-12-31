from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

JS_TOOLS_DIR = PROJECT_DIR / 'js_tools'
IGC_TO_JSON = JS_TOOLS_DIR / 'igc_to_json.js'

DATA_DIR = PROJECT_DIR / 'data'
MAP_FILE = PROJECT_DIR / 'map' / 'map.geojson'

SG_DAILY_DIR = DATA_DIR / 'sg_daily'
FULL_DAILY_DIR = DATA_DIR / 'full_daily'
