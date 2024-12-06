import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re
import argparse
import os
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
    key1_pattern = r'Bits Bool Thresholds:\s*(\d+)'
    key2_pattern = r'Bits float thresholds:\s*(\d+)'
    key3_pattern = r'Bits References inside Trees:\s*(\d+)'
    key4_pattern = r'Bits Feature Threshold mapping:\s*(\d+)'
    key5_pattern = r'Bits Feature float leaves:\s*(\d+)'

    with open(filename, "r") as input:
        ret1 = 0.0
        ret2 = 0.0
        ret3 = 0.0
        ret4 = 0.0
        ret5 = 0.0

        for line in input:
            match1 = re.search(key1_pattern, line)
            match2 = re.search(key2_pattern, line)
            match3 = re.search(key3_pattern, line)
            match4 = re.search(key4_pattern, line)
            match5 = re.search(key5_pattern, line)

            if match1:
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
def extract_key(filename):
    # Use regular expressions to find the numbers after specific prefixes
    match_datams = re.search(r'datams-(\d+)', filename)
    match_fp = re.search(r'fp-([0-9.]+)', filename)
    match_tp = re.search(r'tp-([0-9.]+)', filename)
    match_tree = re.search(r'tree-(\d+)', filename)
    match_depth = re.search(r'depth-(\d+)', filename)

    # Extract the numbers, using 0 if the pattern isn't found
    datams = int(match_datams.group(1)) if match_datams else 0
    fp = float(match_fp.group(1)) if match_fp else 0.0
    tp = float(match_tp.group(1)) if match_tp else 0.0
    tree = int(match_tree.group(1)) if match_tree else 0
    depth = int(match_depth.group(1)) if match_depth else 0

    # Create a tuple for sorting
    return (datams, fp, tp, tree, depth)

# keyword is the substring of the filename to search for in model.txt and .out files
def plotMetrics(keyword, df_key='', log_scale=False, dataset=None, dont_plot=True, get_baseline=True, directory=''):
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
    sorted_dir = sorted(os.listdir(os.path.join("..", "models", directory)), key=extract_key)#, float("0."+x.split(".")[2])))
    setting_value = []
    accuracies = []
    logloss = []
    rmse = []
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
    tinygbdt_forestsize = 0
    num_classes = 0
    objective = ""
    data = ""

    if df_key=='':
        df_key = ''

    for fn in sorted_dir:
        filepath = os.path.join("..", "models", directory, fn)
        if fn.endswith(".out") or (get_baseline and fn.endswith("baseline.out")):
            logloss.append(GetValueFromOut(filepath, 'logloss'))
            rmse.append(GetValueFromOut(filepath, 'rmse'))
            no_features.append(GetValueFromOut(filepath, '#features'))
            no_thresholds.append(GetValueFromOut(filepath, '#thresholds'))
            our_bits.append(GetValueFromOutBits(filepath))
        if fn.endswith(".txt") or (get_baseline and fn.endswith("baseline.txt")):
            no_trees.append(GetValueFromTXT(filepath, 'Tree')+1)
            setting_value.append(GetValueFromTXT(filepath, keyword))
            no_leaves.append(GetValueFromTXT(filepath, 'num_leaves', sum_up=True))
            lgb_bits.append(GetValueFromTXT(filepath, 'model_size', sum_up=True))
            num_iterations = GetValueFromTXT(filepath, 'num_iterations')
            max_depth =  GetValueFromTXT(filepath, 'max_depth')
            tinygbdt_penalty_feature.append(GetValueFromTXT(filepath, 'tinygbdt_penalty_feature'))
            tinygbdt_penalty_split.append(GetValueFromTXT(filepath, 'tinygbdt_penalty_split'))
            tinygbdt_forestsize =  GetValueFromTXT(filepath, 'tinygbdt_forestsize')
            num_classes =  GetValueFromTXT(filepath, 'num_class')
            valid_data = GetValueFromTXT(filepath, 'valid')
            label_column = GetValueFromTXT(filepath, 'label_column')
            objective =  GetValueFromTXT(filepath, 'objective')
            if objective == 'multiclass':
                accuracy, roc = calcAccuracy(filepath, '../'+valid_data, classes=num_classes)
            elif objective == 'binary':
                accuracy, roc = calcAccuracy(filepath, '../'+valid_data, classes=num_classes)
            elif objective == 'regression':
                rmse_py, accuracy = calcAccuracy(filepath, '../'+valid_data, classes=0, label_column=label_column)
            accuracies.append(accuracy)
            data = GetValueFromTXT(filepath, 'data')
        else:
            continue


    df = pd.DataFrame({
        'no_trees': no_trees,
        'max_trees': num_iterations,
        'max_depth': max_depth,
        'no_features': no_features,
        'no_thresholds': no_thresholds,
        'no_leaves': no_leaves,
        'our_bits': our_bits,
        'lgb_bits': lgb_bits,
        'accuracy': accuracies,
        'tinygbdt_penalty_feature': tinygbdt_penalty_feature,
        'tinygbdt_penalty_split': tinygbdt_penalty_split
    })

    df_filename = (keyword
                   +'_'+str(objective)
                   +'_'+str(data[5:])
                    +'_penF'+str(tinygbdt_penalty_feature[-1])
                    +'_penT'+str(tinygbdt_penalty_split[-1])
                   +'_maxtrees'+str(num_iterations)
                   +'_maxdepth'+str(max_depth)
                   + '_maxsize'+str(tinygbdt_forestsize)
                   +'_logscale'+str(log_scale)
                   +'.csv')
    
    res_dir = os.path.join("..", "results", directory)
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)  
    df.to_csv(os.path.join(res_dir, df_filename), index=False)
    df.to_csv(os.path.join(res_dir, 'last.csv'), index=False)

 
parser = argparse.ArgumentParser(description="Name of the dataset")
parser.add_argument('string_arg', type=str, help='the datasetname')
args = parser.parse_args()

# You can access the arguments using args.string_arg and args.directory
print(f"String argument: {args.string_arg}")

df_path = plotMetrics('grid', df_key='tinygbdt_penalty_split', log_scale = True, directory=args.string_arg)

