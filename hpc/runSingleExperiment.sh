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
data_dir="$8"
model_dir="$9"

# Ensure output directory exists
outdir="$model_dir/$dataset"
mkdir -p "$outdir"

# check if dataset is one of wine or covtype_multi, than use multiclass mode
if [ "$dataset" = "wine" ] || [ "$dataset" = "covtype_multi" ]; then
    objective=multiclass
    num_classes=7
    metric=multi_logloss
elif [ "$dataset" = "california_housing" ] || [ "$dataset" = "kin8nm" ]; then
    objective=regression
    num_classes=1
    metric=rmse
else
    objective=binary
    num_classes=1
    metric=auc
fi

# Optional debug print (to stderr)
# printf 'DEBUG: lgbm=%q dataset=%q ms=%q fp=%q tp=%q tree=%q depth=%q data_dir=%q model_dir=%q\n' "$lgbm" "$dataset" "$ms" "$fp" "$tp" "$tree" "$depth" "$data_dir" "$model_dir"

if "$lgbm" \
    config=train.conf \
    objective=$objective \
    num_class=$num_classes \
    metric=$metric \
    train_data=$data_dir/${dataset}.train \
    valid_data=$data_dir/${dataset}.test \
    max_depth=$depth \
    num_trees=$tree \
    tinygbdt_forestsize=$ms \
    tinygbdt_penalty_split=$tp \
    tinygbdt_penalty_feature=$fp \
    output_model=$model_dir/$dataset/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt \
    > $model_dir/$dataset/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out; then
    :  # no-op, do nothing
    # echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth complete"
else
    echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
fi
