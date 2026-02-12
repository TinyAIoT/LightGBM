#!/bin/bash
# Some basic error checking on input parameters
if [ "$#" -lt 10 ]; then
    echo "ERROR: runSingleExperiment.sh requires 9 arguments but got $#."
    echo "Received args:"
    idx=1
    for a in "$@"; do
        printf " $%d = %q\n" "$idx" "$a"
        idx=$((idx+1))
    done
    echo "Usage: $0 <lgbm> <dataset> <ms> <fp> <tp> <rs> <tree> <depth> <data_dir> <model_dir>"
    exit 2
fi

# Assign input parameters to named variables for clarity
lgbm="$1"
dataset="$2"
ms="$3"
fp="$4"
tp="$5"
rs="$6"
tree="$7"
depth="$8"
data_dir="$9"
model_dir="${10}"

#WORK="/Users/xxx" # set path for local testing.
# Ensure output directory exists
outdir="$model_dir/$dataset${rs}"
mkdir -p "$outdir"
mkdir -p "$WORK/toad/${dataset}/"
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
    train_data="$data_dir/data${rs}"/"${dataset}".train \
    valid_data="$data_dir/data${rs}"/"${dataset}".test \
    max_depth="$depth" \
    num_trees="$tree" \
    tinygbdt_forestsize="$ms" \
    tinygbdt_penalty_split="$tp" \
    tinygbdt_penalty_feature="$fp" \
    output_model="$model_dir/$dataset${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt" \
    > "$model_dir/$dataset${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out"; then
    :  # no-op, do nothing
    # echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth complete"
else
    echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
fi

if python ./hpc/evaluation/evaluate_models.py --filename "$model_dir/$dataset$rs/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth" --resultfile "$WORK/toad/${dataset}/${rs}results.csv"; then :
    rm "$model_dir/$dataset${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out"
    rm "$model_dir/$dataset${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt"
else
    echo "Evaluating model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
fi


