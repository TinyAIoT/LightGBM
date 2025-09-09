#!/bin/bash
# set -euo pipefail
chunkfile="$1"
data_dir="$2"
result_dir="$3"

while IFS=' ' read -r model dataset tree depth al; do
    ./baslines/runSingleExperiment.sh "$data_dir" "$model" "$dataset" "$tree" "$depth" "$al" "$result_dir" 
done < "$chunkfile"