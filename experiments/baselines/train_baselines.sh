#!/bin/bash
models=("lgbm_quant" "ccp" "cegb" "rf") # quantization is integrated into lgbm training
datasets=("breastcancer" "kr-vs-kp" "covtype" "mushroom" "california_housing" "kin8nm" "wine" "covtype_multi")
trees=(1 2 4 8 16 32 64 128 256 512 1024)
depths=(1 2 4 8)
alpha=(0.0 0.5 0.25 0.125 0.0625 0.03125 0.015625 0.0078125)

for model in "${models[@]}"; do
  for dataset in "${datasets[@]}"; do
    for tree in "${trees[@]}"; do
      for depth in "${depths[@]}"; do
        for a in "${alpha[@]}"; do
          python train_baselines.py --model "$model" --dataset "$dataset" --max_trees "$tree" --max_depth "$depth" --alpha "$a" --datasets_dir "../data/"
        done
      done
    done
  done
done