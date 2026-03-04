import os
import subprocess
import pandas as pd
# main function:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get datasets for experiments')
    parser.add_argument('--lightgbm', type=str,help='Directory to save datasets')
    parser.add_argument('--config', type=str,help='Directory to save datasets')
    parser.add_argument('--objective', type=str,help='Directory to save datasets')
    parser.add_argument('--num_class', type=int, help='Directory to save datasets')
    parser.add_argument('--metric', type=str,help='Directory to save datasets')
    parser.add_argument('--dataset', type=str,help='Directory to save datasets')
    parser.add_argument('--data_dir', type=str,help='Directory to save datasets')
    parser.add_argument('--max_depth', type=int,help='Directory to save datasets')
    parser.add_argument('--num_trees', type=int,help='Directory to save datasets')
    parser.add_argument('--toad_forestsize', type=int,help='Directory to save datasets')
    parser.add_argument('--toad_penalty_threshold', type=float,help='Directory to save datasets')
    parser.add_argument('--toad_penalty_feature', type=float,help='Directory to save datasets')
    parser.add_argument('--modeldir', type=str,help='Directory to save datasets')
    parser.add_argument('--outdir', type=str,help='Directory to save datasets')
    parser.add_argument('--resdir', type=str, help='Directory to save datasets')
    parser.add_argument('--seed', type=int, help='random seed to process')
    args = parser.parse_args()
    seed = args.seed
    for fold in [0,1,2,3,4]:
        subprocess.call(f"mkdir -p {args.modeldir}-{seed}/", shell=True)
        subprocess.call(f"./{args.lightgbm} config={args.config} \
            objective={args.objective} \
            num_class={args.num_class} \
            metric={args.metric} \
            train_data={args.data_dir}/{fold}/{args.dataset}.train \
            valid_data={args.data_dir}/{fold}/{args.dataset}.val \
            max_depth={args.max_depth} \
            num_trees={args.num_trees} \
            toad_forestsize={args.toad_forestsize} \
            toad_penalty_threshold={args.toad_penalty_threshold} \
            toad_penalty_feature={args.toad_penalty_feature} \
            output_model={args.modeldir}-{seed}/{fold}.txt \
                > {args.modeldir}-{seed}/{fold}.out", shell=True)
        subprocess.call(f"mkdir -p {args.outdir}/{args.resdir}-{seed}", shell=True)
        subprocess.call(f"python ./experiments/python/toad/toadevaluate.py \
         --filename {args.modeldir}-{seed}/{fold} --resultfile {args.outdir}/{args.resdir}-{seed}/kfold.csv --val", shell=True)
    kfoldresults = pd.read_csv(f"{args.outdir}/{args.resdir}-{seed}/kfold.csv")
    meanval = kfoldresults["test_acc"].mean()
    subprocess.call(f"./{args.lightgbm} config={args.config} \
                objective={args.objective} \
                num_class={args.num_class} \
                metric={args.metric} \
                train_data={args.data_dir}/{args.dataset}.train \
                max_depth={args.max_depth} \
                num_trees={args.num_trees} \
                toad_forestsize={args.toad_forestsize} \
                toad_penalty_threshold={args.toad_penalty_threshold} \
                toad_penalty_feature={args.toad_penalty_feature} \
                output_model={args.modeldir}-{seed}/{args.resdir}.txt \
                > {args.modeldir}-{seed}/{args.resdir}.out", shell=True)
    subprocess.call(f"mkdir -p {args.modeldir}-{seed}/{args.resdir}", shell=True)
    subprocess.call(f"python  ./experiments/python/toad/toadevaluate.py \
            --filename {args.modeldir}-{seed}/{args.resdir} --resultfile {args.outdir}/{seed}/results.csv --test --mean={meanval}", shell=True)
    subprocess.call(f"rm -rf {args.modeldir}-{seed}", shell=True)
    subprocess.call(f"rm -rf {args.outdir}/{args.resdir}-{seed}", shell=True)

