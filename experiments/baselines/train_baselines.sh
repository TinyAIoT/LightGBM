#!/bin/bash
models=("lgbm_quant" "ccp" "xgb" "cegb") # quantization is integrated into lgbm training
datasets=("breastcancer" "kr-vs-kp" "covtype" "mushroom" "california_housing" "kin8nm" "wine" "covtype_multi")
trees=(1 2) # 4 8 16 32 64 128 256 512 1024) # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50, 100, 200, 500, 1000]
depths=(3) # 5 7)
alpha=(0.0) # 0.01 0.02 0.05 0.1 0.2)

for model in "${models[@]}"; do
  for dataset in "${datasets[@]}"; do
    for tree in "${trees[@]}"; do
      for depth in "${depths[@]}"; do
        for a in "${alpha[@]}"; do
          python train_baselines.py --model "$model" --dataset "$dataset" --max_trees "$tree" --max_depth "$depth" --alpha "$a" --result_file "results_.csv" --datasets_dir "C:/Users/Jan Stenkamp/Documents/Arbeit/Boosted Trees/code/win/LightGBM/experiments/data/" 
        done
      done
    done
  done
done