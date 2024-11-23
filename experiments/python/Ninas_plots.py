import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re

import lightgbm as lgb
from pandas import read_csv
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score

def plotAccuracyByPenalty(df, keyword, plot_accuracy=True, plot_nodeLeafCount=False, xlog=True, xlabel='penalty'):

    # plt.title(keyword)

    fig1, ax1 = plt.subplots()

    if xlabel == 'Feature Penalty' or xlabel == 'Both penalties':
        keyword = 'tinygbdt_penalty_feature'
    if xlabel == 'Threshold Penalty':
        keyword = 'tinygbdt_penalty_split'

    # color = 'tab:red'
    ax1.set_xlabel(xlabel)
    if xlog:
        ax1.set_xscale('log')

    if plot_accuracy:
        color='tab:orange'
        if df['logloss'].iloc[1] == 0.0:
            label='R2 Score'
        else:
            label='Accuracy'
        ax1.plot(df[keyword], df['accuracy'], '--o', color=color, label=label)
        max_accuracy = df['accuracy'][1:].max()
        max_accuracy_xvalue = df[keyword].loc[df['accuracy'] == max_accuracy].values[0]
        print(max_accuracy_xvalue)
        ax1.plot(max_accuracy_xvalue, max_accuracy, 'ro')
        ax1.annotate('max at '+ str(max_accuracy_xvalue), (max_accuracy_xvalue, max_accuracy))
        locs, labels = plt.xticks()
        if xlabel == 'Threshold Penalty' or xlabel == 'Both penalties':
            ax1.plot(df[keyword], ((df['no_leaves']*2-1)/df['no_thresholds']), 'o--', label="reuse factor", color='tab:green')

        ax1.set_ylabel(label)
        ax1.tick_params(axis='y', labelcolor=color)
        plt.legend(loc='lower left')
    # ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
    ax2.set_ylabel('Count')

    if xlabel == 'Feature Penalty':
        color = 'tab:green'
        ax2.plot(df[keyword], df['no_features'], 'o--', label="Features", color=color)
        ax2.axhline(df['no_features'][0], linestyle=':', label="Penalty = 0", color='tab:red')
    if xlabel == 'Threshold Penalty' or xlabel == 'Both penalties':
        color = 'tab:blue'
        ax2.plot(df[keyword], df['no_thresholds'], 'o--', label="# thresholds and leaf values", color=color)
        ax2.axhline(df['no_thresholds'][0], linestyle=':', label="Penalty = 0", color='tab:red')
        if plot_nodeLeafCount:
            ax2.plot(df[keyword], (df['no_leaves']*2-1), 'o--', label="# nodes and leaves", color='tab:grey')

    plt.legend(loc='upper right')

    fig1.tight_layout()  # otherwise the right y-label is slightly clipped

    plt.savefig(
        '../plots/'+'AccBY.png'
        )

    plt.show()

df = pd.read_csv('../results/grid_binary_breastcancer_data.libsvm.train_penF8.0_penT8.0_maxtrees100.0_maxdepth7.0_maxsize64000.0_precision1.0_logscaleTrue.csv')
subset = df[(df['no_trees'] == 16) & (df['depth'] == 3)]
print(subset.describe())
plotAccuracyByPenalty(subset, 'tinygbdt_penalty_split')
