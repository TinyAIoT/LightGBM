import os
from pydoc import describe
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re
from matplotlib.ticker import FuncFormatter
from matplotlib.cm import viridis
from matplotlib.colors import Normalize
import lightgbm as lgb
import helper.helper as hp
from pandas import read_csv
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score
# keyword is the substring of the filename to search for in model.txt and .out files

plotgrid = True
barplot = True
barplot_check = True
lineplot = True
lineplot2 = False

def plot_grid(df, axe, fig, norm, data, column='accuracy', title=''):
    scm = axe.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df[column], cmap='viridis',
                      label=column, norm=norm)
    # TODO find some metric to go beyond manually selecting points accuracy/memory?
    if column == 'accuracy':
        df['ratio'] = df['accuracy'] / df['our_bits']
        max_row = df.loc[df['ratio'].idxmax()]
        pcm = axe.scatter(max_row['tinygbdt_penalty_split'], max_row['tinygbdt_penalty_feature'], c="#FFA500", label='Max Accuracy', alpha=0.5)
    #plt.annotate('Max Accuracy', (df_max_accuracy['tinygbdt_penalty_split'], df_max_accuracy['tinygbdt_penalty_feature']))
    axe.set_xscale('log')
    axe.set_yscale('log')  # Correct method for setting y scale
    return scm

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
        axe.set_xscale('log')
    if plot_accuracy:
        axe.plot(df[keyword], df['accuracy'], '--o', label='Metric', color=colors[4], markersize=3)
        axe.tick_params(axis='y', color=colors[0])

    ax2 = axe.twinx()

    # Plot features or thresholds
    if xlabel == 'Feature Penalty':
        ax2.tick_params(axis='y', labelcolor=colors[2])
        ax2.plot(df[keyword], df['no_features'], 'o--', label="Features", color=colors[2], markersize=3)
        ax2.axhline(df['no_features'].iloc[0], linestyle=':', label="#Features\nPenalty = 0", color=colors[2])
        handles_axe, labels_axe = axe.get_legend_handles_labels()
    if xlabel == 'Threshold Penalty':
        axe3 = axe.twinx()
        ax2.tick_params(axis='y', labelcolor=colors[3])
        ax2.plot(df[keyword], df['no_thresholds'], 'o--', label="Values", color=colors[3], markersize=3)
        ax2.axhline(df['no_thresholds'].iloc[0], linestyle=':', label="#Values\nPenalty = 0", color=colors[3])
        axe3.plot(df[keyword], ((df['no_leaves']*2-1)/df['no_thresholds']), 'o--', label="Reuse factor", color=colors[1], markersize=3)
        axe3.tick_params(axis='y', labelcolor=colors[1], pad=8)
        axe3.spines['right'].set_position(('axes', 1))
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
        axe.set_xscale('log')
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

def plot_memory_acc(df, dfn, axe, ylim, fig, big=False):
    keywords = ['accuracy1', 'accuracy2','accuracy1', 'accuracy2']
    norm = Normalize(vmin=0, vmax=len(keywords) - 1)
    colors = [viridis(norm(i)) for i in range(len(keywords))]
    width = 0.25
    multiplier = 0
    if big:
        memory_values = [ 4096, 8192, 16384, 32768, 65536]
    else:
        memory_values = [ 4096, 8192, 16384, 32768, 65536]

    fp=df['tinygbdt_penalty_feature'].iloc[2]
    tp=df['tinygbdt_penalty_feature'].iloc[2]
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
        subset = df[(df['our_bits'] <= target) & (df['tinygbdt_penalty_feature'] <= fp) & (df['tinygbdt_penalty_split'] <= tp)]
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
    for attribute, measurement in myitems.items():
        offset = width * multiplier
        rects = axe.bar(x + offset, measurement, width, label=attribute, color=colors[multiplier])
        #axe.bar_label(rects, padding=3)
        multiplier += 1

    axe.set_ylim(ylim, 1)
    axe.set_xticks(x + width)  # Position the ticks at the center of the grouped bars
    kb_mem_val = []
    for memval in memory_values:
        kb_mem_val.append(hp.bits_to_kb(memval))

    axes[counter].set_xlabel("KB")
    axes[0].set_ylabel("Metric: \nAccuracy (binary)\n R2 (regression))")
    axe.set_xticklabels(kb_mem_val)  # Apply the custom labels

def getnaiverow(df, bits):
    returndf = pd.DataFrame()
    for bitvalue in bits:
        subset = df[(df['lgb_bits'] <= bitvalue)]
        returndf = pd.concat([returndf, subset.loc[subset['accuracy'].idxmax()].to_frame().T])
    return returndf

if not os.path.exists('../results/images'):
    os.makedirs('../results/images')
datasets = ['breastcancer', 'california_housing','kin8nm', 'kr-vs-kp', 'mushroom', 'covtype']  
binary = ['breastcancer', 'kr-vs-kp', 'mushroom', 'covtype']
regression = ['california_housing', 'kin8nm']
plt.rcParams['image.cmap'] = 'viridis'
functions = ['simple']
vminour_bits, vmaxour_bits, vminour_accuracy, vmaxour_accuracy = 1000, 0 , 1000, 0
for function in functions:
    for data in datasets:
        df = pd.read_csv('../results/' + data + '/last.csv')
        df = df[(df['our_bits'] != 0) ]
        data_tree_550_depth_3 = df[(df['max_trees'] == 100) ] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        minbits = data_tree_550_depth_3['our_bits'].min()
        vminour_bits, vmaxour_bits = min(minbits, vminour_bits), max(data_tree_550_depth_3['our_bits'].max(), vmaxour_bits)
        vminour_accuracy, vmaxour_accuracy = min(data_tree_550_depth_3['accuracy'].min(), vminour_accuracy), max(data_tree_550_depth_3['accuracy'].max(), vmaxour_accuracy)
        norm = mcolors.Normalize(vmin=vminour_bits, vmax=vmaxour_bits)  # Normalize color range
        norm2 = mcolors.Normalize(vmin=vminour_accuracy, vmax=vmaxour_accuracy)  # Normalize color range
if (plotgrid):
    for function in functions:
        fig, axes = plt.subplots(2, 6, figsize=(15, 4), sharex=True, sharey=True)
        counter = 0
        for data in datasets:
            df = pd.read_csv('../results/' + data + '/last.csv')
            df = df[(df['our_bits'] != 0) ]
            data_tree_550_depth_3 = df[(df['max_trees'] == 100) ]
            data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 100) ]# & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)]
            #graphs
            if (data in binary):
                axe=axes[0, counter].set_title(data + "\n(binary)")
            if (data in regression):
                axe=axes[0, counter].set_title(data + "\n(regression)")
            grid_memory = plot_grid(data_tree_550_depth_3_fptp_1000, axe=axes[0, counter], fig=fig, column='our_bits', data=data, norm=norm, title='Memory usage with changing penalties')
            grid_accuracy = plot_grid(data_tree_550_depth_3_fptp_1000, axe=axes[1,counter], fig=fig, column='accuracy', data=data, norm=norm2, title='Accuracy with changing penalties')
            axes[1, counter].set_xlabel('Threshold Penalty')
            counter =counter+1

        #cbar3 = fig.colorbar(grid_memory2, ax=axes[2], orientation='vertical', location='right', shrink=0.9, pad=0.01)
        cbar = fig.colorbar(grid_memory, ax=axes[0], orientation='vertical',  location='right', shrink=0.9, pad=0.01)
        cbar2 = fig.colorbar(grid_accuracy, ax=axes[1], orientation='vertical',  location='right', shrink=0.9, pad=0.01)
        # Divide by 1000 to convert to KB

        #cbar3.ax.yaxis.set_major_formatter(FuncFormatter(bits_to_kb))
        cbar.ax.yaxis.set_major_formatter(FuncFormatter(hp.bits_to_kb_str))

        axes[0,0].set_ylabel('Feature Penalty')
        axes[1,0].set_ylabel('Feature Penalty')
        axes[0,0].set_ylabel('Feature Penalty')
        axes[0,5].yaxis.set_label_position("right")
        axes[1,5].yaxis.set_label_position("right")

        axes[0,5].set_ylabel('Memory (KB)', labelpad=60)
        axes[1,5].set_ylabel('Metric: \nAccuracy (binary)\n R2 (regression))', labelpad=50)
        plt.savefig('../results/images/' + function + 'grid.png', format='png', dpi=300)
        plt.show()
if barplot_check:
    for function in functions:
        fig, axes = plt.subplots(1, 6, figsize=(15, 4))
        counter = 0
        for data in datasets:
            df = pd.read_csv('../results/' + data + '/last.csv')
            df = df[(df['our_bits'] != 0) ]
            dfn = df[(df['our_bits'] == 0) ]
            dsubset = df[(df['max_trees'] == 100) ] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            if (data in binary):
                axes[counter].set_title(data + "\n(binary)")
            if (data in regression):
                axes[counter].set_title(data + "\n(regression)")
            if data == 'breastcancer':
                plot_memory_acc(df, dfn, axes[counter], 0.9, fig)
            if data == 'california_housing':
                plot_memory_acc(df, dfn, axes[counter], 0.1, fig, True)
            if data == 'covtype':
                plot_memory_acc(df, dfn, axes[counter], 0.6, fig)
            if data == 'kin8nm':
                plot_memory_acc(df, dfn, axes[counter], 0.1, fig, True)
            if data == 'kr-vs-kp':
                plot_memory_acc(df, dfn, axes[counter], 0.85, fig)
            if data == 'mushroom':
                plot_memory_acc(df, dfn, axes[counter], 0.9, fig)
            counter = counter +1
        mergedhandles, mergedlabels = axes[0].get_legend_handles_labels()
        fig.legend(mergedhandles, mergedlabels, loc='center', bbox_to_anchor=(0.15,0.05), ncol=7)
        plt.savefig('../results/images/' + function + 'barplot.png', format='png', dpi=300)
        plt.show()

if lineplot2:
    for function in functions:
        fig, axes = plt.subplots( 2, 6, figsize=(15, 6), sharex=True, sharey=True)
        counter = 0
        for data in datasets:
            df = pd.read_csv('../results/' + data + '/last.csv')
            df = df[(df['our_bits'] != 0) ]
            data_tree_550_depth_3 = df[(df['max_trees'] == 100) ] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 100)  & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            if (data in binary):
                acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.85] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

            if (data in regression):
                acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.4] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

            acc_good_subset = acc_good_subset.sort_values(by='our_bits')
            data_tree_550_depth_3['tinygbdt_penalty_feature'] = pd.to_numeric(data_tree_550_depth_3['tinygbdt_penalty_feature'], errors='coerce')
            data_tree_550_depth_3_fptp_1000_fptp_1 = data_tree_550_depth_3_fptp_1000[(data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_feature'] > 0.001)& (data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_split'] > 0.001)]
            data_criteria_split_1 = data_tree_550_depth_3_fptp_1000_fptp_1[(data_tree_550_depth_3_fptp_1000_fptp_1['tinygbdt_penalty_split'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            data_criteria_feature_1 = data_tree_550_depth_3_fptp_1000_fptp_1[(data_tree_550_depth_3_fptp_1000_fptp_1['tinygbdt_penalty_feature'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            data_criteria_split_1 = data_criteria_split_1.sort_values(by='tinygbdt_penalty_feature')
            data_criteria_feature_1 = data_criteria_feature_1.sort_values(by='tinygbdt_penalty_split')
            #graphs
            if (data in binary):
                axe=axes[0, counter].set_title(data + "\n(binary)")
            if (data in regression):
                axe=axes[0, counter].set_title(data + "\n(regression)")
            if data in regression:
                handles, labels = plotAccuracyMemByPenalty(data_criteria_split_1, axes[0,counter], 'tinygbdt_penalty_feature', binary=False)
                handles2, labels2 = plotAccuracyMemByPenalty(data_criteria_feature_1, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty', binary=False)

            handles, labels = plotAccuracyMemByPenalty(data_criteria_split_1, axes[0,counter], 'tinygbdt_penalty_feature')
            handles2, labels2 = plotAccuracyMemByPenalty(data_criteria_feature_1, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty')
            counter = counter + 1
        mergedhandles = handles + handles2
        mergedlabels = labels + labels2
        #fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.05,0.985), ncol=5)
        fig.legend(mergedhandles, mergedlabels, loc='lower left', bbox_to_anchor=(0.05,0.015), ncol=7)
        axes[0,4].yaxis.set_label_position("right")
        axes[1,4].yaxis.set_label_position("right")
        axes[1,0].set_ylabel('Metric: Accuracy (binary)\n R2 (regression))')
        axes[0,0].set_ylabel('Metric: Accuracy (binary)\n R2 (regression))')

        plt.savefig('../results/images/' + function + 'lines.png', format='png', dpi=300)
        plt.show()
if lineplot:
    for function in functions:
        fig, axes = plt.subplots( 2, 6, figsize=(15, 6), sharex=True, sharey=True)
        counter = 0
        for data in datasets:
            df = pd.read_csv('../results/' + data + '/last.csv')
            df = df[(df['our_bits'] != 0) ]
            data_tree_550_depth_3 = df[(df['max_trees'] == 100)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 100) & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            if (data in binary):
                acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.85] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

            if (data in regression):
                acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.4] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

            acc_good_subset = acc_good_subset.sort_values(by='our_bits')
            data_tree_550_depth_3['tinygbdt_penalty_feature'] = pd.to_numeric(data_tree_550_depth_3['tinygbdt_penalty_feature'], errors='coerce')
            data_tree_550_depth_3_fptp_1000_fptp_1 = data_tree_550_depth_3_fptp_1000[(data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_feature'] > 0.001)& (data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_split'] > 0.001)]
            data_criteria_split_1 = data_tree_550_depth_3_fptp_1000_fptp_1[(data_tree_550_depth_3_fptp_1000_fptp_1['tinygbdt_penalty_split'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            data_criteria_feature_1 = data_tree_550_depth_3_fptp_1000_fptp_1[(data_tree_550_depth_3_fptp_1000_fptp_1['tinygbdt_penalty_feature'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
            data_criteria_split_1 = data_criteria_split_1.sort_values(by='tinygbdt_penalty_feature')
            data_criteria_feature_1 = data_criteria_feature_1.sort_values(by='tinygbdt_penalty_split')
            #graphs
            if (data in binary):
                axe=axes[0, counter].set_title(data + "\n(binary)")
            if (data in regression):
                axe=axes[0, counter].set_title(data + "\n(regression)")
            if data in regression:
                handles, labels = plotAccuracyByPenalty(data_criteria_split_1, axes[0,counter], 'tinygbdt_penalty_feature', binary=False, mem=False)
                handles2, labels2 = plotAccuracyByPenalty(data_criteria_feature_1, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty', binary=False, mem=False)

            handles, labels = plotAccuracyByPenalty(data_criteria_split_1, axes[0,counter], 'tinygbdt_penalty_feature', mem=False)
            handles2, labels2 = plotAccuracyByPenalty(data_criteria_feature_1, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty', mem=False)
            counter = counter + 1
        mergedhandles = handles + handles2
        mergedlabels = labels + labels2
        #fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.05,0.985), ncol=5)
        fig.legend(mergedhandles, mergedlabels, loc='lower left', bbox_to_anchor=(0.05,0.015), ncol=7)
        axes[0,4].yaxis.set_label_position("right")
        axes[1,4].yaxis.set_label_position("right")
        axes[1,0].set_ylabel('Metric: Accuracy (binary)\n R2 (regression))')
        axes[0,0].set_ylabel('Metric: Accuracy (binary)\n R2 (regression))')

        plt.savefig('../results/images/' + function + 'lines.png', format='png', dpi=300)
        plt.show()