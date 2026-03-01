import pandas as pd
import itertools
import os
from pathlib import Path

def write_joblist(model, data, sed, remaining, listcreate, jobpath):
    out_path = f'{jobpath}/{model}-joblist.txt'
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "a") as f:
        for max_tree, depth, alpha in remaining:
            line = f"{model} {data} {max_tree} {depth} {alpha} {sed}\n"
            f.write(line)
    if out_path not in listcreate:
        listcreate.append(out_path)

def write_joblist_tree_depth(model, data, sed, remaining, listcreate, jobpath):
    out_path = f'{jobpath}/{model}-joblist.txt'
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "a") as f:
        for max_tree, depth in remaining:
            line = f"{model} {data} {max_tree} {depth} 0.0 {sed}\n"
            f.write(line)
    if out_path not in listcreate:
        listcreate.append(out_path)

def write_joblist_allmodels(data, sed, remaining, remaining2, listcreateallmodels, jobpath):
    out_path = f'{jobpath}/{data}/{seed}-joblist.txt'
    with open(out_path, "a") as f:
        for max_tree, depth, alpha, model in remaining:
            line = f"{model} {data} {max_tree} {depth} {alpha} {sed}\n"
            f.write(line)
    with open(out_path, "a") as f:
        for max_tree, depth, model in remaining2:
            line = f"{model} {data} {max_tree} {depth} 0.0 {sed}\n"
            f.write(line)

    if out_path not in listcreateallmodels:
        listcreateallmodels.append(out_path)

# max_trees,max_depth, tinygbdt_penalty_feature,tinygbdt_penalty_split
datasets = ['covtype', 'wine', 'covtype_multi', 'california_housing', 'kin8nm', 'mushroom', 'breastcancer', 'kr-vs-kp'] # breastcancer and kr-vs-kp are i.d.R. in a reasonable
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
trees   = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
depths  = [1, 2, 4, 8]
alpha = [0.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125]
models = ["lgbm_quant", "lgbm_base", "ccp", "cegb", 'rf', 'rf_guo']
alphamodels = ['cegb', 'ccp', 'rf_guo']
nonalphamodels = ["lgbm_quant", 'rf', "lgbm_base"]
all_without_models = list(itertools.product(
            trees,  # max_trees
            depths,  # max_depth
            alpha,  # tinygbdt_penalty_feature
        ))
all_without_models_walpha = list(itertools.product(
            trees,  # max_trees
            depths,  # max_depth sbatch --job-name="rest_rfguobase" hpc/baselines/zen2-128C-496G_remaining.sh reversed_shor_guo.txt
        ))
all_without_models_m = list(itertools.product(
            trees,  # max_trees
            depths,  # max_depth
            alpha,  # tinygbdt_penalty_feature
            alphamodels,
        ))
all_without_models_walpha_m = list(itertools.product(
            trees,  # max_trees
            depths,  # max_depth
            nonalphamodels,
        ))
listcreate = []
listcreateallmodels = []
jobpath = './results/valtest/joblistbl/'
dir_path = Path(jobpath)

for p in dir_path.iterdir():
    if p.is_file():
        p.unlink()
for seed in seeds:
    df = pd.DataFrame()
    for data in datasets:
        for model in models:
            if model == 'lgbm_quant' and data == 'california_housing':
                checkthis = True
            path = f'./results/valtest/baselines/{seed}/{model}/{data}/result.csv'
            if os.path.exists(path):
                df_allresults = pd.read_csv(path)
                df = pd.concat([df, df_allresults], ignore_index=True)

    df.drop_duplicates(inplace=True)
    df = df[df['nodes'] != 0]
    df.to_csv(f'./results/valtest/baselines/{seed}/allcollectresults.csv', index=False)
    if len(df) == 0:
        print(f'No data found for {seed}')
        continue
    # lgbm_quant,covtype_multi,1024,7168,8,0.0,0.3660190090072861,0.3683440545599277,0.3652315344698502,410318,0.0
    for data in datasets:
        dfdata = modeldf = df[df['dataset'] == data]
        for model in models:
            # do not process regression with random forest
            if model in ['rf', 'rf_guo'] and data in ['california_housing', 'kin8nm']:
                continue
            modeldf = dfdata[dfdata['model'] == model]
            if len(modeldf) == 0:
                if model in alphamodels:
                    remaining = [
                        combo for combo in all_without_models]
                    write_joblist(model, data, seed, remaining, listcreate, jobpath)
                else:
                    remaining = [
                        combo for combo in all_without_models_walpha]
                    write_joblist_tree_depth(model, data, seed, remaining, listcreate, jobpath)
                continue
            if model in alphamodels:
                cols = ["max_trees", "depth", "alpha"]
                df_done = modeldf[cols].copy()
                done_set = set(
                    df_done.itertuples(index=False, name=None)
                )
                remaining = [
                    combo for combo in all_without_models
                    if combo not in done_set
                ]
                if len(remaining) == 0:
                    continue
                write_joblist(model, data, seed, remaining, listcreate, jobpath)
            else:
                cols = ["max_trees", "depth"]
                df_done = modeldf[cols].copy()
                done_set = set(
                    df_done.itertuples(index=False, name=None)
                )
                remaining = [
                    combo for combo in all_without_models_walpha
                    if combo not in done_set
                ]
                if len(remaining) == 0:
                    continue
                write_joblist_tree_depth(model, data, seed, remaining, listcreate, jobpath)

print('missing parts of:')
for item in listcreate:
    with open(item, "r", encoding="utf-8") as f:
        n_lines = sum(1 for _ in f)
    print(f'{item} \t {n_lines}')
print('missing all of:')
for item in listcreateallmodels:
    with open(item, "r", encoding="utf-8") as f:
        n_lines = sum(1 for _ in f)
    print(f'{item} \t {n_lines}')
