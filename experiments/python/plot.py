import os
from pydoc import describe
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns
import re, csv
import argparse
from matplotlib.ticker import FuncFormatter, MaxNLocator
import matplotlib.ticker as ticker
from matplotlib.cm import viridis
from matplotlib.colors import Normalize
import lightgbm as lgb
import helper.helper as hp
from pandas import read_csv
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score
from sklearn.datasets import load_svmlight_file
# keyword is the substring of the filename to search for in model.txt and .out files

def preprocess_baselineresults(input_file, output_file):
    # Read whole file as text
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Merge multi-line bracketed fields into a single line
    # This regex finds [ ... ] possibly spanning multiple lines
    text = re.sub(r"\[(.*?)\]", 
                lambda m: "[" + " ".join(m.group(1).split()) + "]", 
                text, 
                flags=re.S)

    # Parse with CSV reader
    rows = []
    for row in csv.reader(text.splitlines()):
        new_row = []
        for field in row:
            if field.startswith("[") and field.endswith("]"):
                # Extract numbers inside brackets
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", field)
                new_row.append(numbers[-1] if numbers else "")
            else:
                new_row.append(field)
        rows.append(new_row)

    # Write cleaned CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def plot_grid(df, axe, fig, norm, data, column='accuracy', title=''):
    scm = axe.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df[column], cmap='viridis',
                      label=column, norm=norm)
    # TODO find some metric to go beyond manually selecting points accuracy/memory?
    if column == 'accuracy':
        df['ratio'] = df['accuracy'] / df['our_bits']
        #max_row = df.loc[df['ratio'].idxmax()]
        #pcm = axe.scatter(max_row['tinygbdt_penalty_split'], max_row['tinygbdt_penalty_feature'], c="#FFA500", label='Max Accuracy', alpha=0.5)
    #plt.annotate('Max Accuracy', (df_max_accuracy['tinygbdt_penalty_split'], df_max_accuracy['tinygbdt_penalty_feature']))
    axe.set_xscale('log', base=log_base)
    axe.set_yscale('log', base=log_base)  # Correct method for setting y scale
    return scm

def plot_maxMemGrid(df, column='accuracy', title=''):
    norm = mcolors.Normalize(vmin=df['accuracy'].min(), vmax=df['accuracy'].max())
    fig, ax = plt.subplots(figsize=(5, 4))
    scm = ax.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df[column], norm=norm, cmap='viridis')
    # TODO find some metric to go beyond manually selecting points accuracy/memory?
    if column == 'accuracy':
        # df['ratio'] = df['accuracy'] / df['our_bits']
        max_row = df.loc[df['accuracy'].idxmax()]
        ax.scatter(max_row['tinygbdt_penalty_split'], max_row['tinygbdt_penalty_feature'], c="#FF0000", label='Max Accuracy')
    ax.annotate('Best Model', (max_row['tinygbdt_penalty_split'], max_row['tinygbdt_penalty_feature']))
    ax.set_title(title)
    ax.set_xlabel('Threshold Penalty')
    ax.set_ylabel('Feature Penalty')
    ax.set_xscale('log', base=log_base)
    ax.set_yscale('log', base=log_base)  # Correct method for setting y scale
    ax.xaxis.set_major_locator(ticker.LogLocator(base=log_base, numticks=6))
    ax.yaxis.set_major_locator(ticker.LogLocator(base=log_base, numticks=6))
    
    fig.colorbar(scm, label="R2 score")

def plotAccuracyByPenalty(df, axe, keyword, fp=0, tp=0, plot_accuracy=True, xlog=True, xlabel='Feature Penalty', mem=True, binary=True):
    # Determine which keyword to use based on xlabel
    keywords = ['accuracy1', 'accuracy2', 'accuracy3', 'accuracy4', 'accuracy4', 'accuracy5']
    norm = Normalize(vmin=0, vmax=len(keywords) - 1)
    colors = [viridis(norm(i)) for i in range(len(keywords))]

    if xlabel == 'Feature Penalty' or xlabel == 'Both penalties':
        keyword = 'tinygbdt_penalty_feature'
    if xlabel == 'Threshold Penalty':
        keyword = 'tinygbdt_penalty_split'
    axe.set_xlabel(xlabel)
    if xlog:
        axe.set_xscale('log', base=log_base)
    if plot_accuracy:
        axe.plot(df[keyword], df['accuracy'], '--o', label='Metric', color=colors[4], markersize=4, linewidth=1)
        axe.tick_params(axis='y', color=colors[0])
    
    axe.xaxis.set_major_locator(ticker.LogLocator(base=log_base, numticks=6))

    ax2 = axe.twinx()

    # Plot features or thresholds
    if xlabel == 'Feature Penalty':
        ax2.tick_params(axis='y', labelcolor=colors[2], grid_color=colors[2])
        ax2.plot(df[keyword], df['no_features'], 'v--', label="#Features", color=colors[2], markersize=5, linewidth=1)
        ax2.axhline(df['no_features'].iloc[0], linestyle=':', label="#Features w/\nPenalty = 0", color=colors[2])
        handles_axe, labels_axe = axe.get_legend_handles_labels()
    if xlabel == 'Threshold Penalty':
        axe3 = axe.twinx()
        ax2.tick_params(axis='y', labelcolor=colors[3], colors=colors[3])
        # ax2.yaxis.set_major_locator(plt.FixedLocator([0, 250, 500, 750, 1000, 1250, 1500]))
        ax2.yaxis.set_major_locator(plt.MaxNLocator(4))
        ax2.plot(df[keyword], df['no_thresholds'], 'D--', label="#Values", color=colors[3], markersize=4, linewidth=1)
        ax2.axhline(df['no_thresholds'].iloc[0], linestyle=':', label="#Values w/\nPenalty = 0", color=colors[3])
        # reuse factor: (#leaves + #nodes) / (#thresholds + #leave-values)
        axe3.plot(df[keyword], ((df['no_leaves']*2-1)/df['no_thresholds']), 's--', label="Reuse factor", color=colors[1], markersize=4, linewidth=1)
        # reuse factor: #nodes / ~#thresholds -> because no_thresholds column includes leave values
        # axe3.plot(df[keyword], ((df['no_leaves']-1)/(df['no_thresholds']-df['no_leaves'])), 'o--', label="Reuse factor", color=colors[1], markersize=3)
        axe3.tick_params(axis='y', labelcolor=colors[1], colors=colors[1])
        axe3.spines['right'].set_position(('axes', 1))
        # axe3.yaxis.set_major_locator(plt.FixedLocator([1.0, 1.5, 2.0]))
        axe3.yaxis.set_major_locator(plt.MaxNLocator(4))
        handles_ax3, labels_ax3 = axe3.get_legend_handles_labels()
        handles_axe = handles_ax3
        labels_axe = labels_ax3


    handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()

    # Combine the handles and labels
    merged_handles = handles_ax2  + handles_axe
    merged_labels = labels_ax2 + labels_axe
    if mem:
        ax4 = ax2.twinx()
        ax4.plot(df[keyword], df['our_bits'], 'v--', label="Our Bits", color=colors[5], markersize=3)
        ax4.plot(df[keyword], df['lgb_bits'], '-.', label="naive Bits", color=colors[5], markersize=3)
        ax4.tick_params(axis='y', labelcolor=colors[5])
        handles_axe4, labels_axe4 = ax4.get_legend_handles_labels()
        merged_handles = merged_handles +handles_axe4
        merged_labels = merged_labels + labels_axe4
    return merged_handles, merged_labels

def plotAccuracyMemByPenalty(df, axe, keyword, plot_accuracy=True, xlog=True, xlabel='Feature Penalty', binary=True):
    # Determine which keyword to use based on xlabel
    keywords = ['accuracy1', 'accuracy2', 'accuracy3', 'accuracy4', 'accuracy4', 'accuracy5']
    norm = Normalize(vmin=0, vmax=len(keywords) - 1)
    colors = [viridis(norm(i)) for i in range(len(keywords))]

    if xlabel == 'Feature Penalty' or xlabel == 'Both penalties':
        keyword = 'tinygbdt_penalty_feature'
    if xlabel == 'Threshold Penalty':
        keyword = 'tinygbdt_penalty_split'
    axe.set_xlabel(xlabel)
    if xlog:
        axe.set_xscale('log', base=log_base)
    if plot_accuracy:
        axe.plot(df[keyword], df['accuracy'], '--o', label='Metric', color=colors[4], markersize=3)
        axe.tick_params(axis='y', color=colors[0])

    ax2 = axe.twinx()

    # Plot features or thresholds
    handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
    handles_axe, labels_axe = axe.get_legend_handles_labels()
    # Combine the handles and labels
    merged_handles = handles_ax2  + handles_axe
    merged_labels = labels_ax2 + labels_axe

    ax4 = ax2.twinx()
    ax4.plot(df[keyword], df['our_bits'], 'v--', label="Our Bits", color=colors[5], markersize=3)
    ax4.plot(df[keyword], df['lgb_bits'], '-.', label="naive Bits", color=colors[5], markersize=3)
    ax4.tick_params(axis='y', labelcolor=colors[5])
    handles_axe4, labels_axe4 = ax4.get_legend_handles_labels()
    merged_handles = merged_handles +handles_axe4
    merged_labels = merged_labels + labels_axe4
    return merged_handles, merged_labels 

    #ax2.legend(loc='upper right')

def plot_memory_acc(df, dfn, axe, ylim, fig, big=False, ylim_top=1):
    keywords = ['accuracy1', 'accuracy2','accuracy1', 'accuracy2']
    norm = Normalize(vmin=0, vmax=len(keywords) - 1)
    colors = [viridis(norm(i)) for i in range(len(keywords))]
    width = 0.25
    multiplier = 0
    if big:
        # memory_values = [ 65536, 131072, 262144, 524288, 1048576]
        memory_values = [ 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    else:
        memory_values = [ 4096, 8192, 16384, 32768, 65536]
        # memory_values = [ 8192, 16384, 32768, 65536, 131072]
    # Create a new DataFrame to store the best accuracy rows
    best_rows_toad = pd.DataFrame(columns=['no_trees','no_features','no_thresholds','no_leaves','our_bits','lgb_bits','logloss','rmse','accuracy','tinygbdt_penalty_feature','tinygbdt_penalty_split','max_trees','depth'])
    best_rows_naive = pd.DataFrame(columns=['no_trees','no_features','no_thresholds','no_leaves','our_bits','lgb_bits','logloss','rmse','accuracy','tinygbdt_penalty_feature','tinygbdt_penalty_split','max_trees','depth'])
    best_rows_naive_fp = pd.DataFrame(columns=['no_trees','no_features','no_thresholds','no_leaves','our_bits','lgb_bits','logloss','rmse','accuracy','tinygbdt_penalty_feature','tinygbdt_penalty_split','max_trees','depth'])
    test = pd.DataFrame(columns=['no_trees','no_features','no_thresholds','no_leaves','our_bits','lgb_bits','logloss','rmse','accuracy','tinygbdt_penalty_feature','tinygbdt_penalty_split','max_trees','depth'])

    zero_row = [0] * 13
    for target in memory_values:
        subset = df[(df['our_bits'] <= target)]
        if not subset.empty:
            best_row = subset.loc[subset['accuracy'].idxmax()]  # Select the entire row
            best_rows_toad = pd.concat([best_rows_toad, best_row.to_frame().T], ignore_index=True)  # Append the row

    for target in memory_values:
        subset = dfn[(dfn['lgb_bits'] <= target)]
        if not subset.empty:
            best_row_n = subset.loc[subset['accuracy'].idxmax()]  # Select the entire row
            best_rows_naive = pd.concat([best_rows_naive, best_row_n.to_frame().T], ignore_index=True)  # Append the row
        else :
            best_rows_naive = pd.concat([best_rows_naive, pd.DataFrame([zero_row], columns=test.columns)])

    for target in memory_values:
        # TODO: in my understanding, here we should check for our bits with penalties==0, i.e. dfn[(dfn['our_bits'] <= target)]
        subset = dfn[(dfn['our_bits'] <= target)]
        # subset = df[(df['our_bits'] <= target) & (df['tinygbdt_penalty_feature'] <= fp) & (df['tinygbdt_penalty_split'] <= tp)]
        if not subset.empty:
            best_row_n = subset.loc[subset['accuracy'].idxmax()]  # Select the entire row
            best_rows_naive_fp = pd.concat([best_rows_naive_fp, best_row_n.to_frame().T], ignore_index=True)  # Append the row
        else :
            best_rows_naive_fp = pd.concat([best_rows_naive_fp, pd.DataFrame([zero_row], columns=test.columns)])

    x = np.arange(len(best_rows_toad['our_bits']))
    myitems = {
        'Naive': (best_rows_naive['accuracy']),
        'ToaD': (best_rows_naive_fp['accuracy']),
        'ToaD + Penalty': (best_rows_toad['accuracy'])
    }
    
    # print(best_rows_naive)
    # print(best_rows_naive_fp)
    # print(best_rows_toad)
    
    for attribute, measurement in myitems.items():
        offset = width * multiplier
        rects = axe.bar(x + offset, measurement, width, label=attribute, color=colors[multiplier])
        #axe.bar_label(rects, padding=3)
        multiplier += 1

    axe.set_ylim(ylim, ylim_top)
    axe.set_xticks(x + width)  # Position the ticks at the center of the grouped bars
    kb_mem_val = []
    for memval in memory_values:
        kb_mem_val.append(hp.bits_to_kb(memval))

    axe.set_xlabel("KB")
    axe[0][0].set_ylabel("R2 score")
    axe[1][0].set_ylabel("Accuracy")
    axe[2][0].set_ylabel("Accuracy")
    # fig.supylabel("Metric: \nAccuracy (binary)\n R2 (regression))")
    if big:
        axe.tick_params(axis='x', labelrotation=45)
    axe.set_xticklabels(kb_mem_val)  # Apply the custom labels

def getnaiverow(df, bits):
    returndf = pd.DataFrame()
    for bitvalue in bits:
        subset = df[(df['lgb_bits'] <= bitvalue)]
        returndf = pd.concat([returndf, subset.loc[subset['accuracy'].idxmax()].to_frame().T])
    return returndf

def plot_figures(datasets, results_folder, images_folder, baseline_folder, data_folder, max_trees, max_depth, functions, multiclass, binary, regression, multivariate=True, univariate=False, plot_dots=False, memgrid=False, baselines=False):
    vminour_bits, vmaxour_bits = float('inf'), float('-inf')
    vminour_accuracy, vmaxour_accuracy = float('inf'), float('-inf')
    plt.rcParams['image.cmap'] = 'viridis'
    big = True
    
    for function in functions:
        for data in datasets:
            df = pd.read_csv(results_folder + data + '/results.csv')
            print(df)
            df = df[(df['our_bits'] != 0) ]
            # select the rows with 100 trees
            data_tree_550_depth_3 = df[(df['max_trees'] == max_trees) & (df['max_depth'] == max_depth)]  # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            minbits = data_tree_550_depth_3['our_bits'].min()
            # check for the minimum and maximum values of the bits and accuracy compared to values set above
            vminour_bits, vmaxour_bits = min(minbits, vminour_bits), max(data_tree_550_depth_3['our_bits'].max(), vmaxour_bits)
            vminour_accuracy, vmaxour_accuracy = min(data_tree_550_depth_3['accuracy'].min(), vminour_accuracy), max(data_tree_550_depth_3['accuracy'].max(), vmaxour_accuracy)
            norm = mcolors.Normalize(vmin=vminour_bits, vmax=vmaxour_bits)  # Normalize color range
            norm2 = mcolors.Normalize(vmin=vminour_accuracy, vmax=vmaxour_accuracy)  # Normalize color range
    if (multivariate):
        for function in functions:
            fig, axes = plt.subplots(2, 8, figsize=(20, 5), sharex=True, sharey=True)
            dots = [[8,9],[2,3],[10,11],[5,8],[8,8],[9,10],[6,8],[14,12]] # TODO: just added random values to wine and covtype_multi
            counter = 0
            for data in datasets:
                df = pd.read_csv(results_folder + data + '/results.csv')
                df = df[(df['tinygbdt_penalty_feature'] != 0) ]
                # TODO !: also filter for depth when its varied in the experiments
                # data_tree_550_depth_3 = df[(df['max_trees'] == 100) ]
                if data in multiclass:
                    data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == max_trees) & (df['max_depth'] == max_depth)]
                else:
                    data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == max_trees) & (df['max_depth'] == max_depth)]# & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)]
                #graphs
                if (data in binary):
                    axe=axes[0, counter].set_title(data + "\n(binary)")
                if (data in regression):
                    axe=axes[0, counter].set_title(data + "\n(regression)")
                if (data in multiclass):
                    axe=axes[0, counter].set_title(data + "\n(multiclass)")
                grid_memory = plot_grid(data_tree_550_depth_3_fptp_1000, axe=axes[0, counter], fig=fig, column='our_bits', data=data, norm=norm, title='Memory usage with changing penalties')
                grid_accuracy = plot_grid(data_tree_550_depth_3_fptp_1000, axe=axes[1,counter], fig=fig, column='accuracy', data=data, norm=norm2, title='Accuracy with changing penalties')
                if plot_dots:
                    axes[0,counter].scatter((2**(dots[counter][0])), (2**(dots[counter][1])), c="#FFA500")
                    axes[1,counter].scatter((2**(dots[counter][0])), (2**(dots[counter][1])), c="#FFA500")
                axes[1, counter].set_xlabel('Threshold Penalty')
                axes[1,counter].xaxis.set_major_locator(plt.LogLocator(base=log_base, numticks=5))
                axes[1,counter].yaxis.set_major_locator(plt.LogLocator(base=log_base, numticks=5))
                counter =counter+1

            #cbar3 = fig.colorbar(grid_memory2, ax=axes[2], orientation='vertical', location='right', shrink=0.9, pad=0.01)
            cbar = fig.colorbar(grid_memory, ax=axes[0], orientation='vertical',  location='right', shrink=0.9, pad=0.1, anchor=(1.1, 1.0))
            cbar2 = fig.colorbar(grid_accuracy, ax=axes[1], orientation='vertical',  location='right', shrink=0.9, pad=0.1, anchor=(1.1, 1.0))
            # Divide by 1000 to convert to KB

            #cbar3.ax.yaxis.set_major_formatter(FuncFormatter(bits_to_kb))
            cbar.locator = MaxNLocator(nbins=5)
            cbar.update_ticks()
            cbar.ax.yaxis.set_major_formatter(FuncFormatter(hp.bits_to_kb_str))

            axes[0,0].set_ylabel('Feature Penalty')
            axes[1,0].set_ylabel('Feature Penalty')
            axes[0,7].yaxis.set_label_position("right")
            axes[1,7].yaxis.set_label_position("right")

            axes[0,7].set_ylabel('Memory (KB)', labelpad=70)
            axes[1,7].set_ylabel('Metric: Accuracy\n R2 (regression))', labelpad=50)
            fig.subplots_adjust(bottom=0.15)
            # fig.tight_layout()
            plt.savefig(images_folder + function + 'grid.png', format='png', dpi=300)
            plt.savefig(images_folder + function + 'grid.pdf', format='pdf')
            plt.show()

    if memgrid:
        df = pd.read_csv('../results/results_mem/california_housing/last.csv')
        df = df[(df['tinygbdt_forestsize'] == 8000) ] # choose from 8000, 16000, 64000 bits
        grid_memory = plot_maxMemGrid(df, title='Penalty Grid Search, California Housing, 1 KB')
        plt.savefig(images_folder + 'memory_grid.png', format='png', dpi=300)
        plt.savefig(images_folder + 'memory_grid.pdf', format='pdf')
        plt.tight_layout()
        plt.show()

    if barplot_check:
        for function in functions:
            fig, axes = plt.subplots(3, 2, figsize=(15, 4))
            print(len(axes), len(axes[0]), len(axes[1]))
            counter_x = 0
            counter_y = 0
            for data in datasets:
                print(data)
                df = pd.read_csv(results_folder + data + '/results.csv')
                df = df[(df['our_bits'] != 0.0) ]
                dfn = df[(df['tinygbdt_penalty_feature'] == 0.0) & (df['tinygbdt_penalty_split'] == 0.0)]
                dsubset = df[(df['max_trees'] == max_trees) ] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
                print(counter_x, counter_y)
                if (data in binary):
                    axes[counter_x][counter_y].set_title(data + "\n(binary)")
                if (data in regression):
                    axes[counter_x][counter_y].set_title(data + "\n(regression)")
                if data == 'california_housing':
                    plot_memory_acc(df, dfn, axes[counter_x][counter_y], 0.2, fig, big, ylim_top=0.9)
                    counter_y += + 1
                if data == 'kin8nm':
                    plot_memory_acc(df, dfn, axes[counter_x][counter_y], 0.1, fig, big, ylim_top=0.8)
                    counter_x += + 1
                if data == 'covtype':
                    plot_memory_acc(df, dfn, axes[counter_x][counter_y], 0.7, fig, big, ylim_top=0.85)
                    counter_y -= + 1
                if data == 'breastcancer':
                    plot_memory_acc(df, dfn, axes[counter_x][counter_y], 0.9, fig, big)
                    counter_x += 1
                if data == 'kr-vs-kp':
                    plot_memory_acc(df, dfn, axes[counter_x][counter_y], 0.9, fig, big)
                    counter_y += 1
                if data == 'mushroom':
                    plot_memory_acc(df, dfn, axes[counter_x][counter_y], 0.995, fig, big)
            mergedhandles, mergedlabels = axes[0][0].get_legend_handles_labels()
            # fig.legend(mergedhandles, mergedlabels, loc='center', bbox_to_anchor=(0.15,0.05), ncol=7)
            fig.legend(mergedhandles, mergedlabels, loc='center', bbox_to_anchor=(0.5,0.05), ncol=7)
            plt.savefig(images_folder + function + 'barplot.png', format='png', dpi=300)
            plt.savefig(images_folder + function + 'barplot.pdf', format='pdf')
            plt.show()

    if univariate:
        for function in functions:
            fig, axes = plt.subplots(2, 8, figsize=(15, 6), sharex=True, sharey=True)
            counter = 0
            max_trees = 256
            max_depth = 2
            for data in datasets:
                df = pd.read_csv(results_folder + data + '/results.csv')
                df = df[(df['our_bits'] != 0) ]
                data_tree_550_depth_3 = df[(df['max_trees'] == max_trees) & (df['max_depth'] == max_depth)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
                # data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 100) & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)  & (df['max_depth'] == 3)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
                data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == max_trees) & (df['max_depth'] == max_depth)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
                if (data in binary):
                    acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.85] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

                if (data in regression):
                    acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.4] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

                acc_good_subset = acc_good_subset.sort_values(by='our_bits')
                data_tree_550_depth_3['tinygbdt_penalty_feature'] = pd.to_numeric(data_tree_550_depth_3['tinygbdt_penalty_feature'], errors='coerce')
                # data_tree_550_depth_3_fptp_1000_fptp_1 = data_tree_550_depth_3_fptp_1000[(data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_feature'] > 0.001)& (data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_split'] > 0.001)]
                data_criteria_split_0 = data_tree_550_depth_3_fptp_1000[(data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_split'] == 0.0) & (data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_feature'] > 0.0)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
                data_criteria_feature_0 = data_tree_550_depth_3_fptp_1000[(data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_feature'] == 0.0) & (data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_split'] > 0.0)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
                data_criteria_split_0 = data_criteria_split_0.sort_values(by='tinygbdt_penalty_feature')
                data_criteria_feature_0 = data_criteria_feature_0.sort_values(by='tinygbdt_penalty_split')
                #graphs
                if (data in binary):
                    axe=axes[0, counter].set_title(data + "\n(binary)")
                if (data in regression):
                    axe=axes[0, counter].set_title(data + "\n(regression)")
                if (data in multiclass):
                    axe=axes[0, counter].set_title(data + "\n(multiclass)")
                if data in regression:
                    handles, labels = plotAccuracyByPenalty(data_criteria_split_0, axes[0,counter], 'tinygbdt_penalty_feature', binary=False, mem=False)
                    handles2, labels2 = plotAccuracyByPenalty(data_criteria_feature_0, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty', binary=False, mem=False)

                handles, labels = plotAccuracyByPenalty(data_criteria_split_0, axes[0,counter], 'tinygbdt_penalty_feature', mem=False)
                handles2, labels2 = plotAccuracyByPenalty(data_criteria_feature_0, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty', mem=False)
                counter = counter + 1
            mergedhandles = handles + handles2
            mergedlabels = labels + labels2
            #fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.05,0.985), ncol=5)
            # fig.legend(mergedhandles, mergedlabels, loc='lower left', bbox_to_anchor=(0.05,0.015), ncol=7)
            fig.legend(mergedhandles, mergedlabels, loc='center', bbox_to_anchor=(0.5,0.05), ncol=7)
            axes[0,4].yaxis.set_label_position("right")
            axes[1,4].yaxis.set_label_position("right")
            axes[1,0].set_ylabel('Metric: Accuracy\n R2 (regression))')
            axes[0,0].set_ylabel('Metric: Accuracy\n R2 (regression))')

            fig.tight_layout()
            plt.savefig(images_folder + function + 'lines.png', format='png', dpi=300)
            plt.savefig(images_folder + function + 'lines.pdf', format='pdf')
            plt.show()

    if baselines:
        baseline_results = pd.read_csv(baseline_folder + "/baseline_results.csv")

        # add column for memory usage calculated by 64 * nodes if model is lgbm_quant, otherwise 128 * nodes
        baseline_results['memory_usage'] = baseline_results.apply(lambda row: 64 * row['nodes'] if row['model'] in ['lgbm_quant'] else 128 * row['nodes'], axis=1)
        classification_datasets = binary + multiclass
        regression_datasets = regression
        datasets = classification_datasets + regression_datasets
        # define memory limits in KB
        memory_limit_kb = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]#, 4096, 8192, 16384]
        memory_limits = [int(x * 8000) for x in memory_limit_kb]
        # create empty pandas dataframe to store results
        df_baseline_res = pd.DataFrame()
        # for each type of model find the best result for each dataset based on the highest test score that is below a memory usage of 100000
        for memory in memory_limits:
            best_classification_results_ids = baseline_results[(baseline_results['memory_usage'] <= memory) & (baseline_results['dataset'].isin(classification_datasets))].groupby(['model', 'dataset'])['test_accuracy'].idxmax()
            best_regression_results_ids = baseline_results[(baseline_results['memory_usage'] <= memory) & (baseline_results['dataset'].isin(regression_datasets))].groupby(['model', 'dataset'])['test_accuracy'].idxmin()
            best_results_ids = pd.concat([best_classification_results_ids, best_regression_results_ids])
            best_results = baseline_results.loc[best_results_ids]
            best_results['max_memory'] = memory
            df_baseline_res = pd.concat([df_baseline_res, best_results])
        results_all = df_baseline_res.copy()
        # for regression datasets convert rmse to R2 score
        # calculate variance of target column for each regression dataset
        for data in regression:
            d = load_svmlight_file(f"{data_folder}/{data}.test")
            y_true = d[1]
            var = np.var(y_true, ddof=0)
            # where results_all is in regression_datasets and dataset == data convert rmse to R2 score
            results_all.loc[(results_all['dataset'] == data), 'test_accuracy'] = 1 - (results_all.loc[(results_all['dataset'] == data), 'test_accuracy'] / var)


        for data in datasets:
            path = os.path.join(results_folder, data, 'results.csv')
            if not os.path.exists(path):
                continue
            df = pd.read_csv(path)
            for memory in memory_limits:
                # our_bits != 0 because of some weird results with 0 memory
                # TODO: evaluate/train again (covtype_multi)
                subset_pen = df[(df['our_bits'] <= memory) & (df['our_bits'] != 0) & (df['tinygbdt_penalty_feature'] != 0) & (df['tinygbdt_penalty_split'] != 0)]
                if subset_pen.empty:
                    print(f"No ToaD with penalty for {data} and memory {memory}")
                else: # not subset_pen.empty:
                    if data in regression_datasets:
                        best_row = subset_pen.loc[subset_pen['accuracy'].idxmax()]
                    else:
                        best_row = subset_pen.loc[subset_pen['accuracy'].idxmax()]
                        print(memory)
                        print(best_row) 
                    filled = {
                        "model": "toad_pen",
                        "dataset": data,
                        "max_trees": best_row.max_trees,
                        "no_trees": best_row.no_trees,
                        "depth": best_row.max_depth,
                        "alpha": 0,
                        "train_loss": 1e+34,
                        "test_accuracy": best_row.accuracy,
                        "nodes": best_row.no_leaves*2-1,
                        "memory_usage": best_row.our_bits,
                        "max_memory": memory
                    }
                    # print(filled)
                    # add filled as new row to df_baseline_res
                    results_all = pd.concat([results_all, pd.DataFrame([filled])], ignore_index=True)
                subset_nopen = df[(df['our_bits'] <= memory) & (df['tinygbdt_penalty_feature'] == 0) & (df['tinygbdt_penalty_split'] == 0)]
                if subset_nopen.empty:
                    print(f"No ToaD without penalty for {data} and memory {memory}")
                else: # not subset_nopen.empty:
                    if data in regression_datasets:
                        best_row = subset_nopen.loc[subset_nopen['accuracy'].idxmax()]
                    else:
                        best_row = subset_nopen.loc[subset_nopen['accuracy'].idxmax()] 
                    filled = {
                        "model": "toad_nopen",
                        "dataset": data,
                        "max_trees": best_row.max_trees,
                        "no_trees": best_row.no_trees,
                        "depth": best_row.max_depth,
                        "alpha": 0,
                        "train_loss": 1e+34,
                        "test_accuracy": best_row.accuracy,
                        "nodes": best_row.no_leaves*2-1,
                        "memory_usage": best_row.our_bits,
                        "max_memory": memory
                    }
                    # print(filled)
                    # add filled as new row to df_baseline_res
                    results_all = pd.concat([results_all, pd.DataFrame([filled])], ignore_index=True)

        df = results_all
        n_datasets = len(datasets)

        fig, axes = plt.subplots(2, int(n_datasets/2), figsize=(15, 5.5))
        for ax, dataset in zip(axes.flatten(), datasets):
            data = df[df['dataset'] == dataset].copy()
            # Convert max_memory to string for categorical x-axis
            data['max_memory'] = (data['max_memory']/8000).astype(str)
            markers = ['o', 's', 'D', '^', 'v', 'X']#, '*', 'P', '<', '>']

            l = sns.lineplot(
                data=data,
                x='max_memory',
                y='test_accuracy',
                style='model',
                hue='model',
                hue_order=['lgbm_base', 'lgbm_quant', 'cegb', 'ccp', 'toad_pen', 'toad_nopen'],
                # marker='o',
                markers=markers,
                # mec=None, # marker edge color
                mew=0.2, # marker edge width
                ax=ax,
                linewidth=1,
                dashes=False,
                # palette=cmap.colors
                palette='tab20'
                # legend=False
            )
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
            new_handles = handles.copy()
            new_labels = labels.copy()
            for i, label in enumerate(labels):
                if label == 'lgbm_base':
                    new_labels[0] = 'LightGBM'
                    new_handles[0] = handles[i]
                elif label == 'lgbm_quant':
                    new_labels[1] = 'LightGBM FP16'
                    new_handles[1] = handles[i]
                elif label == 'ccp':
                    new_labels[3] = 'CCP'
                    new_handles[3] = handles[i]
                elif label == 'cegb':
                    new_labels[2] = 'CEGB'
                    new_handles[2] = handles[i]
                elif label == 'toad_pen':
                    new_labels[4] = 'ToaD w/ best Penalties'
                    new_handles[4] = handles[i]
                elif label == 'toad_nopen':
                    new_labels[5] = 'ToaD w/o Penalties'
                    new_handles[5] = handles[i]
                else:
                    new_labels.append(label)
            # only plot legend in the first subplot otherwise no legend
            if dataset == datasets[0]:
                ax.legend(new_handles, new_labels, title='Model')
            else:
                ax.legend().remove()
            ax.tick_params(axis='x', rotation=65)
            # remove ytick labels in first row
            if dataset in datasets[:4]:
                ax.set_xticklabels([])
                ax.set_xlabel("")
            # ax.grid()
        plt.tight_layout()
        plt.savefig(images_folder + 'baseline_comparison.pdf', format='pdf')
        plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot results from experiments')
    parser.add_argument('--results_folder', type=str, default='../../hpc/evaluation/results/', help='Directory where ToaD results are stored')
    parser.add_argument('--baseline_results_folder', type=str, default='../baselines', help='Directory where baseline results are stored')
    parser.add_argument('--images_folder', type=str, default='../results/images/', help='Directory where images are saved')
    parser.add_argument('--data_folder', type=str, default='../data/', help='Directory where datasets are stored')
    args = parser.parse_args()
    results_folder = args.results_folder
    images_folder = args.images_folder
    baseline_folder = args.baseline_results_folder
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
    datasets = ['california_housing','kin8nm', 'covtype', 'breastcancer', 'kr-vs-kp', 'mushroom', 'wine', 'covtype_multi']  
    binary = ['breastcancer', 'kr-vs-kp', 'mushroom', 'covtype']
    regression = ['california_housing', 'kin8nm']
    multiclass = ['covtype_multi', 'wine']
    functions = ['simple']
    max_trees = 256
    max_depth = 4

    plot_figures(datasets, results_folder, images_folder, baseline_folder, data_folder, max_trees, max_depth, functions, multiclass, binary, regression, multivariate=multivariate, univariate=univariate, plot_dots=plot_dots, memgrid=memgrid, baselines=baselines)