
from sklearn.model_selection import train_test_split, KFold
import sklearn.datasets as datasets
import numpy as np
import wget, bz2
import os
from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def fetch_data(data, target, name, seed, flatten=False):
    X_trainpre, X_val, y_trainpre, y_val = train_test_split(data, target, test_size=0.2, random_state=seed)
    kf = KFold(n_splits=5)
    kf.get_n_splits(X_trainpre)
    if isinstance(X_trainpre, pd.DataFrame):
        X_trainpre = X_trainpre.to_numpy()
        y_trainpre = y_trainpre.to_numpy()
    for i, (train_index, test_index) in enumerate(kf.split(X_trainpre)):
        finaldir = directory + '/' + f'{seed}/' + str(i)
        seeddir = directory + '/' + f'{seed}/'
        if not os.path.exists(finaldir):
            os.makedirs(finaldir)
        if flatten:
            datasets.dump_svmlight_file(X_trainpre[train_index,:], y_trainpre[train_index].flatten(), os.path.join(finaldir, name + '.train'),
                                        zero_based=False)
            datasets.dump_svmlight_file(X_trainpre[test_index,:], y_trainpre[test_index].flatten(), os.path.join(finaldir, name + '.test'),
                                        zero_based=False)
        else:
            datasets.dump_svmlight_file(X_trainpre[train_index,:], y_trainpre[train_index], os.path.join(finaldir, name + '.train'), zero_based=False)
            datasets.dump_svmlight_file(X_trainpre[test_index,:], y_trainpre[test_index], os.path.join(finaldir, name + '.test'), zero_based=False)

    if flatten:
        datasets.dump_svmlight_file(X_trainpre, y_trainpre.flatten(), os.path.join(seeddir, name + '.train'), zero_based=False)
        datasets.dump_svmlight_file(X_val, y_val.flatten(), os.path.join(seeddir, name + '.val'), zero_based=False)
    else:
        datasets.dump_svmlight_file(X_trainpre, y_trainpre, os.path.join(seeddir, name + '.train'), zero_based=False)
        datasets.dump_svmlight_file(X_val, y_val, os.path.join(seeddir, name + '.val'), zero_based=False)

# main function:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get datasets for experiments')
    parser.add_argument('--directory', type=str, default='../data', help='Directory to save datasets')
    args = parser.parse_args()
    directory = args.directory

    seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if not os.path.exists(directory):
        os.makedirs(directory)
    for seed in seeds:
        if not os.path.exists(directory + '/kr-vs-kp.test'):
            chess = fetch_ucirepo(id=22)

            X = chess.data.features
            y = chess.data.targets
            X = X.apply(LabelEncoder().fit_transform).to_numpy()
            y = y.apply(LabelEncoder().fit_transform).to_numpy()
            fetch_data(X, y, 'kr-vs-kp', seed, True)

        # breastcancer wisconsin (diagnostic) https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
        if not os.path.exists(directory + '/breastcancer.test'):
            breastcancer = fetch_ucirepo(id=17)

            X = breastcancer.data.features
            y = breastcancer.data.targets
            X = X.apply(LabelEncoder().fit_transform).to_numpy()
            y = y.apply(LabelEncoder().fit_transform).to_numpy()
            fetch_data(X, y, 'breastcancer', seed,True)
