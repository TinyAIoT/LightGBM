#!/bin/bash

cd python || exit

for dataset in "/kin8nm" "/california_housing"; do
  python3 evaluate_models.py ${dataset}
done

cd ..

