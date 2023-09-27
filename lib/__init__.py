from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

JS_TOOLS_DIR = PROJECT_DIR / 'js_tools'
IGC_TO_JSON = JS_TOOLS_DIR / 'igc_to_json.js'

DATA_DIR = PROJECT_DIR / 'data'
IGC_DIR = DATA_DIR / 'igc'

SG_DAILY_DIR = DATA_DIR / 'sg_daily'
FULL_DAILY_DIR = DATA_DIR / 'full_daily'


def json_fx(data):
    from pyfx import PyfxApp

    PyfxApp(data).run()
