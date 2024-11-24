import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re
from matplotlib.cm import viridis
from matplotlib.colors import Normalize
import lightgbm as lgb
from pandas import read_csv
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score
# keyword is the substring of the filename to search for in model.txt and .out files
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
    ax3.plot(setting_value, df['lgb_bits'], color='tab:brown', label="no. bits LGBM")
    ax3.legend(loc='upper right')
    ax4 = axe.twinx()
    ax4.spines['right'].set_position(('outward', 120))  # Offset the spine
    ax4.set_ylabel('no. features/trees', color='tab:green')
    ax4.plot(setting_value, df['no_features'], label="no. features", color='tab:green')
    ax4.plot(setting_value, df['no_trees'], label="no. trees", color='tab:cyan')
    ax4.tick_params(axis='y', labelcolor='tab:green')
    ax4.legend(loc='lower right')

    # Tweak layout with tight_layout and return the figure (but no plt since using an existing axe)
    axe.figure.tight_layout()

def plot_grid(df, axe, fig, column='accuracy', title=''):

    scm = axe.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df[column], cmap='viridis',
                label=column)
    #if (column == 'accuracy'):
        # max_accuracy = df[column][1:].max()
        # df_max_accuracy = df.loc[df[column] == max_accuracy]
        # split_penalty = df_max_accuracy['tinygbdt_penalty_split'].iloc[0]
        # feature_penalty = df_max_accuracy['tinygbdt_penalty_feature'].iloc[0]
        # pcm = axe.scatter(split_penalty, feature_penalty, c='r', label='Max Accuracy')
        # axe.annotate('Max Accuracy', (split_penalty, feature_penalty))

    axe.set_xscale('log')
    axe.set_yscale('log')  # Correct method for setting y scale
    axe.set_ylabel('Feature Penalty')
    fig.colorbar(scm, ax=axe, orientation='vertical')


def plotAccuracyByPenalty(df, axe, keyword, plot_accuracy=True, plot_nodeLeafCount=False, xlog=True, xlabel='Feature Penalty'):
    # Determine which keyword to use based on xlabel
    keywords = ['accuracy1', 'accuracy2', 'accuracy3', 'accuracy4', 'accuracy4']
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

        axe.plot(df[keyword], df['accuracy'], '--o', label=label, color=colors[0])

        max_accuracy = df['accuracy'][1:].max()
        max_accuracy_xvalue = df[keyword].loc[df['accuracy'] == max_accuracy].values[0]

        axe.plot(max_accuracy_xvalue, max_accuracy, 'ro')
        #axe.annotate('max at ' + str(max_accuracy_xvalue), (max_accuracy_xvalue, max_accuracy))

        if xlabel == 'Threshold Penalty' or xlabel == 'Both penalties':
            axe.plot(df[keyword], ((df['no_leaves']*2-1)/df['no_thresholds']), 'o--', label="reuse factor", color=colors[1])


        axe.set_ylabel(label)
        axe.tick_params(axis='y', color=colors[0])
        #axe.legend(loc='lower left')

    # Add a twin axis for plotting other metrics
    ax2 = axe.twinx()
    ax2.set_ylabel('Count')

    # Plot features or thresholds
    if xlabel == 'Feature Penalty':
        ax2.plot(df[keyword], df['no_features'], 'o--', label="Features", color=colors[4])
        #ax2.axhline(df['no_features'][0], linestyle=':', label="Penalty = 0", color=colors[2])

    if xlabel == 'Threshold Penalty' or xlabel == 'Both penalties':
        ax2.plot(df[keyword], df['no_thresholds'], 'o--', label="# thresholds and leaf values", color=colors[4])
        #ax2.axhline(df['no_thresholds'][0], linestyle=':', label="Penalty = 0", color='tab:red')
        if plot_nodeLeafCount:
            ax2.plot(df[keyword], (df['no_leaves']*2-1), 'o--', label="# nodes and leaves", color='tab:grey')
    ax2.plot(df[keyword], df['our_bits'], 'o--', label="Our Bits", color=colors[2])
    ax2.plot(df[keyword], df['lgb_bits'], 'o--', label="LGB Bits", color=colors[3])

    #ax2.legend(loc='upper right')
def plot_memory_acc(subset, axe, fig):
    keywords = ['accuracy1', 'accuracy4']
    norm = Normalize(vmin=0, vmax=len(keywords) - 1)
    colors = [viridis(norm(i)) for i in range(len(keywords))]
    axe.plot(subset['our_bits'], subset['accuracy'],  label='TOD', color=colors[0], alpha=0.6)#, s=3)
    axe.plot(subset['lgb_bits'], subset['accuracy'], label='LGB', color=colors[1], alpha=0.6)#, s=3)
    axe.legend()


datasets = ['Breastcancer', 'california_housing', 'kin8nm', 'kr-vs-kp', 'mushroom'] #  'california_housing', 'kin8nm', 'covtype' # todo covtype
plt.rcParams['image.cmap'] = 'viridis'
functions = ['bit']

for function in functions:
    fig, axes = plt.subplots(5, 4, figsize=(10, 8))
    counter = 0
    for data in datasets:
        # collect data
        df = pd.read_csv('../results/' + data + '/' + function + '_all.csv')
        subset = df[(df['max_trees'] == 100) & (df['depth'] == 3)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        acc_good_subset = df[(df['max_trees'] == 100) & (df['depth'] == 3) & (df['tinygbdt_penalty_feature'] < 1000)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        acc_good_subset = acc_good_subset.sort_values(by='our_bits')
        sm_subset = subset[(subset['tinygbdt_penalty_split'] == 1) & (subset['tinygbdt_penalty_feature'] < 1000) & (subset['tinygbdt_penalty_feature'] > 0.1)& (subset['tinygbdt_penalty_split'] < 1000)& (subset['tinygbdt_penalty_split'] > 0.1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        sm_subset = sm_subset.sort_values(by='tinygbdt_penalty_feature')
        print(acc_good_subset)
        #graphs
        plot_grid(subset, axe=axes[counter, 0], fig=fig, column='accuracy', title='Accuracy with changing penalties')
        plotAccuracyByPenalty(sm_subset, axes[counter, 1], 'tinygbdt_penalty_feature')
        plot_grid(subset, axe=axes[counter, 2], fig=fig, column='our_bits', title='Memory usage with changing penalties')
        plot_memory_acc(acc_good_subset, axe=axes[counter, 3], fig=fig)

        counter = counter + 1

    axes[3,0].set_xlabel('Split Penalty')
    axes[3,1].set_xlabel('Split Penalty')
    plt.savefig('../results/' + function + '.png', format='png', dpi=300)
    plt.show()
