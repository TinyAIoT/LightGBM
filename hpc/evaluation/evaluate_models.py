import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import re
import argparse
import os
import lightgbm as lgb
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, r2_score, root_mean_squared_error

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
        accuracy = root_mean_squared_error(test_data.get_label(), y_pred)
    elif classes > 1:
        other = roc_auc_score(test_data.get_label(), y_pred, multi_class='ovo')
        accuracy = accuracy_score(test_data.get_label(), np.argmax(y_pred, axis=1))
    else:
        other = roc_auc_score(test_data.get_label(), y_pred)
        accuracy = accuracy_score(test_data.get_label(), (y_pred > 0.5).astype(int))

    if classes == 0: # regression
        otherval = r2_score(y_pred_val.get_label(), y_pred)
        accuracyval = root_mean_squared_error(y_pred_val.get_label(), y_pred)
    elif classes > 1:
        otherval = roc_auc_score(y_pred_val.get_label(), y_pred, multi_class='ovo')
        accuracyval = accuracy_score(y_pred_val.get_label(), np.argmax(y_pred, axis=1))
    else:
        otherval = roc_auc_score(y_pred_val.get_label(), y_pred)
        accuracyval = accuracy_score(y_pred_val.get_label(), (y_pred > 0.5).astype(int))


    return accuracy, accuracyval, other, otherval

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
def evaluateModel(filename, resultfile):

    if not os.path.exists(resultfile):
        with open(resultfile, "w") as f:
            f.write(f"no_trees,max_trees,max_depth,no_features,no_thresholds,no_leaves,our_bits,lgb_bits,accuracy,tinygbdt_penalty_feature,tinygbdt_penalty_split,tinygbdt_forestsize\n")
    
    filepath = (filename + ".txt")
    no_trees = GetValueFromTXT(filepath, 'Tree')+1
    num_iterations = GetValueFromTXT(filepath, 'num_iterations')
    max_depth = GetValueFromTXT(filepath, 'max_depth')
    no_leaves = GetValueFromTXT(filepath, 'num_leaves', sum_up=True)
    lgb_bits = GetValueFromTXT(filepath, 'model_size', sum_up=True)
    objective = GetValueFromTXT(filepath, 'objective')
    num_classes = GetValueFromTXT(filepath, 'num_class')
    tinygbdt_forestsize = GetValueFromTXT(filepath, 'tinygbdt_forestsize')
    tinygbdt_penalty_feature = GetValueFromTXT(filepath, 'tinygbdt_penalty_feature')
    tinygbdt_penalty_split = GetValueFromTXT(filepath, 'tinygbdt_penalty_split')
    valid_data = GetValueFromTXT(filepath, 'valid')
    out = 'val'.join(valid_data.rsplit('test', 1))
    if objective == 'multiclass':
        accuracy, val_acc, roc, val_oth = calcAccuracy(filepath, valid_data, out, classes=num_classes)
    elif objective == 'binary':
        accuracy, val_acc, roc, val_oth = calcAccuracy(filepath, valid_data, out, classes=num_classes)
    elif objective == 'regression':
        rmse_py, val_rmse, accuracy, val_acc = calcAccuracy(filepath, valid_data, out, classes=0)

    filepath = (filename + ".out")
    our_bits = GetValueFromOutBits(filepath)
    no_features = GetValueFromOut(filepath, '#features')
    no_thresholds = GetValueFromOut(filepath, '#thresholds')

    with open(resultfile, "a") as f:
        f.write(f"{no_trees},{num_iterations},{max_depth},{no_features},{no_thresholds},{no_leaves},{our_bits},{lgb_bits},{accuracy},{val_acc},{tinygbdt_penalty_feature},{tinygbdt_penalty_split},{tinygbdt_forestsize}\n")


parser = argparse.ArgumentParser(description='Evaluate LightGBM models and logged results.')
parser.add_argument('--filename', required=True, type=str, help='Path to the model file without extension')
parser.add_argument('--resultfile', required=True, type=str, help='Path to the result file to append results to')
args = parser.parse_args()

# You can access the arguments using args.string_arg and args.directory
# print(f"String argument: {args}")

df_path = evaluateModel(filename=args.filename, resultfile=args.resultfile)
