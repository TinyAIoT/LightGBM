import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from matplotlib.cm import viridis
from sklearn.datasets import load_svmlight_file


def plot_variance(results_folder, datasets, images_folder, showmemrange=False):
    df = pd.read_csv(f"./plotting/plottingdata/plotdata.csv")

    n_datasets = len(datasets)
    plt.rcParams.update({'font.size': 12})
    plt.rcParams.update({
        "axes.labelsize": 12,  # x/y label font size
        "xtick.labelsize": 11,  # tick labels
        "ytick.labelsize": 11,
    })
    # Plotting starts no further need for data processing
    fig, axes = plt.subplots(2, int(n_datasets / 2), figsize=(15, 5.5))
    for ax, dataset in zip(axes.flatten(), datasets):
        data = df[df['dataset'] == dataset].copy()
        data = data[data["val_acc"].between(0, 1)]
        data['max_memory'] = (data['max_memory'] / 8000).astype(str)
        markers =['^', ">", '<', 'd', 'h', 'X', '*']
        cmap = plt.get_cmap("tab20")

        colors = [cmap(i) for i in [0, 1, 18, 2, 3, 5, 6]]

        ordermem = ['0.25', '0.5', '1.0', '2.0', '4.0', '8.0', '16.0', '32.0', '64.0', '128.0', '256.0', '512.0', '1024.0', '2048.0']
        data['max_memory'] = pd.Categorical(data['max_memory'], categories=ordermem, ordered=True)
        data = data.sort_values('max_memory')
        order = ['lgbm_base', 'lgbm_quant', 'lgbm_array', 'rf', 'rf_guo', 'toad_nopen', 'toad_bpen']
        data['model'] = pd.Categorical(data['model'], categories=order, ordered=True)
        data = data.sort_values('model')
        l = sns.lineplot(data=data, x='max_memory', y='val_acc', style='model', hue='model',
                         hue_order=['lgbm_base', 'lgbm_quant', 'lgbm_array', 'rf', 'rf_guo', 'toad_nopen', 'toad_bpen'],
                         style_order=['lgbm_base', 'lgbm_quant', 'lgbm_array', 'rf', 'rf_guo', 'toad_nopen', 'toad_bpen'],
                         markers=markers, mew=0.2, ax=ax, linewidth=1, dashes=False, palette=colors, errorbar=('sd', 1))
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
            elif label == 'rf':
                new_labels[3] = 'Random Forest'
                new_handles[3] = handles[3]
            elif label == 'rf_guo':
                new_labels[4] = 'Pruned Random Forest'
                new_handles[4] = handles[4]
            elif label == 'toad_nopen':
                new_labels[5] = 'ToaD w/o Penalties'
                new_handles[5] = handles[5]
            elif label == 'toad_bpen':
                new_labels[6] = 'ToaD w/ best Penalties'
                new_handles[6] = handles[6]
            else:
                print("do nothing")
        # only plot lend in the first subplot otherwise no legend ['lgbm_base', 'sqtoad', 'logtoad', 'seed42', 'toad_nopen'],
        if dataset == datasets[0]:
            leg = ax.legend(new_handles, new_labels, title='Model', loc='lower right', fontsize=10)
            leg.set_title(None)
        else:
            ax.legend().remove()
        ax.tick_params(axis='x', rotation=65)
        # remove ytick labels in first row
        if dataset in datasets[:3]:
            ax.set_xticklabels([])
            ax.set_xlabel("")
        ax.grid()
        # ax.grid()

    plt.tight_layout()
    plt.savefig(f'{images_folder}pdf/rf_variance_comparison_{str(showmemrange)}_red.pdf', format='pdf')
    plt.savefig(f'{images_folder}png/rf_variance_comparison_{str(showmemrange)}_red.png', format='png')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot results from experiments')
    parser.add_argument('--results_folder', type=str, default='../results/valtest/', help='Directory where ToaD results are stored')
    parser.add_argument('--images_folder', type=str, default='./plotting/images/rebuttal/valtest/', help='Directory where images are saved')
    parser.add_argument('--data_folder', type=str, default='../results/data', help='Directory where datasets are stored')
    args = parser.parse_args()
    results_folder = args.results_folder
    images_folder = args.images_folder
    data_folder = args.data_folder


    log_base = 2
    barplot_check = False
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    not_reg = ['mushroom', 'covtype', 'breastcancer', 'kr-vs-kp', 'wine', 'covtype_multi']

    functions = ['simple']
    max_trees = 256
    max_depth = 4
    plot_variance(results_folder, not_reg, images_folder,  showmemrange=False)

