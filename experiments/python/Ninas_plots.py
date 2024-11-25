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
from pandas import read_csv
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score
# keyword is the substring of the filename to search for in model.txt and .out files

plotgrid = False
def plotMetrics(df, axe, log_scale=False):
    setting_value = df['tinygbdt_penalty_split']
    color = 'tab:red'
    axe.set_xlabel('tinygbdt_penalty_split')
    if log_scale:
        axe.set_xscale('log')
    # Plot on the main Axes
    if len(df['logloss']) > 0 and df['logloss'].iloc[-1] != 0:
        axe.set_ylabel('Logloss', color=color)
        axe.plot(setting_value, df['logloss'], color=color, label='Logloss')

    if len(df['rmse']) > 0 and df['rmse'].iloc[-1] != 0:
        axe.set_ylabel('R2 Score', color=color)
        axe.plot(setting_value, df['accuracy'], color=color, label='R2 Score')

    axe.plot(setting_value, df['accuracy'], color='tab:purple', label='Accuracy/R2')
    axe.tick_params(axis='y', labelcolor=color)
    axe.legend(loc='upper left')

    # Create a twin Axes for each additional y-axis
    ax2 = axe.twinx()
    ax2.set_ylabel('count')
    ax2.plot(setting_value, df['no_thresholds'], label="no. thresholds")
    ax2.plot(setting_value, df['no_leaves'], label="no. leaves")
    ax2.legend(loc='upper right')

    ax3 = axe.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset the spine
    ax3.set_ylabel('bit count')
    ax3.plot(setting_value, df['our_bits'], color='tab:pink', label="no. bits")
    ax3.plot(setting_value, df['lgb_bits'], color='tab:brown', label="no. bits Naive")
    ax3.legend(loc='upper right')
    ax4 = axe.twinx()
    ax4.spines['right'].set_position(('outward', 120))  # Offset the spine
    ax4.set_ylabel('no. features/trees', color='tab:green')
    ax4.plot(setting_value, df['no_features'], label="no. features", color='tab:green')
    ax4.plot(setting_value, df['no_trees'], label="no. trees", color='tab:cyan')
    ax4.tick_params(axis='y', labelcolor='tab:green')
    ax4.legend(loc='lower right')

    axe.figure.tight_layout()

def plot_grid(df, axe, fig, norm, column='accuracy', title=''):
    scm = axe.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df[column], cmap='viridis',
                label=column, norm=norm)
    axe.set_xscale('log')
    axe.set_yscale('log')  # Correct method for setting y scale
    return scm
def rgb_to_hex(r, g, b):
    r_int = int(r * 255)
    g_int = int(g * 255)
    b_int = int(b * 255)
    return ('{:02X}' * 3).format(r_int, g_int, b_int)
def generatecolors(rangeint):
    norm2 = Normalize(vmin=0, vmax=rangeint - 1)
    colors2 = [viridis(norm2(i)) for i in range(rangeint)]
    for x in range(rangeint):
        print(rgb_to_hex(colors2[x][0], colors2[x][1], colors2[x][2]))
def plotAccuracyByPenalty(df, axe, keyword, plot_accuracy=True, plot_nodeLeafCount=False, xlog=True, xlabel='Feature Penalty'):
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
        if df['logloss'].iloc[1] == 0.0:
            label = 'R2 Score'
        else:
            label = 'Accuracy'

        axe.plot(df[keyword], df['accuracy'], '--o', label=label, color=colors[2], markersize=3)

        max_accuracy = df['accuracy'][1:].max()
        max_accuracy_xvalue = df[keyword].loc[df['accuracy'] == max_accuracy].values[0]

        axe.plot(max_accuracy_xvalue, max_accuracy, 'ro')
        axe.annotate('max at ' + str(max_accuracy_xvalue), (max_accuracy_xvalue, max_accuracy))


        axe.set_ylabel(label)
        axe.tick_params(axis='y', color=colors[2])

    ax2 = axe.twinx()
    ax3 = axe.twinx()

    # Plot features or thresholds
    if xlabel == 'Feature Penalty':
        ax2.plot(df[keyword], df['no_features'], 'o--', label="Features", color=colors[4], markersize=3)
        ax2.tick_params(axis='y', labelcolor=colors[4])
        ax2.axhline(df['no_features'].iloc[0], linestyle=':', label="Penalty = 0", color=colors[4])

    if xlabel == 'Threshold Penalty':
        ax2.tick_params(axis='y', labelcolor=colors[4])
        ax2.plot(df[keyword], df['no_thresholds'], 'o--', label="Values", color=colors[0], markersize=3)
        ax2.axhline(df['no_thresholds'].iloc[0], linestyle=':', label="Penalty = 0", color=colors[0])

    ax4 = ax2.twinx()
    ax4.plot(df[keyword], df['our_bits'], 'v--', label="Our Bits", color=colors[5], markersize=3)
    ax4.plot(df[keyword], df['lgb_bits'], '-.', label="naive Bits", color=colors[5], markersize=3)
    ax4.tick_params(axis='y', labelcolor=colors[5])

    handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
    handles_axe3, labels_axe3 = ax3.get_legend_handles_labels()
    handles_axe4, labels_axe4 = ax4.get_legend_handles_labels()
    handles_axe, labels_axe = axe.get_legend_handles_labels()

    # Combine the handles and labels
    merged_handles = handles_ax2 + handles_axe3 +handles_axe4 + handles_axe
    merged_labels = labels_ax2 + labels_axe3 + labels_axe4 + labels_axe
    return merged_handles, merged_labels

    #ax2.legend(loc='upper right')
def plot_memory_acc(df, axe, fig, big=False):
    keywords = ['accuracy1', 'accuracy4']
    norm = Normalize(vmin=0, vmax=len(keywords) - 1)
    colors = [viridis(norm(i)) for i in range(len(keywords))]
    width = 0.25  # the width of the bars
    multiplier = 0
    if big:
        memory_values = [16384, 32768]
    else:
        memory_values = [1024, 2048, 4096, 8192]

    tolerance = 40000
    # Create a new DataFrame to store the best accuracy rows
    best_rows_toad = pd.DataFrame()
    best_rows_native = pd.DataFrame()

    for target in memory_values:
        subset = df[(df['our_bits'] <= target) & (df['our_bits'] >= target - tolerance)]
        if not subset.empty:
            best_row = subset.loc[subset['accuracy'].idxmax()]  # Select the entire row
            best_rows_toad = pd.concat([best_rows_toad, best_row.to_frame().T], ignore_index=True)  # Append the row

    for target in memory_values:
        subset = df[(df['lgb_bits'] <= target) & (df['lgb_bits'] >= target - tolerance)]
        print(subset)
        if not subset.empty:
            best_row_n = subset.loc[subset['accuracy'].idxmax()]  # Select the entire row
            print("bestrow")
            print(best_row_n)
            best_rows_native = pd.concat([best_row_n, best_row_n.to_frame().T], ignore_index=True)  # Append the row

    print(best_rows_toad.head(20))
    print(best_rows_native.head(20))
    x = np.arange(len(best_rows_toad['our_bits']))
    myitems = {
        'Our_bits': (best_rows_toad['accuracy']),
        'native_bits': (best_rows_native['accuracy'])
    }
    for attribute, measurement in myitems.items():
        offset = width * multiplier
        rects = axe.bar(x + offset, measurement, width, label=attribute)
        #axe.bar_label(rects, padding=3)
        multiplier += 1

    axe.set_xticks(x + width)  # Position the ticks at the center of the grouped bars
    axe.set_xticklabels(memory_values)  # Apply the custom labels

    axe.legend()


datasets = ['Breastcancer', 'california_housing', 'kin8nm', 'kr-vs-kp', 'mushroom'] #  'california_housing', 'kin8nm', 'covtype' # todo covtype
binary = ['Breastcancer', 'kr-vs-kp', 'mushroom'] #  'california_housing', 'kin8nm', 'covtype' # todo covtype
regression = ['california_housing', 'kin8nm'] #  'california_housing', 'kin8nm', 'covtype' # todo covtype
plt.rcParams['image.cmap'] = 'viridis'
functions = ['simple']
vminour_bits, vmaxour_bits, vminour_accuracy, vmaxour_accuracy = 1000, 0 , 1000, 0
for function in functions:
    for data in datasets:
        df = pd.read_csv('../results/' + data + '/' + function + '_all.csv')
        data_tree_550_depth_3 = df[(df['max_trees'] == 500) & (df['depth'] == 3)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 500) & (df['depth'] == 3)]# & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        minbits = data_tree_550_depth_3_fptp_1000['our_bits'].min()
        vminour_bits, vmaxour_bits = min(minbits, vminour_bits), max(data_tree_550_depth_3_fptp_1000['our_bits'].max(), vmaxour_bits)
        vminour_accuracy, vmaxour_accuracy = min(data_tree_550_depth_3_fptp_1000['accuracy'].min(), vminour_accuracy), max(data_tree_550_depth_3_fptp_1000['accuracy'].max(), vmaxour_accuracy)
        norm = mcolors.Normalize(vmin=vminour_bits, vmax=vmaxour_bits)  # Normalize color range
        norm2 = mcolors.Normalize(vmin=vminour_accuracy, vmax=vmaxour_accuracy)  # Normalize color range
if (plotgrid):
    for function in functions:
        fig, axes = plt.subplots(2, 5, figsize=(5, 2), sharex=True, sharey=True)
        counter = 0
        for data in datasets:
            df = pd.read_csv('../results/' + data + '/' + function + '_all.csv')
            data_tree_550_depth_3 = df[(df['max_trees'] == 500) & (df['depth'] == 3)]
            data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 500) & (df['depth'] == 3)]# & (df['tinygbdt_penalty_feature'] < 4000) & (df['tinygbdt_penalty_split'] < 4000)]
            #graphs
            if (data in binary):
                if data == "Breastcancer":
                    axe=axes[0, counter].set_title("breastcancer" + "\n(binary)")
                else:
                    axe=axes[0, counter].set_title(data + "\n(binary)")
            if (data in regression):
                axe=axes[0, counter].set_title(data + "\n(regression)")
            grid_memory = plot_grid(data_tree_550_depth_3_fptp_1000, axe=axes[0, counter], fig=fig, column='our_bits', norm=norm, title='Memory usage with changing penalties')
            grid_accuracy = plot_grid(data_tree_550_depth_3_fptp_1000, axe=axes[1,counter], fig=fig, column='accuracy', norm=norm2, title='Accuracy with changing penalties')
            axes[1, counter].set_xlabel('Split Penalty')
            counter =counter+1

        cbar = fig.colorbar(grid_memory, ax=axes[0], orientation='vertical', location='right', shrink=0.9, pad=0.01)
        cbar2 = fig.colorbar(grid_accuracy, ax=axes[1], orientation='vertical', location='right', shrink=0.9, pad=0.01)
        def bits_to_kb(x, pos):
            return f"{x / 1000:.1f}"  # Divide by 1000 to convert to KB

        cbar.ax.yaxis.set_major_formatter(FuncFormatter(bits_to_kb))
        axes[0,0].set_ylabel('Feature Penalty')
        axes[1,0].set_ylabel('Feature Penalty')
        axes[0,4].yaxis.set_label_position("right")
        axes[1,4].yaxis.set_label_position("right")

        axes[0,4].set_ylabel('Memory (KB)', labelpad=50)
        axes[1,4].set_ylabel('Metric: Accuracy (binary)\n RMSE (regression))', labelpad=50)

        plt.savefig('../results/' + function + '.png', format='png', dpi=300)
        plt.show()

for function in functions:
    fig, axes = plt.subplots( 3, 5, figsize=(10, 8))
    counter = 0
    for data in datasets:
        df = pd.read_csv('../results/' + data + '/' + function + '_all.csv')
        data_tree_550_depth_3 = df[(df['max_trees'] == 500) & (df['depth'] == 3)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        data_tree_550_depth_3_fptp_1000 = df[(df['max_trees'] == 500) & (df['depth'] == 3) & (df['tinygbdt_penalty_feature'] < 1000) & (df['tinygbdt_penalty_split'] < 1000)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        if (data in binary):
            acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.85] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

        if (data in regression):
            acc_good_subset = data_tree_550_depth_3[data_tree_550_depth_3['accuracy'] > 0.4] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]

        acc_good_subset = acc_good_subset.sort_values(by='our_bits')
        data_tree_550_depth_3['tinygbdt_penalty_feature'] = pd.to_numeric(data_tree_550_depth_3['tinygbdt_penalty_feature'], errors='coerce')
        data_tree_550_depth_3_fptp_1000_fptp_1 = data_tree_550_depth_3_fptp_1000[(data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_feature'] > 0.1)& (data_tree_550_depth_3_fptp_1000['tinygbdt_penalty_split'] > 0.1)]
        data_criteria_split_1 = data_tree_550_depth_3_fptp_1000_fptp_1[(data_tree_550_depth_3_fptp_1000_fptp_1['tinygbdt_penalty_split'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        data_criteria_feature_1 = data_tree_550_depth_3_fptp_1000_fptp_1[(data_tree_550_depth_3_fptp_1000_fptp_1['tinygbdt_penalty_feature'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        data_criteria_split_1 = data_criteria_split_1.sort_values(by='tinygbdt_penalty_feature')
        data_criteria_feature_1 = data_criteria_feature_1.sort_values(by='tinygbdt_penalty_split')
        #graphs
        handles, labels = plotAccuracyByPenalty(data_criteria_split_1, axes[0,counter], 'tinygbdt_penalty_feature')
        handles2, labels2 = plotAccuracyByPenalty(data_criteria_feature_1, axes[1, counter], keyword='tinygbdt_penalty_split', xlabel='Threshold Penalty')
        print(data)
        if data == 'california_housing' or data == 'kin8nm':
            plot_memory_acc(df, axe=axes[2, counter], fig=fig, big=True)
        else:
            plot_memory_acc(df, axe=axes[2, counter], fig=fig, big=False)

        # Create a single legend for all subplots at the bottom
        fig.legend(handles, labels, loc='center', bbox_to_anchor=(0.60,0.9), ncol=2)
        fig.legend(handles2, labels2, loc='center', bbox_to_anchor=(0.85,0.9), ncol=2)
        counter = counter + 1

    axes[0,4].yaxis.set_label_position("right")
    axes[1,4].yaxis.set_label_position("right")

    plt.savefig('../results/' + function + 'lines.png', format='png', dpi=300)
    plt.show()