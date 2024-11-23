import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re

import lightgbm as lgb
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score

def GetValueFromOut(filename, key):
    input = open(filename, "r")
    ret = 0.0
    for line in input.readlines():
        if key + ' :' in line:
            ret = float(line.split(key+' :')[-1])
    return ret

def GetValueFromOutBits(filename):
    key1_pattern = r'Bits Bool Thresholds: \d+ ->'
    key2_pattern = r'Bits float thresholds: \d+ ->'
    key3_pattern = r'Bits References inside Trees: \d+ ->'
    key4_pattern = r'Bits Feature Threshold mapping: \d+ ->'
    key5_pattern = r'Bits Feature float leaves: \d+ ->'

    input = open(filename, "r")
    ret1 = 0.0
    ret2 = 0.0
    ret3 = 0.0
    ret4 = 0.0
    ret5 = 0.0
    for line in input.readlines():
        match1 = re.search(r'{} ([\d.]+)'.format(key1_pattern), line)
        match2 = re.search(r'{} ([\d.]+)'.format(key2_pattern), line)
        match3 = re.search(r'{} ([\d.]+)'.format(key3_pattern), line)
        match4 = re.search(r'{} ([\d.]+)'.format(key4_pattern), line)
        match5 = re.search(r'{} ([\d.]+)'.format(key5_pattern), line)

        if match1:
            print("Match found for key1!")
            ret1 = float(match1.group(1))
        if match2:
            ret2 = float(match2.group(1))
        if match3:
            ret3 = float(match3.group(1))
        if match4:
            ret4 = float(match4.group(1))
        if match5:
            ret5 = float(match5.group(1))
    return ret1 + ret2 + ret3 + ret4 + ret5

def GetValueFromTXT(filename, key, sum_up=False):
    input = open(filename, "r")
    ret = 0.0
    for line in input.readlines():
        if key + '=' in line:
            if key == 'objective':
                ret = line.split(key+'=')[-1]
            elif sum_up:
                ret += float(line.split(key+'=')[-1])
            else:
                ret = float(line.split(key+'=')[-1])
        elif key + ': ' in line and key != 'num_leaves':
            try:
                ret = float(line.split(key+': ')[-1][:-2])
            except:
                ret = line.split(key+': ')[-1][:-2]
    return ret

def calcAccuracy(model_path, data_path, classes=1, label_column=None):
    model = lgb.Booster(model_file=model_path)

    if data_path.endswith('.csv'):
        df = pd.read_csv(data_path, header=None)
        test_data = lgb.Dataset(df.iloc[:,:int(label_column)], label=df.iloc[:,int(label_column)], free_raw_data=False)
    else:
        test_data = lgb.Dataset(data_path, free_raw_data=False)
    test_data.construct()

    y_pred = model.predict(test_data.get_data(), predict_disable_shape_check=True)


    if classes == 0: # regression
        other = r2_score(test_data.get_label(), y_pred)
        accuracy = mean_squared_error(test_data.get_label(), y_pred)
    elif classes > 1:
        other = roc_auc_score(test_data.get_label(), y_pred, multi_class='ovo')
        accuracy = accuracy_score(test_data.get_label(), np.argmax(y_pred, axis=1))
    else:
        other = roc_auc_score(test_data.get_label(), y_pred)
        accuracy = accuracy_score(test_data.get_label(), (y_pred > 0.5).astype(int))

    return accuracy, other

# keyword is the substring of the filename to search for in model.txt and .out files
def plotMetrics(keyword, df_key='', log_scale=False, dataset=None, dont_plot=False, get_baseline=True):
    """Evaluates the model files that end with the specified keyword in the filename and plots various metrics.
    keyword : str
        The keyword to identify the model files.
    df_key : str, optional
        The key to plot on the x-axis; mostly either 'tinygbdt_penalty_split' or 'tinygbdt_penalty_feature'.
    log_scale : bool, optional
        Whether to use a logarithmic scale for the plots (default is False).
    dataset : str, optional
        The dataset to use (default is None).
        Currently not in use. Test dataset is received from the model file.
    dont_plot : bool, optional
        If True, the function will not generate plots (default is False).
    get_baseline : bool, optional
        If True, baseline models will also be evaluated (default is True).
    Returns
    -------
    str
        The filename of the saved DataFrame in CSV format.
    """
    sorted_dir = (os.listdir("../Modeltest"))#, float("0."+x.split(".")[2])))
    setting_value = []
    accuracies = []
    logloss = []
    rmse = []
    r2 = []
    no_features = []
    no_thresholds = []
    no_leaves = []
    no_trees = []
    our_bits = []
    lgb_bits = []
    tinygbdt_penalty_feature = []
    tinygbdt_penalty_split = []
    num_iterations = 0
    max_depth = 0
    # tinygbdt_penalty_feature = 0
    # tinygbdt_penalty_split = 0
    tinygbdt_forestsize = 0
    tinygbdt_precision = 0
    num_classes = 0
    objective = ""
    data = ""

    if df_key=='':
        df_key = ''

    for fn in sorted_dir:
        if fn.endswith(".out") or (get_baseline and fn.endswith("baseline.out")):
            logloss.append(GetValueFromOut('../Modeltest/'+fn, 'logloss'))
            rmse.append(GetValueFromOut('../Modeltest/'+fn, 'rmse'))
            no_features.append(GetValueFromOut('../Modeltest/'+fn, '#features'))
            no_thresholds.append(GetValueFromOut('../Modeltest/'+fn, '#thresholds'))
            our_bits.append(GetValueFromOutBits('../Modeltest/'+fn))
        if fn.endswith(".txt") or (get_baseline and fn.endswith("baseline.txt")):
            no_trees.append(GetValueFromTXT('../Modeltest/'+fn, 'Tree'))
            setting_value.append(GetValueFromTXT('../Modeltest/'+fn, keyword))
            no_leaves.append(GetValueFromTXT('../Modeltest/'+fn, 'num_leaves', sum_up=True))
            lgb_bits.append(GetValueFromTXT('../Modeltest/'+fn, 'model_size', sum_up=True))
            num_iterations = GetValueFromTXT('../Modeltest/'+fn, 'num_iterations')
            max_depth =  GetValueFromTXT('../Modeltest/'+fn, 'max_depth')
            tinygbdt_penalty_feature.append(GetValueFromTXT('../Modeltest/'+fn, 'tinygbdt_penalty_feature'))
            tinygbdt_penalty_split.append(GetValueFromTXT('../Modeltest/'+fn, 'tinygbdt_penalty_split'))
            tinygbdt_forestsize =  GetValueFromTXT('../Modeltest/'+fn, 'tinygbdt_forestsize')
            tinygbdt_precision =  GetValueFromTXT('../Modeltest/'+fn, 'tinygbdt_precision')
            num_classes =  GetValueFromTXT('../Modeltest/'+fn, 'num_class')
            valid_data = GetValueFromTXT('../Modeltest/'+fn, 'valid')
            label_column = GetValueFromTXT('../Modeltest/'+fn, 'label_column')
            objective =  GetValueFromTXT('../Modeltest/'+fn, 'objective')
            if objective == 'multiclass':
                accuracy, roc = calcAccuracy('../Modeltest/'+fn, '../'+valid_data, classes=num_classes)
            elif objective == 'binary':
                accuracy, roc = calcAccuracy('../Modeltest/'+fn, '../'+valid_data, classes=num_classes)
            elif objective == 'regression':
                rmse_py, accuracy = calcAccuracy('../Modeltest/'+fn, '../'+valid_data, classes=0, label_column=label_column)
            accuracies.append(accuracy)
            data = GetValueFromTXT('../Modeltest/'+fn, 'data')
        else:
            continue

    # lbg_bits = lgb_floats*32 + lgb_ints*16
    # print(len(setting_value), len(no_trees), len(no_features), len(no_thresholds), len(no_leaves), len(our_bits), len(lgb_bits), len(logloss), len(rmse), len(accuracies))
    print(no_trees)
    length = len(no_trees)
    if len(no_leaves) != length:
        print(no_leaves)
        print("noleaves")

    if len(our_bits) != length:
        print(our_bits)
        print("ourbits")

    if len(lgb_bits) != length:
        print(lgb_bits)
        print("lgb_bits")

    if len(logloss) != length:
        print(logloss)
        print("logloss")
    if len(rmse) != length:
        print(rmse)
        print("rmse")
    if len(accuracies) != length:
        print(accuracies)
        print("accuracies")
    if len(no_features) != length:
        print(no_features)
        print("no_features")
    if len(no_thresholds) != length:
        print(no_thresholds)
        print("no_thresholds")
    if len(tinygbdt_penalty_feature) != length:
        print(tinygbdt_penalty_feature)
        print("tinygbdt_penalty_feature")

    df = pd.DataFrame({
        # keyword: setting_value,
        'no_trees': no_trees,
        'no_features': no_features,
        'no_thresholds': no_thresholds,
        'no_leaves': no_leaves,
        'our_bits': our_bits,
        'lgb_bits': lgb_bits,
        'logloss': logloss,
        'rmse': rmse,
        'accuracy': accuracies,
        'tinygbdt_penalty_feature': tinygbdt_penalty_feature,
        'tinygbdt_penalty_split': tinygbdt_penalty_split
    })

    df_filename = (keyword
                   +'_'+str(objective)
                   +'_'+str(data[5:])
                    +'_penF'+str(tinygbdt_penalty_split[-1])
                    +'_penT'+str(tinygbdt_penalty_split[-1])
                   +'_maxtrees'+str(num_iterations)
                   +'_maxdepth'+str(max_depth)
                   + '_maxsize'+str(tinygbdt_forestsize)
                   +'_precision'+str(tinygbdt_precision)
                   +'_logscale'+str(log_scale)
                   +'.csv')

    df.to_csv('../results/'+
        df_filename
        , index=False
        )

    if not dont_plot:

        setting_value = df[df_key]

        plt.ioff()

        fig1, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel(df_key)
        if log_scale:
        # 	ax2.set_yscale('log')
            ax1.set_xscale('log')
        if len(logloss) > 0:
            if logloss[-1] != 0:
                ax1.set_ylabel('Logloss')
                ax1.plot(setting_value, logloss, color=color, label='Logloss')
        if len(rmse) > 0:
            if rmse[-1] != 0:
                ax1.set_ylabel('R2 Score')
                ax1.plot(setting_value, accuracies, color=color, label='R2 Score')
        ax1.plot(setting_value, accuracies, color='tab:purple', label='Accuracy/R2')
        plt.legend(loc='lower center')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis


        ax2.set_ylabel('count')  # we already handled the x-label with ax1
        # if log_scale:
        # 	ax2.set_yscale('log')
        # ax2.set_yscale('log')
        ax2.plot(setting_value, no_thresholds, label="no. thresholds")
        ax2.plot(setting_value, no_leaves, label="no. leaves")
        plt.legend(loc='lower left')


        ax4 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis
        ax4.yaxis.set_label_position("left")
        ax4.yaxis.tick_left()
        ax4.set_ylabel('bit count')
        ax4.plot(setting_value, our_bits, color='tab:pink', label="no. bits")
        ax4.plot(setting_value, lgb_bits, color='tab:brown', label="no. bits LGBM")
        plt.legend(loc='lower right')


        color = 'tab:green'
        ax3 = ax1.twinx()  # instantiate a third Axes that shares the same x-axis
        ax3.tick_params(axis='y', labelcolor=color)
        ax3.plot(setting_value, no_features, label="no. features", color=color)
        ax3.plot(setting_value, no_trees, label="no. trees", color='tab:cyan')

        fig1.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.legend(loc='upper left')

        plt.savefig(
            '../plots/'+keyword
            +'_'+str(data[5:])
            +'_penF'+str(tinygbdt_penalty_feature)
            +'_penT'+str(tinygbdt_penalty_split)
            +'_maxtrees'+str(num_iterations)
            +'_maxdepth'+str(max_depth)
            + '_maxsize'+str(tinygbdt_forestsize)
            +'_precision'+str(tinygbdt_precision)
            +'_logscale'+str(log_scale)
            +'.png'
            )

        plt.show()

    return df_filename

log_scale = False

# TODO: value at x=0 goes to -inf because of log scale
def plotAccuracyByPenalty(dataframe_filename, keyword, plot_accuracy=True, plot_nodeLeafCount=False, xlog=True, xlabel='penalty'):
    """
    Plots accuracy and other metrics against a specified penalty from a given CSV file.
    Parameters:
    dataframe_filename (str): The filename of the CSV file containing the data.
    keyword (str): The keyword to filter the data.
    plot_accuracy (bool, optional): Whether to plot accuracy. Defaults to True.
    plot_nodeLeafCount (bool, optional): Whether to plot node and leaf count. Defaults to False.
    xlog (bool, optional): Whether to use a logarithmic scale for the x-axis. Defaults to True.
    xlabel (str, optional): The label for the x-axis. Defaults to 'penalty'.
    Returns:
    None
    """
    df = pd.read_csv('../results/'+dataframe_filename)

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
        '../plots/'+'AccBY'+dataframe_filename[:-4]+'.png'
        )

    plt.show()

def plot_memories():
    """
    ! Pay attention that the correct models are in the models directory !
    Plots the accuracy of different models against memory usage.
    This function reads the accuracy data of three models from CSV files and plots their accuracy
    against different memory sizes. The models compared are:
    - Default LightGBM
    - ToD Compression
    - ToD Compression with Penalty
    The memory sizes considered are 1KB, 8KB, and 32KB.
    The plot is saved as a PNG file in the '../plots/' directory with a filename that includes the
    memory sizes.
    Returns:
        None
    """
    lgbm_df_path = plotMetrics('num_iterations', dont_plot=True)
    tinygbdt_df_path = plotMetrics('0.tinygbdt_forestsize', dont_plot=True)
    tinygbdt_penalty_df_path = plotMetrics('penalties.1.tinygbdt_forestsize', dont_plot=True)

    lgbm_df = pd.read_csv('../results/'+lgbm_df_path)
    tinygbdt_df = pd.read_csv('../results/'+tinygbdt_df_path)
    tinygbdt_penalty_df = pd.read_csv('../results/'+tinygbdt_penalty_df_path)

    x = ["1KB", "8KB", "32KB"]
    # create an index for each tick position
    xi = list(range(len(x)))
    # TODO: make baseline model evaluation plotMetrics() parameter instead of starting at value 1
    plt.plot(xi, lgbm_df['accuracy'][1:], marker='o', linestyle='--', color='r', label='Default LightGBM')
    plt.plot(xi, tinygbdt_df['accuracy'][1:], marker='o', linestyle='--', color='b', label='ToD Compression')
    plt.plot(xi, tinygbdt_penalty_df['accuracy'][1:], marker='o', linestyle='--', color='g', label='ToD Compression with Penalty')
    plt.xlabel('Memory')
    plt.ylabel('Accuracy')
    plt.xticks(xi, x)
    plt.legend()
    plt.savefig(
        '../plots/'+'modeltypes_bymemory_'+x[0]+x[1]+x[2]+'.png'
        )
    # plt.tight_layout()
    plt.show()

def plot_grid(df_grid_path, title='Penalty Grid Search'):
    df = pd.read_csv('../results/'+df_grid_path)
    plt.scatter(df['tinygbdt_penalty_split'], df['tinygbdt_penalty_feature'], c=df['accuracy'], cmap='viridis', label='Accuracy')
    max_accuracy = df['accuracy'][1:].max()
    df_max_accuracy = df.loc[df['accuracy'] == max_accuracy]
    pcm = plt.scatter(df_max_accuracy['tinygbdt_penalty_split'], df_max_accuracy['tinygbdt_penalty_feature'], c='r', label='Max Accuracy')
    plt.annotate('Max Accuracy', (df_max_accuracy['tinygbdt_penalty_split'], df_max_accuracy['tinygbdt_penalty_feature']))
    print("Dataframe max accuracy")
    print(df_max_accuracy)
    plt.title(title)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Split Penalty')
    plt.ylabel('Feature Penalty')
    plt.colorbar()
    plt.show()
    plt.savefig(
        '../plots/'+'penalty_grid_.png'
        )
    # plt.tight_layout()


"""
Experiment 3
"""
# plot_memories()

"""
Experiment 1
"""
# fp_df_path = plotMetrics('tinygbdt_penalty_feature', log_scale = True)
# tp_df_path = plotMetrics('tinygbdt_penalty_split', log_scale = True)
# # both_df_path = plotMetrics('bothpenalties', df_key='tinygbdt_penalty_split', log_scale = True)
# plotAccuracyByPenalty(fp_df_path, 'tinygbdt_penalty_feature', xlog=True, xlabel='Feature Penalty', plot_nodeLeafCount=plot_nodeLeafCount)
# plotAccuracyByPenalty(tp_df_path, 'tinygbdt_penalty_split', xlog=True, xlabel='Threshold Penalty', plot_nodeLeafCount=plot_nodeLeafCount)
# # plotAccuracyByPenalty(both_df_path, 'bothpenalties', xlog=True, xlabel='Both penalties', plot_nodeLeafCount=plot_nodeLeafCount)

"""
Experiment 2
"""
fp_df_path = plotMetrics('grid', df_key='tinygbdt_penalty_split', log_scale = True)
# fp_df_path = 'grid_binary_covtype.libsvm.binary.train_penF8192.0_penT8192.0_maxtrees100000.0_maxdepth3.0_maxsize8000.0_precision4.0_logscaleTrue.csv'
plot_grid(fp_df_path, title='Penalty Grid Search, Covtype binary, 8KB Memory')


"""
Others
"""
plot_nodeLeafCount = False
# fp_df_path = 'tinygbdt_penalty_feature_binary_covtype.libsvm.binary.train_penF0.0_penT0.0_maxtrees100.0_maxdepth3.0_maxsize500000.0_precision4.0_logscaleTrue.csv'
# tp_df_path = 'tinygbdt_penalty_split_binary_covtype.libsvm.binary.train_penF1048580.0_penT1048580.0_maxtrees100.0_maxdepth3.0_maxsize500000.0_precision4.0_logscaleTrue.csv'
# df_path = 'bothpenalties_binary_covtype.libsvm.binary.train_penF32.0_penT32.0_maxtrees10000.0_maxdepth3.0_maxsize8000.0_precision4.0_logscaleTrue.csv'

"""
Maybe need to use these keyword for EXPERIMENT 3
"""
# plotMetrics('num_iterations', get_baseline=False)
# # plotMetrics('max_depth', log_scale = log_scale)
# plotMetrics('0.tinygbdt_forestsize', get_baseline=False)
# plotMetrics('1.tinygbdt_forestsize', get_baseline=False)

