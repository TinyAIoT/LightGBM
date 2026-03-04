#!/bin/bash

dataset="breastcancer"
ms=64000
fp=0.0
tp=0.0
rs=1
tree=4
depth=2
data_dir="./experiments/data/1"
model_dir="./experiments/local/model/"
result_dir="./experiments/local/result/"
mkdir -p $model_dir/$dataset/${rs}

while read -r model dataset max_trees max_depth alpha seed; do
    [[ -z "${model:-}" ]] && continue
    [[ "${model}" =~ ^# ]] && continue
    echo "Running: model=$model dataset=$dataset trees=$max_trees depth=$max_depth alpha=$alpha seed=$seed"

    if [ "$dataset" = "breastcancer" ] || [ "$dataset" = "kr-vs-kp" ]; then
        python $home/experiments/baselines/kfoldsbaselines.py \
        --data_dir="${data_dir}/${seed}/" \
        --model="${model}" \
        --dataset="${dataset}" \
        --max_trees="${max_trees}" \
        --max_depth="${max_depth}" \
        --alpha="${alpha}" \
        --result_dir="${result_dir}/${seed}" \
        --val \
        --mean=0 \
        --kfold
    else
        python $home/experiments/baselines/train_baselines.py \
        --data_dir="${data_dir}/${seed}/" \
        --model="${model}" \
        --dataset="${dataset}" \
        --max_trees="${max_trees}" \
        --max_depth="${max_depth}" \
        --alpha="${alpha}" \
        --result_dir="${result_dir}/${seed}" \
        --val \
        --mean=0
    fi
done < "$input_file"
