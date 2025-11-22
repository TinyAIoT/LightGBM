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
    parser.add_argument('--tinygbdt_forestsize', type=int,help='Directory to save datasets')
    parser.add_argument('--tinygbdt_penalty_split', type=float,help='Directory to save datasets')
    parser.add_argument('--tinygbdt_penalty_feature', type=float,help='Directory to save datasets')
    parser.add_argument('--output_model', type=str,help='Directory to save datasets')
    parser.add_argument('--modeldir', type=str,help='Directory to save datasets')
    parser.add_argument('--outdir', type=str,help='Directory to save datasets')
    parser.add_argument('--resdir', type=str, help='Directory to save datasets')
    args = parser.parse_args()
    seeds = [3, 4, 10, 11, 12]
    for seed in seeds:
        for fold in [0,1,2,3,4]:
            subprocess.call(f"mkdir -p {args.output_model}/{seed}/", shell=True)
            subprocess.call(f"mkdir -p {args.modeldir}/{seed}/", shell=True)
            subprocess.call(f"./{args.lightgbm} config={args.config} \
                objective={args.objective} \
                num_class={args.num_class} \
                metric={args.metric} \
                train_data={args.data_dir}/{seed}/{fold}/{args.dataset}.train \
                valid_data={args.data_dir}/{seed}/{fold}/{args.dataset}.test \
                max_depth={args.max_depth} \
                num_trees={args.num_trees} \
                tinygbdt_forestsize={args.tinygbdt_forestsize} \
                tinygbdt_penalty_split={args.tinygbdt_penalty_split} \
                tinygbdt_penalty_feature={args.tinygbdt_penalty_feature} \
                output_model={args.output_model}/{seed}/{fold}.txt \
                    > {args.modeldir}/{seed}/{fold}.out", shell=True)
            subprocess.call(f"mkdir -p {args.outdir}/{args.resdir}/{seed}", shell=True)
            print(f"{args.outdir}/{args.resdir}/{seed}/kfold.csv")
            subprocess.call(f"python /home/n/n_herr03/toadkfolds/hpc/evaluation/evaluate_models.py \
             --filename {args.modeldir}/{seed}/{fold} --resultfile {args.outdir}/{args.resdir}/{seed}/kfold.csv --test", shell=True)
        kfoldresults = pd.read_csv(f"{args.outdir}/{args.resdir}/{seed}/kfold.csv")
        meanval = kfoldresults["accuracy"].mean()
        print(meanval)
        subprocess.call(f"./{args.lightgbm} config={args.config} \
                    objective={args.objective} \
                    num_class={args.num_class} \
                    metric={args.metric} \
                    train_data={args.data_dir}/{seed}/{args.dataset}.train \
                    max_depth={args.max_depth} \
                    num_trees={args.num_trees} \
                    tinygbdt_forestsize={args.tinygbdt_forestsize} \
                    tinygbdt_penalty_split={args.tinygbdt_penalty_split} \
                    tinygbdt_penalty_feature={args.tinygbdt_penalty_feature} \
                    output_model={args.output_model}/{seed}/{args.resdir}.txt \
                    > {args.modeldir}/{seed}/{args.resdir}.out", shell=True)
        resultfile = f"{args.outdir}/results.csv"
        subprocess.call(f"mkdir -p {args.modeldir}/{seed}/{args.resdir}", shell=True)
        subprocess.call(f"mkdir -p {args.outdir}/{seed}", shell=True)
        subprocess.call(f"python  /home/n/n_herr03/toadkfolds/hpc/evaluation/evaluate_models.py \
                --filename {args.modeldir}/{seed}/{args.resdir} --resultfile {args.outdir}/{seed}/results.csv --val --mean={meanval}", shell=True)
        subprocess.call(f"rm -rf {args.modeldir}", shell=True)
        subprocess.call(f"rm -rf {args.modeldir}", shell=True)
        subprocess.call(f"rm -rf {args.modeldir}.txt", shell=True)
        subprocess.call(f"rm -rf {args.modeldir}.out", shell=True)
        subprocess.call(f"rm -rf {args.outdir}/{args.resdir}", shell=True)



