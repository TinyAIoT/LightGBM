import os
import pandas as pd
from matplotlib.cm import viridis
from pathlib import Path
import sys

cwd = Path.cwd()
if cwd.name != "experiments":
    sys.exit(f"Abort: run this from the 'experiments' directory. Current: {cwd}")

results_all = pd.DataFrame()

for seed in seeds:
    for data in datasets:
        dfseed = all_baseline_results[all_baseline_results['randomseed'] == float(seed)]
        dfseed = dfseed[dfseed['dataset'] == data]
        models = ['lgbm_base', 'lgbm_quant', 'lgbm_array', 'ccp', 'cegb']
        for model in models:
            dfseedmodel = dfseed[dfseed['model'] == model]
            prev_mem = 0
            column = 'test_accuracy'
            if data == 'breastcancer' or data == 'kr-vs-kp':
                column = 'meankfold'
            for memory in memory_limits:
                if showmemrange:
                    subset_mem_seed_model = dfseedmodel[(dfseedmodel['memory_usage'] <= memory) & (dfseedmodel['memory_usage'] > prev_mem) & (dfseedmodel['memory_usage'] != 0)]
                else:
                    subset_mem_seed_model = dfseedmodel[(dfseedmodel['memory_usage'] <= memory) & (dfseedmodel['memory_usage'] != 0)]

                if subset_mem_seed_model.shape[0] > 0:
                    best_row = subset_mem_seed_model.loc[subset_mem_seed_model[column].idxmax()]
                else:
                    print(f'could not find data for Model {model} \t {seed} \t {memory} \t {data}')
                    continue
                results_all = pd.concat([results_all, subset_mem_seed_model])
                filled = {
                    "model": model,
                    "dataset": data,
                    "max_trees": best_row.max_trees,
                    "no_trees": best_row.no_trees,
                    "depth": best_row.depth,
                    "alpha": best_row.alpha,
                    "train_loss": 1e+34,
                    "test_accuracy": best_row.test_accuracy,
                    "val_acc": best_row.val_acc,
                    "nodes": best_row.no_trees * (2 ** best_row.depth - 1),
                    "memory_usage": best_row.memory_usage,
                    "max_memory": memory
                }
                results_all = pd.concat([results_all, pd.DataFrame([filled])], ignore_index=True)
                prev_mem = memory

for seed in seeds:
    for data in datasets:
        path = os.path.join(f"{results_folder}normal/{data}/{seed}", 'results.csv')
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        df['LightGBMBits'] = (df['no_leaves'] * 2 - 1) * 128
        prev_mem = 0
        column = 'accuracy'
        if data == 'breastcancer' or data == 'kr-vs-kp':
            column = 'meankfold'
        goals = ['LightGBMBits', 'our_bits']
        for goal in goals:
            for memory in memory_limits:
                if showmemrange:
                    subset_pen = df[(df[goal] <= memory) & (df[goal] > prev_mem) & (df[goal] != 0)]
                else:
                    subset_pen = df[(df[goal] <= memory) & (df[goal] != 0)]
                if subset_pen.empty:
                    print(f"No ToaD with penalty for {data} and memory {memory} and seed {seed} and goal {goal}")
                else:  # not subset_pen.empty:
                    best_row = subset_pen.loc[subset_pen[column].idxmax()]
                    if goal == 'our_bits':
                        model = 'toad_bpen'
                    else:
                        model = 'lgbm_array'
                    filled = {
                        "model": model, "dataset": data, "max_trees": best_row.max_trees,
                        "no_trees": best_row.no_trees,
                        "depth": best_row.max_depth, "alpha": 0, "train_loss": 1e+34,
                        "test_accuracy": best_row[column], "val_acc": best_row.val_acc,
                        "nodes": best_row.no_leaves * 2 - 1, "memory_usage": best_row[goal], "max_memory": memory
                    }
                    results_all = pd.concat([results_all, pd.DataFrame([filled])], ignore_index=True)
                prev_mem = memory
        for memory in memory_limits:
            for data in datasets:
                path = os.path.join(f"{results_folder}normal/{data}/{seed}", 'results.csv')
                if not os.path.exists(path):
                    continue
                df = pd.read_csv(path)
                column = 'accuracy'
                if data == 'breastcancer' or data == 'kr-vs-kp':
                    column = 'meankfold'
                if showmemrange:
                    subset_nopen = df[(df['our_bits'] <= memory) & (df['our_bits'] > prev_mem) & (
                        df['tinygbdt_penalty_feature'] == 0) & (df['tinygbdt_penalty_split'] == 0)]
                else:
                    subset_nopen = df[(df['our_bits'] <= memory) & (
                        df['tinygbdt_penalty_feature'] == 0) & (df['tinygbdt_penalty_split'] == 0)]
                if subset_nopen.empty:
                    print(f"No ToaD without penalty for {data} and memory {memory}")
                else:
                    best_row = subset_nopen.loc[subset_nopen[column].idxmax()]
                    filled = {
                        "model": "toad_nopen",
                        "dataset": data,
                        "max_trees": best_row.max_trees,
                        "no_trees": best_row.no_trees,
                        "depth": best_row.max_depth,
                        "alpha": 0,
                        "train_loss": 1e+34,
                        "test_accuracy": best_row[column],
                        "val_acc": best_row.val_acc,
                        "nodes": best_row.no_leaves * 2 - 1,
                        "memory_usage": best_row.our_bits,
                        "max_memory": memory
                    }
                    results_all = pd.concat([results_all, pd.DataFrame([filled])], ignore_index=True)
results_all.to_csv(f"./plotting/plottingdata/plotdata.csv", index=False)
