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
    for fold in [0,1,2]:
        subprocess.call(f"mkdir -p {args.output_model}", shell=True)
        subprocess.call(f"./{args.lightgbm} config={args.config} \
            objective={args.objective} \
            num_class={args.num_class} \
            metric={args.metric} \
            train_data={args.data_dir}/{fold}/{args.dataset}.train \
            valid_data={args.data_dir}/{fold}/{args.dataset}.test \
            max_depth={args.max_depth} \
            num_trees={args.num_trees} \
            tinygbdt_forestsize={args.tinygbdt_forestsize} \
            tinygbdt_penalty_split={args.tinygbdt_penalty_split} \
            tinygbdt_penalty_feature={args.tinygbdt_penalty_feature} \
            output_model={args.output_model}/{fold}.txt \
                > {args.modeldir}/{fold}.out", shell=True)
        subprocess.call(f"mkdir -p {args.outdir}/{args.resdir}", shell=True)
        subprocess.call(f"python ./hpc/evaluation/evaluate_models.py \
         --filename {args.modeldir}/{fold} --resultfile {args.outdir}/{args.resdir}/kfold.csv --test", shell=True)
    kfoldresults = pd.read_csv(args.outdir + '/' + args.resdir + "/kfold.csv")
    meanval = kfoldresults["accuracy"].mean()
    print(meanval)
    subprocess.call(f"./{args.lightgbm} config={args.config} \
                objective={args.objective} \
                num_class={args.num_class} \
                metric={args.metric} \
                train_data={args.data_dir}/{args.dataset}.train \
                max_depth={args.max_depth} \
                num_trees={args.num_trees} \
                tinygbdt_forestsize={args.tinygbdt_forestsize} \
                tinygbdt_penalty_split={args.tinygbdt_penalty_split} \
                tinygbdt_penalty_feature={args.tinygbdt_penalty_feature} \
                output_model={args.output_model}.txt \
                > {args.modeldir}.out", shell=True)
    resultfile = f"{args.outdir}/results.csv"
    subprocess.call(f"python ./hpc/evaluation/evaluate_models.py \
            --filename {args.modeldir} --resultfile {args.outdir}/results.csv --val --mean={meanval}", shell=True)
    subprocess.call(f"rm -rf {args.modeldir}", shell=True)
    subprocess.call(f"rm -rf {args.modeldir}", shell=True)
    subprocess.call(f"rm -rf {args.modeldir}.txt", shell=True)
    subprocess.call(f"rm -rf {args.modeldir}.out", shell=True)
    subprocess.call(f"rm -rf {args.outdir}/{args.resdir}", shell=True)



