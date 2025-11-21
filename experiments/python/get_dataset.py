
from sklearn.model_selection import train_test_split, KFold
import sklearn.datasets as datasets
import numpy as np
import wget, bz2
import os
from ucimlrepo import fetch_ucirepo
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def fetch_data(data, target, name, flatten=False):
    X_trainpre, X_val, y_trainpre, y_val = train_test_split(data, target, test_size=0.2, random_state=42)
    kf = KFold(n_splits=5)
    kf.get_n_splits(X_trainpre)
    if isinstance(X_trainpre, pd.DataFrame):
        X_trainpre = X_trainpre.to_numpy()
        y_trainpre = y_trainpre.to_numpy()
    for i, (train_index, test_index) in enumerate(kf.split(X_trainpre)):
        if not os.path.exists(directory + '/' + str(i)):
            os.makedirs(directory + '/' + str(i))
        if flatten:
            datasets.dump_svmlight_file(X_trainpre[train_index,:], y_trainpre[train_index].flatten(), os.path.join(directory + '/' + str(i), name + '.train'),
                                        zero_based=False)
            datasets.dump_svmlight_file(X_trainpre[test_index,:], y_trainpre[test_index].flatten(), os.path.join(directory+ '/' + str(i), name + '.test'),
                                        zero_based=False)
        else:
            datasets.dump_svmlight_file(X_trainpre[train_index,:], y_trainpre[train_index], os.path.join(directory+ '/' + str(i), name + '.train'), zero_based=False)
            datasets.dump_svmlight_file(X_trainpre[test_index,:], y_trainpre[test_index], os.path.join(directory+ '/' + str(i), name + '.test'), zero_based=False)

    if flatten:
        datasets.dump_svmlight_file(X_trainpre, y_trainpre.flatten(), os.path.join(directory, name + '.train'), zero_based=False)
        datasets.dump_svmlight_file(X_val, y_val.flatten(), os.path.join(directory, name + '.val'), zero_based=False)
    else:
        datasets.dump_svmlight_file(X_trainpre, y_trainpre, os.path.join(directory, name + '.train'), zero_based=False)
        datasets.dump_svmlight_file(X_val, y_val, os.path.join(directory, name + '.val'), zero_based=False)

# main function:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get datasets for experiments')
    parser.add_argument('--directory', type=str, default='../data', help='Directory to save datasets')
    args = parser.parse_args()
    directory = args.directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    ########################
    # Covtype dataset https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html
    # if not os.path.exists(directory + '/covtype.test'):
    #     path = wget.download('https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/covtype.libsvm.binary.bz2', os.path.join(directory, 'covtype.libsvm.binary.bz2'))
    #
    #     with bz2.open(os.path.join(directory, 'covtype.libsvm.binary.bz2')) as f:
    #         # Decompress data from file
    #         content = f.read()
    #         # Write decompressed data to file
    #         with open(os.path.join(directory, 'covtype.libsvm.binary'), 'wb') as f:
    #             f.write(content)
    #
    #     covtype_libsvm = datasets.load_svmlight_file(os.path.join(directory, 'covtype.libsvm.binary'))
    #     # convert target to [0,1] from [1,2]
    #     ids = np.where(covtype_libsvm[1] == 1)
    #     covtype_libsvm[1][ids]=0
    #     ids = np.where(covtype_libsvm[1] == 2)
    #     covtype_libsvm[1][ids]=1
    #
    #     fetch_data(covtype_libsvm[0], covtype_libsvm[1], 'covtype')
    #     os.remove(os.path.join(directory, 'covtype.libsvm.binary.bz2'))
    #     os.remove(os.path.join(directory, 'covtype.libsvm.binary'))

    ########################
    # # California housing dataset https://scikit-learn.org/dev/modules/generated/sklearn.datasets.fetch_california_housing.html
    # if not os.path.exists(directory + '/california_housing.test'):
    #     housing = datasets.fetch_california_housing()
    #     fetch_data(housing.data, housing.target, 'california_housing')
    #
    # ########################
    # # kin8nm dataset https://k8sapi.openml.org/d/189
    # if not os.path.exists(directory + 'kin8nm.test'):
    #     kin8nm = datasets.fetch_openml(data_id=189)
    #     fetch_data(kin8nm.data, kin8nm.target, 'kin8nm')
    #
    # ########################
    # # Mushroom dataset https://archive.ics.uci.edu/dataset/73/mushroom
    # if not os.path.exists(directory + '/mushroom.test'):
    #     mushroom = fetch_ucirepo(id=73)
    #
    #     X = mushroom.data.features
    #     y = mushroom.data.targets
    #     X = X.apply(LabelEncoder().fit_transform).to_numpy()
    #     y = y.apply(LabelEncoder().fit_transform).to_numpy()
    #     fetch_data(X, y, 'mushroom', True)

    ########################
    # chess kr-vs-kp dataset https://archive.ics.uci.edu/dataset/22/chess+king+rook+vs+king+pawn
    if not os.path.exists(directory + '/kr-vs-kp.test'):
        chess = fetch_ucirepo(id=22)

        X = chess.data.features
        y = chess.data.targets
        X = X.apply(LabelEncoder().fit_transform).to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data(X, y, 'kr-vs-kp', True)

    ########################
    # breastcancer wisconsin (diagnostic) https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
    if not os.path.exists(directory + '/breastcancer.test'):
        breastcancer = fetch_ucirepo(id=17)
        X = breastcancer.data.features
        y = breastcancer.data.targets
        X = X.to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data(X, y, 'breastcancer', True)

# ########################
# # wine quality https://archive.ics.uci.edu/dataset/186/wine+quality
# if not os.path.exists(directory + '/wine.test'):
#     wine = fetch_ucirepo(id=186)
#
#     X = wine.data.features
#     y = wine.data.targets
#     X = X.to_numpy()
#     y = y.apply(LabelEncoder().fit_transform).to_numpy()
#     fetch_data(X, y, 'wine', True)
#
# if not os.path.exists(directory + '/covtype_multi.test'):
#     covtype = fetch_ucirepo(id=31)
#
#     X = covtype.data.features
#     y = covtype.data.targets
#     X = X.to_numpy()
#     y = y.apply(LabelEncoder().fit_transform).to_numpy()
#     fetch_data(X, y, 'covtype_multi', True)
