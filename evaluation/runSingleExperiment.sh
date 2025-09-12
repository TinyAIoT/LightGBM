#!/bin/bash
# Some basic error checking on input parameters
if [ "$#" -lt 9 ]; then
    echo "ERROR: runSingleExperiment.sh requires 9 arguments but got $#."
    echo "Received args:"
    idx=1
    for a in "$@"; do
        printf " $%d = %q\n" "$idx" "$a"
        idx=$((idx+1))
    done
    echo "Usage: $0 <lgbm> <dataset> <ms> <fp> <tp> <tree> <depth> <data_dir> <model_dir>"
    exit 2
fi

# Assign input parameters to named variables for clarity
lgbm="$1"
dataset="$2"
ms="$3"
fp="$4"
tp="$5"
tree="$6"
depth="$7"
result_dir="$8"
model_dir="$9"

# Ensure output directory exists
outdir="$result_dir/$dataset"
mkdir -p "$outdir"

# Optional debug print (to stderr)
# printf 'DEBUG: lgbm=%q dataset=%q ms=%q fp=%q tp=%q tree=%q depth=%q data_dir=%q model_dir=%q\n' "$lgbm" "$dataset" "$ms" "$fp" "$tp" "$tree" "$depth" "$data_dir" "$model_dir"

python --filename $model_dir/$dataset/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth --result_file $outdir/results.csv