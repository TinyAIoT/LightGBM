#!/bin/bash

randomseeds=(1 2 5 6 7)
datasets=("breastcancer" "krvskp" "mushroom" "wine")
for rs in "${randomseeds[@]}"; do
  for dataset in "${datasets[@]}"; do
    sbatch hpc/zen4_generic.sh "$rs" "$dataset"
  done
done
