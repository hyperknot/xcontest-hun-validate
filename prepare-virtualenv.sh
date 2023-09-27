#!/usr/bin/env bash

rm -rf venv *.egg-info __pycache__

python3 -m venv venv
source venv/bin/activate

pip install -U pip wheel
pip install -e .

pip install python-fx

cd js_tools
pnpm i
cd ..

