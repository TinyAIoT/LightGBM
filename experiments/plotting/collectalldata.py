import os
import pandas as pd
from pathlib import Path
import sys
import numpy as np
cwd = Path.cwd()
if cwd.name != "experiments":
    sys.exit(f"Abort: run this from the 'experiments' directory. Current: {cwd}")

results_all = pd.DataFrame()
memory_limit_kb = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]  # , 4096, 8192, 16384]
memory_limits = [int(x * 8000) for x in memory_limit_kb]
df_baseline_res = pd.DataFrame()
seeds = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
datasets = ['mushroom', 'covtype', 'breastcancer', 'kr-vs-kp', 'kin8nm', 'california_housing', 'wine', 'covtype_multi']
showmemrange = False
results_folder = './results/valtest/'

for seed in seeds:
    path = os.path.join(f"{results_folder}baselines/{seed}/allcollectresults.csv")
    if not os.path.exists(path):
        print(f'could not find {seed}')
        continue

    all_baseline_results = pd.read_csv(path)
    m_quant = all_baseline_results["model"].eq("lgbm_quant")
    m_array = all_baseline_results["model"].eq("lgbm_array")
    m_qarr = all_baseline_results["model"].eq("lgbm_quant_arr")

    all_baseline_results.loc[m_quant, "memory_usage"] = 64 * all_baseline_results.loc[m_quant, "nodes"]

    all_baseline_results.loc[m_array, "memory_usage"] = (
        64 * all_baseline_results.loc[m_array, "nodes"]
    )

    all_baseline_results.loc[m_qarr, "memory_usage"] = (
        32 * all_baseline_results.loc[m_qarr, "nodes"]
    )

    # default case (everything else)
    m_default = ~(m_quant | m_array | m_qarr)
    all_baseline_results.loc[m_default, "memory_usage"] = 128 * all_baseline_results.loc[m_default, "nodes"]

    # --- Add-ons (apply to all rows matching these conditions) ---
    m_add2 = (
        all_baseline_results["dataset"].isin(["mushroom", "kr-vs-kp", "covtype", "breastcancer"])
        & all_baseline_results["model"].isin(["rf_base", "rf_guo"])
    )
    all_baseline_results.loc[m_add2, "memory_usage"] += 2 * 8 * all_baseline_results.loc[m_add2, "nodes"]

    m_add7 = (
        all_baseline_results["dataset"].isin(["covtype_multi", "wine"])
        & all_baseline_results["model"].isin(["rf_base", "rf_guo"])
    )
    all_baseline_results.loc[m_add7, "memory_usage"] += 7 * 8 * all_baseline_results.loc[m_add7, "nodes"]


    for data in datasets:
        dfseed = all_baseline_results[all_baseline_results['dataset'] == data]
        dfseed = dfseed[dfseed["val_acc"].between(0, 1)]

        if data == 'kin8nm':
            check = all_baseline_results[all_baseline_results['model'] == 'lgbm_base']
        models = ['lgbm_base', 'lgbm_quant', 'ccp', 'cegb', 'rf', 'rf_guo']
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

                if len(subset_mem_seed_model) == 0:
                    continue
                if subset_mem_seed_model.shape[0] > 0:

                    idx = subset_mem_seed_model[column].idxmax()

                    if pd.isna(idx):
                        # nothing to select (all values in `column` are NaN) -> skip this iteration
                        continue

                    best_row = subset_mem_seed_model.loc[idx]
                    betmem = best_row["memory_usage"]
                else:
                    print(f'could not find data for Model {model} \t {seed} \t {memory} \t {data}')
                    continue
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
                    "memory_usage": best_row['memory_usage'],
                    "max_memory": memory,
                    "randomseed": seed
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
                else:  # not subset_pen.empty: sed -i 's/toadkfolds/toad/g' hpc/baselines/zen4_generic_remaining.sh

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
                        "nodes": best_row.no_leaves * 2 - 1, "memory_usage": best_row[goal], "max_memory": memory,
                        "randomseed": seed
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
                        df['toad_penalty_feature'] == 0) & (df['toad_penalty_threshold'] == 0)]
                else:
                    subset_nopen = df[(df['our_bits'] <= memory) & (
                        df['toad_penalty_feature'] == 0) & (df['toad_penalty_threshold'] == 0)]
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
                        "max_memory": memory,
                        "randomseed": seed
                    }
                    results_all = pd.concat([results_all, pd.DataFrame([filled])], ignore_index=True)


results_all.to_csv(f"./plotting/plottingdata/plotdata.csv", index=False)
results_all_small = results_all[results_all['max_trees'] != 1024]
results_all_small = results_all_small[results_all_small['max_trees'] != 512]
results_all.to_csv(f"./plotting/plottingdata/plotdata_small.csv", index=False)
