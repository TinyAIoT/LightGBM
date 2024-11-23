#!/bin/bash

cd ..
python3 -m venv path/to/venv
source path/to/venv/bin/activate
cd experiments/python || exit

for dataset in "/nina-test" ; do
  python3 evaluate_models.py ${dataset}
done