import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re

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

def plot_grid(df, axe, fig, title='Penalty Grid Search'):

    scm = axe.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df['accuracy'], cmap='viridis',
                label='Accuracy')
    max_accuracy = df['accuracy'][1:].max()
    df_max_accuracy = df.loc[df['accuracy'] == max_accuracy]

    # Assuming there's a single row with max accuracy, extract the first element
    split_penalty = df_max_accuracy['tinygbdt_penalty_split'].iloc[0]
    feature_penalty = df_max_accuracy['tinygbdt_penalty_feature'].iloc[0]

    # Scatter and annotate the point with the max accuracy
    pcm = plt.scatter(split_penalty, feature_penalty, c='r', label='Max Accuracy')
    axe.annotate('Max Accuracy', (split_penalty, feature_penalty))
    axe.set_title(title)
    axe.set_xscale('log')
    axe.set_yscale('log')  # Correct method for setting y scale
    axe.set_xlabel('Split Penalty')
    axe.set_ylabel('Feature Penalty')

    # axe.colorbar()
    fig.colorbar(scm, ax=axe, orientation='vertical')
    axe.legend()


def plotAccuracyByPenalty(df, axe, keyword, plot_accuracy=True, plot_nodeLeafCount=False, xlog=True, xlabel='Threshold Penalty'):
    # Determine which keyword to use based on xlabel
    if xlabel == 'Feature Penalty' or xlabel == 'Both penalties':
        keyword = 'tinygbdt_penalty_feature'
    if xlabel == 'Threshold Penalty':
        keyword = 'tinygbdt_penalty_split'

    axe.set_xlabel(xlabel)

    if xlog:
        axe.set_xscale('log')

    # Plot accuracy or R2 score
    if plot_accuracy:
        color = 'tab:orange'
        if df['logloss'].iloc[1] == 0.0:
            label = 'R2 Score'
        else:
            label = 'Accuracy'

        axe.plot(df[keyword], df['accuracy'], '--o', color=color, label=label)
        max_accuracy = df['accuracy'][1:].max()
        max_accuracy_xvalue = df[keyword].loc[df['accuracy'] == max_accuracy].values[0]

        # Highlight the maximum point
        print(max_accuracy_xvalue)
        axe.plot(max_accuracy_xvalue, max_accuracy, 'ro')
        axe.annotate('max at ' + str(max_accuracy_xvalue), (max_accuracy_xvalue, max_accuracy))

        if xlabel == 'Threshold Penalty' or xlabel == 'Both penalties':
            axe.plot(df[keyword], ((df['no_leaves']*2-1)/df['no_thresholds']), 'o--', label="reuse factor", color='tab:green')

        axe.set_ylabel(label, color=color)
        axe.tick_params(axis='y', labelcolor=color)
        axe.legend(loc='lower left')

    # Add a twin axis for plotting other metrics
    ax2 = axe.twinx()
    ax2.set_ylabel('Count')

    # Plot features or thresholds
    if xlabel == 'Feature Penalty':
        ax2.plot(df[keyword], df['no_features'], 'o--', label="Features", color=color)
        ax2.axhline(df['no_features'][0], linestyle=':', label="Penalty = 0", color='tab:red')

    if xlabel == 'Threshold Penalty' or xlabel == 'Both penalties':
        ax2.plot(df[keyword], df['no_thresholds'], 'o--', label="# thresholds and leaf values", color=color)
        #ax2.axhline(df['no_thresholds'][0], linestyle=':', label="Penalty = 0", color='tab:red')
        if plot_nodeLeafCount:
            ax2.plot(df[keyword], (df['no_leaves']*2-1), 'o--', label="# nodes and leaves", color='tab:grey')

    ax2.legend(loc='upper right')

    axe.figure.tight_layout()  # Ensure layout adjustments

datasets = ['Breastcancer', 'california_housing', 'kin8nm', 'kr-vs-kp', 'mushroom'] # 'Breastcancer', 'california_housing', 'kr-vs-kp', 'kin8nm' # todo covtype
plt.rcParams['image.cmap'] = 'viridis'
functions = ['simple', 'bits']
fig, axes = plt.subplots(2, 5, figsize=(10, 8))
counter = 0

for function in functions:
    for data in datasets:
        df = pd.read_csv('../results/' + data + '/' + function + '_all.csv')
        subset = df[(df['max_trees'] == 10000) & (df['depth'] == 3)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        sm_subset = df[(df['max_trees'] == 10000) & (df['depth'] == 3) & (df['tinygbdt_penalty_feature'] == 1)] # & (df['no_trees'] > 15) & (df['no_trees'] < 20)]
        sm_subset = sm_subset.sort_values(by='tinygbdt_penalty_split')
        print(data)
        print(subset.describe())
        plot_grid(subset, axe=axes[0, counter], fig=fig)
        #plotMetrics(sm_subset, axe=axes[1, counter])
        plotAccuracyByPenalty(sm_subset, axes[1, counter], 'tinygbdt_penalty_split' )
        counter = counter + 1
    plt.savefig('results/' + function + ' .png', format='png', dpi=300)
    plt.show()
