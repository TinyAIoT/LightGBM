#!/bin/bash

# [TODO: Set to what you want to test or change to cl params if you want to loop]
lgbm="./lightgbm"
dataset="kin8nm"
ms=64000
fp=0.0
tp=0.0
seed=1
tree=8
depth=8
data_dir="./experiments/data/1"
model_dir="./experiments/local/model/"
result_dir="./experiments/local/result/toad/"
mkdir -p ${result_dir}
mkdir -p $model_dir/$dataset/${seed}
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
    if python ./experiments/python/toad/toadkfold.py --lightgbm $lgbm \
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
        --seed $seed \
        --modeldir $model_dir/$dataset/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth \
        --resdir data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth \
        --outdir ${result_dir}${dataset}; then
        :  # no-op, do nothing
        # echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth complete"
    else
        echo "Training and evaluating model fp=$fp tp=$tp trees=$tree depth=$depth seed=$seed failed / not complete!"
    fi
else
    if "$lgbm" \
        config=train.conf \
        objective=$objective \
        num_class=$num_classes \
        metric=$metric \
        train_data="$data_dir"/"${dataset}".train \
        valid_data="$data_dir"/"${dataset}".val \
        max_depth="$depth" \
        num_trees="$tree" \
        toad_forestsize="$ms" \
        toad_penalty_threshold="$tp" \
        toad_penalty_feature="$fp" \
        output_model="$model_dir/$dataset/${seed}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt" \
        > "$model_dir/$dataset/${seed}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out"; then
        :  # no-op, do nothing
        # echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth complete"
    else
        echo "Training model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
    fi

    if python ./experiments/python/toad/toadevaluate.py --filename "$model_dir/$dataset/$seed/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth" --resultfile "${result_dir}/${dataset}/${seed}/results.csv" --test --val; then :
        rm "$model_dir/$dataset/${seed}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.out"
        rm "$model_dir/$dataset/${seed}/data-$dataset-ms-$ms-fp-$fp-tp-$tp-tree-$tree-depth-$depth.txt"
    else
        echo "Evaluating model fp=$fp tp=$tp trees=$tree depth=$depth failed / not complete!"
    fi
fi

