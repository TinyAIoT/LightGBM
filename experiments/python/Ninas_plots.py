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
def plotMetrics(df, log_scale=False, dataset=None, dont_plot=False, get_baseline=True):
    setting_value = df['tinygbdt_penalty_split']
    plt.ioff()
    fig1, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('tinygbdt_penalty_split')
    if log_scale:
    # 	ax2.set_yscale('log')
        ax1.set_xscale('log')
    if len(df['logloss']) > 0:
        if df['logloss'].iloc[-1] != 0:
            ax1.set_ylabel('Logloss')
            ax1.plot(setting_value, df['logloss'], color=color, label='Logloss')
    if len(df['rmse']) > 0:
        if df['rmse'].iloc[-1] != 0:
            ax1.set_ylabel('R2 Score')
            ax1.plot(setting_value, df['accuracy'], color=color, label='R2 Score')
    ax1.plot(setting_value, df['accuracy'], color='tab:purple', label='Accuracy/R2')
    plt.legend(loc='lower center')
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
    ax2.set_ylabel('count')
    ax2.plot(setting_value, df['no_thresholds'], label="no. thresholds")
    ax2.plot(setting_value, df['no_leaves'], label="no. leaves")
    plt.legend(loc='lower left')


    ax4 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
    ax4.yaxis.set_label_position("left")
    ax4.yaxis.tick_left()
    ax4.set_ylabel('bit count')
    ax4.plot(setting_value, df['our_bits'], color='tab:pink', label="no. bits")
    ax4.plot(setting_value, df['lgb_bits'], color='tab:brown', label="no. bits LGBM")
    plt.legend(loc='lower right')


    color = 'tab:green'
    ax3 = ax1.twinx()  # instantiate a third Axes that shares the same x-axis
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.plot(setting_value, df['no_features'], label="no. features", color=color)
    ax3.plot(setting_value, df['no_trees'], label="no. trees", color='tab:cyan')

    fig1.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.legend(loc='upper left')

    plt.savefig(
        '../plots/'
        +'_penF'+str(df['tinygbdt_penalty_feature'].iloc[-1])
        +'_penT'+str(df['tinygbdt_penalty_split'].iloc[-1])
        +'_maxdepth'+str(df['depth'].iloc[-1])
        +'_logscale'+str(log_scale)
        +'.png'
        )

    plt.show()

def plot_grid(df, title='Penalty Grid Search'):
    plt.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df['accuracy'], cmap='viridis',
                label='Accuracy')

    max_accuracy = df['accuracy'][1:].max()
    print(max_accuracy)

    # Find rows where 'accuracy' matches max_accuracy
    df_max_accuracy = df.loc[df['accuracy'] == max_accuracy]

    # Assuming there's a single row with max accuracy, extract the first element
    split_penalty = df_max_accuracy['tinygbdt_penalty_split'].iloc[0]
    feature_penalty = df_max_accuracy['tinygbdt_penalty_feature'].iloc[0]

    # Scatter and annotate the point with the max accuracy
    pcm = plt.scatter(split_penalty, feature_penalty, c='r', label='Max Accuracy')
    plt.annotate('Max Accuracy', (split_penalty, feature_penalty))

    print("Dataframe max accuracy")
    summary = df.describe()
    print(summary)

    plt.title(title)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Split Penalty')
    plt.ylabel('Feature Penalty')
    plt.colorbar()
    plt.legend()
    plt.show()
    plt.savefig('../plots/' + 'penalty_grid_.png')
    # plt.tight_layout()

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
subset = df[(df['no_trees'] == 16)]
print(subset.describe())
#plot_grid(subset, 'tinygbdt_penalty_split')
plotMetrics(subset)
