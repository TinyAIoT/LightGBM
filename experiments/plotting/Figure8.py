import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from matplotlib.cm import viridis
from sklearn.datasets import load_svmlight_file


def convertsingle_rsme_to_r2(seed, data, val_acc, data_folder):
    d = load_svmlight_file(f"{data_folder}{seed}/{data}.test")
    y_true = d[1]
    var = np.var(y_true, ddof=0)
    return (1-(val_acc/var))

def collect_data(seeds, memory_limits, showmemrange, all_baseline_results):
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
    results_all.to_csv(f"{results_folder}normal/plotdata.csv", index=False)
    return results_all

def convert_rsme_to_r2(seed, data, df, data_folder):
    d = load_svmlight_file(f"{data_folder}{seed}/{data}.test")
    y_true = d[1]
    var = np.var(y_true, ddof=0)
    df.loc[(df['dataset'] == data), 'val_acc'] = 1 - (df.loc[(df['dataset'] == data), 'val_acc'] / var)
    df.loc[(df['dataset'] == data), 'val_acc'] = 1 - (df.loc[(df['dataset'] == data), 'val_acc'] / var)

def plot_variance(results_folder, datasets, images_folder, newdata, showmemrange=False):
    memory_limit_kb = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]  # , 4096, 8192, 16384]
    memory_limits = [int(x * 8000) for x in memory_limit_kb]
    df_baseline_res = pd.DataFrame()
    seeds = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
    for seed in seeds:
        path = os.path.join(f"{results_folder}baselines/{seed}/bestr2results.csv")
        if not os.path.exists(path):
            continue
        df = pd.read_csv(path)
        df_baseline_res = pd.concat([df_baseline_res, df])

    allbaselineresults = df_baseline_res.copy()

    if not os.path.exists(f"{results_folder}normal/plotdata.csv") or newdata == 1:
        df = collect_data(seeds, memory_limits, showmemrange, allbaselineresults)
    else:
        df = pd.read_csv(f"{results_folder}normal/plotdata.csv")

    n_datasets = len(datasets)

    # Plotting starts no further need for data processing
    fig, axes = plt.subplots(2, int(n_datasets / 2), figsize=(15, 5.5))
    for ax, dataset in zip(axes.flatten(), datasets):
        data = df[df['dataset'] == dataset].copy()
        data['max_memory'] = (data['max_memory'] / 8000).astype(str)
        markers = ['o', 's', 'D', '^', 'v', 'X', '*']  # , , 'X', '*', 'P', '<', '>']
        order = ['lgbm_base', 'lgbm_quant', 'lgbm_array', 'ccp', 'cegb', 'toad_nopen', 'toad_bpen']
        data['model'] = pd.Categorical(data['model'], categories=order, ordered=True)
        data = data.sort_values('model')
        ordermem = ['0.25', '0.5', '1.0', '2.0', '4.0', '8.0', '16.0', '32.0', '64.0', '128.0', '256.0', '512.0', '1024.0', '2048.0']
        data['max_memory'] = pd.Categorical(data['max_memory'], categories=ordermem, ordered=True)
        data = data.sort_values('max_memory')
        l = sns.lineplot(data=data, x='max_memory', y='val_acc', style='model', hue='model',
                         hue_order=['lgbm_base', 'lgbm_quant', 'lgbm_array', 'ccp', 'cegb', 'toad_nopen', 'toad_bpen'],
                         markers=markers, mew=0.2, ax=ax, linewidth=1, dashes=False, palette='tab20', errorbar=('sd', 1))
        sns.set_style("whitegrid")
        ax.set_xlabel("Max Memory (KB)")
        if dataset in ["california_housing", "kin8nm"]:
            ax.set_ylabel("R2 Score")
            datatype = "regression"
        elif dataset in ["wine", "covtype_multi"]:
            ax.set_ylabel("Accuracy")
            datatype = "multiclass"
        else:
            ax.set_ylabel("Accuracy")
            datatype = "binary"
        ax.set_title(f"{dataset} ({datatype})")
        # adjust legend labels
        handles, labels = ax.get_legend_handles_labels()
        counter = 0
        new_handles = handles.copy()
        new_labels = labels.copy()
        for i, label in enumerate(labels):
            if label == 'lgbm_base':
                new_labels[0] = 'LightGBM'
                new_handles[0] = handles[0]
            elif label == 'lgbm_quant':
                new_labels[1] = 'LightGBM FP16'
                new_handles[1] = handles[1]
            elif label == 'lgbm_array':
                new_labels[2] = 'LightGBM array-based'
                new_handles[2] = handles[2]
            elif label == 'ccp':
                new_labels[3] = 'CPP'
                new_handles[3] = handles[3]
            elif label == 'cegb':
                new_labels[4] = 'CEGB'
                new_handles[4] = handles[5]
            elif label == 'toad_nopen':
                new_labels[5] = 'ToaD w/o Penalties'
                new_handles[5] = handles[4]
            elif label == 'toad_bpen':
                new_labels[6] = 'ToaD w/ best Penalties'
                new_handles[6] = handles[6]
            else:
                print("do nothing")
                #new_labels.append(label)
        # only plot lend in the first subplot otherwise no legend ['lgbm_base', 'sqtoad', 'logtoad', 'seed42', 'toad_nopen'],
        if dataset == datasets[0]:
            ax.legend(new_handles, new_labels, title='Model', loc='lower right')
        else:
            ax.legend().remove()
        ax.tick_params(axis='x', rotation=65)
        # remove ytick labels in first row
        if dataset in datasets[:4]:
            ax.set_xticklabels([])
            ax.set_xlabel("")
        ax.grid()
        # ax.grid()

    plt.tight_layout()
    plt.savefig(images_folder + 'pdf/' + str(showmemrange) + '1-710-12-variance_comparison.pdf', format='pdf')
    plt.savefig(images_folder + 'png/' + str(showmemrange) + '1-710-12-variance_comparison.png', format='png')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot results from experiments')
    parser.add_argument('--results_folder', type=str, default='../results/valtest/', help='Directory where ToaD results are stored')
    parser.add_argument('--images_folder', type=str, default='../results/images/rebuttal/valtest/', help='Directory where images are saved')
    parser.add_argument('--data_folder', type=str, default='../results/data', help='Directory where datasets are stored')
    args = parser.parse_args()
    results_folder = args.results_folder
    images_folder = args.images_folder
    data_folder = args.data_folder

    univariate = True
    multivariate = True
    baselines = True
    plot_dots = True # whether to plot orange dots on grid
    memgrid = True
    log_base = 2
    barplot_check = False
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    datasets = [ 'mushroom', 'covtype', 'breastcancer', 'kr-vs-kp', 'kin8nm', 'california_housing', 'wine', 'covtype_multi']
    binary = ['breastcancer', 'kr-vs-kp', 'mushroom', 'covtype']
    regression = ['california_housing', 'kin8nm']
    multiclass = ['covtype_multi', 'wine']
    functions = ['simple']
    max_trees = 256
    max_depth = 4
    newdata = args.new
    # sed -i -e 's/seed10toad/seed4toad/g' *.sh
    # plot_penalties(results_folder, datasets, images_folder, showmemrange=False)
    # plot_randomforest(results_folder, datasets, images_folder, showmemrange=False)
    plot_variance(results_folder, datasets, images_folder, newdata,  showmemrange=False)

