#!/bin/bash
# Some basic error checking on input parameters
if [ "$#" -lt 11 ]; then
    echo "ERROR: runSingleExperiment.sh requires 11 arguments but got $#."
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
rs="$6"
tree="$7"
depth="$8"
data_dir="$9"
model_dir="${10}"
result_dir="${11}"

#WORK="/Users/xxx" # set path for local testing.
# Ensure output directory exists
mkdir -p "$result_dir"
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
if [ "$dataset" = "breastcancer" ] || [ "$dataset" = "kr-vs-kp" ]; then
    if python experiments/python/toad/toadkfold.py --lightgbm $lgbm \
        --config train.conf \
        --objective $objective \
        --num_class $num_classes \
        --metric $metric \
        --dataset $dataset \
        --data_dir $data_dir \
        --max_depth $depth \
        --num_trees $tree \
        --toad_forestsize $ms \
        --toad_penalty_threshold $tp \
        --toad_penalty_feature $fp \
        --seed $rs \
        --modeldir $model_dir/$dataset/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth \
        --resdir data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth \
        --outdir $result_dir/$dataset; then
        :  # no-op, do nothing
        echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth complete"
    else
        echo "Training and evaluating model fp=$fp tp=$tp trees=$tree depth=$depth rs=$rs failed / not complete!"
    fi
else
    if "$lgbm" \
        config=train.conf \
        objective=$objective \
        num_class=$num_classes \
        metric=$metric \
        train_data="$data_dir"/"${dataset}".train \
        valid_data="$data_dir"/"${dataset}".test \
        max_depth="$depth" \
        num_trees="$tree" \
        toad_forestsize="$ms" \
        toad_penalty_threshold="$tp" \
        toad_penalty_feature="$fp" \
        output_model="$model_dir/$dataset/${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt" \
        > "$model_dir/$dataset/${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out"; then
        :  # no-op, do nothing
        echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth complete"
    else
        echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
    fi

    if python ./experiments/python/toad/toadevaluate.py --filename "$model_dir/$dataset/$rs/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth" --resultfile "$WORK/toad/${dataset}/${rs}results.csv" --test --val; then :
        rm "$model_dir/$dataset${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out"
        rm "$model_dir/$dataset${rs}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt"
    else
        echo "Evaluating model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
    fi
fi



