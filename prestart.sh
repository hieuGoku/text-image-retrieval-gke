#!/bin/bash

set -e

. /opt/pysetup/.venv/bin/activate

export PYTHONPATH=$PWD

python3 "app/ml/scripts/download_files.py"

exec "$@"
