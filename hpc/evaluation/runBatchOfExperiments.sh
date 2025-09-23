#!/bin/bash
# set -euo pipefail
chunkfile="$1"
lgbm="$2"
ms="$3"
result_dir="$4"
model_dir="$5"

while IFS=' ' read -r dataset tree depth fp tp; do
    ./hpc/evaluation/runSingleExperiment.sh "$lgbm" "$dataset" "$ms" "$fp" "$tp" "$tree" "$depth" "$result_dir" "$model_dir"
done < "$chunkfile"