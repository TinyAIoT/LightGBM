import pandas as pd
import numpy as np
import os
from pathlib import Path
from sklearn.datasets import load_svmlight_file
import itertools
# max_trees,max_depth, tinygbdt_penalty_feature,tinygbdt_penalty_split
datasets = ["breastcancer", "california_housing", "mushroom", "kin8nm", "kr-vs-kp", "covtype", "wine", "covtype_multi"]
def r2_from_mse(mse, var_y, n):
    """
    Convert a scalar MSE to R² using the unbiased variance formula.
    """
    # n/(n‑1) factor accounts for the ddof=1 variance
    return 1.0 - (n / (n - 1.0)) * (mse / var_y)
def get_variation(path):
    _, y_truee = load_svmlight_file(path)
    y_truee = np.asarray(y_truee, dtype=np.float64)

    nn = len(y_truee)
    var_yy = np.var(y_truee, ddof=1)
    return nn, var_yy

def fix_regression_data(tofix, regreesionsets):
    mask = (tofix["dataset"].isin(regreesionsets))
    group_cols = ["dataset"]
    for (dataset), sub_idx in tofix[mask].groupby(group_cols).groups.items():
        nval, varnval = get_variation(f"./data/{seed}/{dataset}.val")
        ntest, varntest = get_variation(f"./data/{seed}/{dataset}.test")

        column = 'test_accuracy'
        mse_vals = tofix.loc[sub_idx, "val_acc"].values.astype(np.float64)
        mse_vals_test = tofix.loc[sub_idx, column].values.astype(np.float64)

        r2_vals = r2_from_mse(mse_vals, varnval, nval)
        r2_test = r2_from_mse(mse_vals_test, varntest, ntest)

        tofix.loc[sub_idx, "mse_vals_val"] = mse_vals
        tofix.loc[sub_idx, "mse_vals_test"] = mse_vals_test
        tofix.loc[sub_idx, "val_acc"] = r2_vals
        tofix.loc[sub_idx, "test_accuracy"] = r2_test
        tofix.loc[sub_idx, "meankfold"] = r2_test
    return tofix

datasets_to_fix = {"kin8nm", "california_housing"}
classification_datasetstest = {'mushroom', 'covtype', 'wine', 'covtype_multi'}
classification_datasetskfold = {'breastcancer', 'kr-vs-kp'}
models = ['rf', 'rf_guo', 'lgbm_quant', 'lgbm_base', 'ccp', 'cegb']
datapath = f'./results/valtest/baselines/'
root = Path(f'./results/valtest/baselines/largeredo/')
all_datasets = ["kin8nm", "california_housing", 'breastcancer', 'kr-vs-kp', 'mushroom', 'covtype', 'wine', 'covtype_multi']
for csv_path in root.rglob("*.csv"):
    seed = csv_path.parent.name
    df = pd.read_csv(csv_path)
    df = df[df['nodes'] != 0]
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    if len(df) == 0:
        continue
    for model in models:
        modelresults = df[df['model'] == model]
        for data in all_datasets:
            modelresultsdata = modelresults[modelresults['dataset'] == data]
            if len(modelresultsdata) == 0:
                continue
            if data in datasets_to_fix:
                fix_regression_data(modelresultsdata, datasets_to_fix)
            path = Path(f'{datapath}{seed}/{model}/{data}/result.csv')
            path.parent.mkdir(parents=True, exist_ok=True)
            modelresultsdata.sort_values(by=['max_trees', 'depth', 'alpha'], inplace=True)
            if path.exists():
                checkdf = pd.read_csv(path)
                checkdf = checkdf[checkdf['dataset'] == data]
                checkdf = checkdf[checkdf['model'] == model]
                modelresultsdata = pd.concat([modelresultsdata, checkdf])
                modelresultsdata.drop_duplicates(inplace=True)
            modelresultsdata.to_csv(path, index=False)
