
from sklearn.model_selection import train_test_split, KFold
import sklearn.datasets as datasets
import numpy as np
import wget, bz2
import os
from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from pathlib import Path
import warnings
import argparse
import ssl
import certifi
import wget

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_data_small(data, target, name, seeds, flatten=False):
    for seed in seeds:
        directory = base_dir + f"{seed}"
        X_trainpre, X_val, y_trainpre, y_val = train_test_split(data, target, test_size=0.2, random_state=seed)
        kf = KFold(n_splits=5)
        kf.get_n_splits(X_trainpre)
        if isinstance(X_trainpre, pd.DataFrame):
            X_trainpre = X_trainpre.to_numpy()
            y_trainpre = y_trainpre.to_numpy()
        for i, (train_index, test_index) in enumerate(kf.split(X_trainpre)):
            finaldir = directory + '/' + str(i)
            seeddir = directory + '/'
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

def fetch_data(data, target, name, seeds, flatten=False):
    for seed in seeds:
        directory = base_dir + f"{seed}"
        X_trainpre, X_val, y_trainpre, y_val = train_test_split(data, target, test_size=0.2, random_state=seed)
        X_train, X_test, y_train, y_test = train_test_split(X_trainpre, y_trainpre, test_size=0.1, random_state=seed)

        if flatten:
            datasets.dump_svmlight_file(X_train, y_train.flatten(), os.path.join(directory, name + '.train'), zero_based=False)
            datasets.dump_svmlight_file(X_test, y_test.flatten(), os.path.join(directory, name + '.test'), zero_based=False)
            datasets.dump_svmlight_file(X_val, y_val.flatten(), os.path.join(directory, name + '.val'), zero_based=False)
        else:
            datasets.dump_svmlight_file(X_train, y_train, os.path.join(directory, name + '.train'), zero_based=False)
            datasets.dump_svmlight_file(X_test, y_test, os.path.join(directory, name + '.test'), zero_based=False)
            datasets.dump_svmlight_file(X_val, y_val, os.path.join(directory, name + '.val'), zero_based=False)

def find_missing_seeds(seeds, directory, data):
    selectedseeds = []
    for seed in seeds:
        if not os.path.exists(directory + f'/{seed}/{data}.test'):
            selectedseeds.append(seed)
    return selectedseeds

if __name__ == "__main__":
    cwd = Path.cwd()
    if cwd.name != "experiments":
        warnings.warn(f"Note: you are running the script from a different than the 'experiments' directory. Current: {cwd}")

    seedsdefault = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    datasetsdefault = ['breastcancer', 'kr-vs-kp', 'mushroom', 'covtype', 'covtype_mutli', 'wine', 'kin8nm', 'california_housing']
    parser = argparse.ArgumentParser(description='Get datasets for experiments')
    parser.add_argument('--directory', type=str, default='./data/', help='Directory to save datasets')
    parser.add_argument('--seeds', type=int, nargs="+", default=seedsdefault, metavar="N", help=f'Seeds (default: {datasetsdefault})')
    parser.add_argument('--datasets', type=str, nargs="+", default=datasetsdefault, metavar="N", help=f'Datasets (default: {datasetsdefault})')
    args = parser.parse_args()
    base_dir = args.directory
    seeds = args.seeds
    argdatasets = args.datasets

    for seed in seeds:
        directory = base_dir+f"{seed}"
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Covtype dataset https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html
    selectedseeds = find_missing_seeds(seeds, base_dir, 'covtype')
    if 'covtype' in argdatasets and len(selectedseeds) > 0:
        path = wget.download('https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/covtype.libsvm.binary.bz2', os.path.join(directory, 'covtype.libsvm.binary.bz2'))

        with bz2.open(os.path.join(directory, 'covtype.libsvm.binary.bz2')) as f:
            # Decompress data from file
            content = f.read()
            # Write decompressed data to file
            with open(os.path.join(directory, 'covtype.libsvm.binary'), 'wb') as f:
                f.write(content)

        covtype_libsvm = datasets.load_svmlight_file(os.path.join(directory, 'covtype.libsvm.binary'))
        # convert target to [0,1] from [1,2]
        ids = np.where(covtype_libsvm[1] == 1)
        covtype_libsvm[1][ids]=0
        ids = np.where(covtype_libsvm[1] == 2)
        covtype_libsvm[1][ids]=1

        fetch_data(covtype_libsvm[0], covtype_libsvm[1], 'covtype', selectedseeds)
        os.remove(os.path.join(directory, 'covtype.libsvm.binary.bz2'))
        os.remove(os.path.join(directory, 'covtype.libsvm.binary'))

    selectedseeds = find_missing_seeds(seeds, base_dir, 'california_housing')
    # California housing dataset https://scikit-learn.org/dev/modules/generated/sklearn.datasets.fetch_california_housing.html
    if 'california_housing' in argdatasets and len(selectedseeds) > 0:
        housing = datasets.fetch_california_housing()
        fetch_data(housing.data, housing.target, 'california_housing', seeds)

    selectedseeds = find_missing_seeds(seeds, base_dir, 'kin8nm')
    # kin8nm dataset https://k8sapi.openml.org/d/189
    if 'kin8nm' in argdatasets and len(selectedseeds) > 0:
        kin8nm = datasets.fetch_openml(data_id=189)
        fetch_data(kin8nm.data, kin8nm.target, 'kin8nm', seeds)

    selectedseeds = find_missing_seeds(seeds, base_dir, 'mushroom')
    # Mushroom dataset https://archive.ics.uci.edu/dataset/73/mushroom
    if 'mushroom' in argdatasets and len(selectedseeds) > 0:
        mushroom = fetch_ucirepo(id=73)

        X = mushroom.data.features
        y = mushroom.data.targets
        X = X.apply(LabelEncoder().fit_transform).to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data(X, y, 'mushroom', seeds, True)

    selectedseeds = find_missing_seeds(seeds, base_dir, 'kr-vs-kp')
    # chess kr-vs-kp dataset https://archive.ics.uci.edu/dataset/22/chess+king+rook+vs+king+pawn
    if 'kr-vs-kp' in argdatasets and len(selectedseeds) > 0:
        chess = fetch_ucirepo(id=22)

        X = chess.data.features
        y = chess.data.targets
        X = X.apply(LabelEncoder().fit_transform).to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data_small(X, y, 'kr-vs-kp', seeds, True)

    selectedseeds = find_missing_seeds(seeds, base_dir, 'breastcancer')
    # breastcancer wisconsin (diagnostic) https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
    if 'breastcancer' in argdatasets and len(selectedseeds) > 0:
        breastcancer = fetch_ucirepo(id=17)

        X = breastcancer.data.features
        y = breastcancer.data.targets
        X = X.apply(LabelEncoder().fit_transform).to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data_small(X, y, 'breastcancer', seeds,True)

    selectedseeds = find_missing_seeds(seeds, base_dir, 'wine')
    # wine quality https://archive.ics.uci.edu/dataset/186/wine+quality
    if 'wine' in argdatasets and len(selectedseeds) > 0:
        wine = fetch_ucirepo(id=186)

        X = wine.data.features
        y = wine.data.targets
        X = X.to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data(X, y, 'wine', seeds, True)

    selectedseeds = find_missing_seeds(seeds, base_dir, 'covtype_multi')
    if 'covtype_multi' in argdatasets and len(selectedseeds) > 0:
        covtype = fetch_ucirepo(id=31)

        X = covtype.data.features
        y = covtype.data.targets
        X = X.to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data(X, y, 'covtype_multi', seeds, True)
