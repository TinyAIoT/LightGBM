import os
import subprocess
import pandas as pd
# main function:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get datasets for experiments')
    parser.add_argument('--data_dir', type=str,help='Directory to save datasets')
    parser.add_argument('--model', type=str,help='Directory to save datasets')
    parser.add_argument('--dataset', type=str,help='Directory to save datasets')
    parser.add_argument('--max_depth', type=int,help='Directory to save datasets')
    parser.add_argument('--max_trees', type=int,help='Directory to save datasets')
    parser.add_argument('--alpha', type=float,help='Directory to save datasets')
    parser.add_argument('--result_dir', type=str, help='Directory to save datasets')
    parser.add_argument('--seed', type=int, help='Randomseed')
    args = parser.parse_args()
    seed = args.seed
    for fold in [0,1,2,3,4]:
        subprocess.call(f"mkdir -p {args.data_dir}/{fold}", shell=True)
        subprocess.call(f"mkdir -p {args.result_dir}", shell=True)
        subprocess.call(f"mkdir -p {args.result_dir}/{args.dataset}-{seed}-{args.alpha}-{args.max_depth}-{args.max_trees}-{args.model}/", shell=True)
        subprocess.call(f"python ./experiments/python/baseline/baselinetrainandeval.py \
            --data_dir={args.data_dir}/{fold} \
            --model={args.model} \
            --dataset={args.dataset} \
            --max_trees={args.max_trees} \
            --max_depth={args.max_depth} \
            --alpha={args.alpha} \
            --kfold \
            --val \
            --randomseed={seed} \
            --result_dir={args.result_dir}/{args.dataset}-{seed}-{args.alpha}-{args.max_depth}-{args.max_trees}-{args.model}", shell=True)
    kfoldresults = pd.read_csv(f"{args.result_dir}/{args.dataset}-{seed}-{args.alpha}-{args.max_depth}-{args.max_trees}-{args.model}/results.csv")
    meanval = kfoldresults["val_acc"].mean()
    subprocess.call(f"python ./experiments/python/baseline/baselinetrainandeval.py \
                    --data_dir={args.data_dir} \
                    --model={args.model} \
                    --dataset={args.dataset} \
                    --max_trees={args.max_trees} \
                    --max_depth={args.max_depth} \
                    --alpha={args.alpha} \
                    --result_dir={args.result_dir} \
                    --mean={meanval} \
                    --randomseed={seed} \
                    --kfold", shell=True)
    subprocess.call(f"rm -rf {args.result_dir}/{args.dataset}-{seed}-{args.alpha}-{args.max_depth}-{args.max_trees}-{args.model}/", shell=True)

