#!/bin/bash
# set -euo pipefail
chunkfile="$1"
lgbm="$2"
ms="$3"
data_dir="$4"
model_dir="$5"
result_dir="$6"

while IFS=' ' read -r dataset tree depth fp tp; do
    ./hpc/runSingleExperiment.sh "$lgbm" "$dataset" "$ms" "$fp" "$tp" "$tree" "$depth" "$data_dir" "$model_dir" "$result_dir"
done < "$chunkfile"
