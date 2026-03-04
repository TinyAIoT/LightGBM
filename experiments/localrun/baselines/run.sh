#!/bin/bash

dataset="kin8nm"
seed=1
tree=4
depth=2
data_dir="./experiments/data/${seed}"
result_dir="./experiments/local/result/baselines/${seed}"
model="lgbm_quant"
alpha=0
mkdir -p ${result_dir}
echo "Running: model=$model dataset=$dataset trees=$tree depth=$depth alpha=$alpha seed=$seed"

if [ "$dataset" = "breastcancer" ] || [ "$dataset" = "kr-vs-kp" ]; then
    python ./experiments/python/baseline/baselinekfold.py \
    --data_dir="${data_dir}/" \
    --model="${model}" \
    --dataset="${dataset}" \
    --max_trees="${tree}" \
    --max_depth="${depth}" \
    --alpha="${alpha}" \
    --result_dir="${result_dir}/" \
    --seed=${seed}
else
    python ./experiments/python/baseline/baselinetrainandeval.py \
    --data_dir="${data_dir}/" \
    --model="${model}" \
    --dataset="${dataset}" \
    --max_trees="${tree}" \
    --max_depth="${depth}" \
    --alpha="${alpha}" \
    --result_dir="${result_dir}/" \
    --val \
    --mean=0
fi
