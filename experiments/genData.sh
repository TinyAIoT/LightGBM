#!/bin/bash

#cd ..
#python3 -m venv path/to/venv
#source path/to/venv/bin/activate
cd python || exit

for dataset in "/mushroom" "/kr-vs-kp" "/kin8nm" "/Breastcancer"; do
  python3 evaluate_models.py ${dataset}
done

cd ..
