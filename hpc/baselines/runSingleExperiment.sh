#!/bin/bash
# Some basic error checking on input parameters
if [ "$#" -lt 7 ]; then
    echo "ERROR: runSingleExperiment.sh requires 7 arguments but got $#."
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
data_dir="$1"
model="$2"
dataset="$3"
tree="$4"
depth="$5"
al="$6"
result_dir="$7"

# Ensure output directory exists
mkdir -p "$result_dir"

# Optional debug print (to stderr)
# printf 'DEBUG: lgbm=%q dataset=%q ms=%q fp=%q tp=%q tree=%q depth=%q data_dir=%q model_dir=%q\n' "$lgbm" "$dataset" "$ms" "$fp" "$tp" "$tree" "$depth" "$data_dir" "$model_dir"

python ./experiments/baselines/train_baselines.py \
    --datasets_dir $data_dir \
    --model $model \
    --dataset $dataset \
    --max_trees $tree \
    --max_depth $depth \
    --alpha $al \
    --result_dir $result_dir  \
