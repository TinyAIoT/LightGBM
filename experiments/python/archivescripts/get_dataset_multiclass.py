
from sklearn.model_selection import train_test_split
import sklearn.datasets as datasets
import numpy as np
import wget, bz2
import os
from ucimlrepo import fetch_ucirepo 
from sklearn.preprocessing import LabelEncoder


def fetch_data(data, target, name, flatten=False):
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=42)
    if flatten:
        datasets.dump_svmlight_file(X_train, y_train.flatten(), os.path.join(directory, name + '.train'), zero_based=False)
        datasets.dump_svmlight_file(X_test, y_test.flatten(), os.path.join(directory, name + '.test'), zero_based=False)
    else:
        datasets.dump_svmlight_file(X_train, y_train, os.path.join(directory, name + '.train'), zero_based=False)
        datasets.dump_svmlight_file(X_test, y_test, os.path.join(directory, name + '.test'), zero_based=False)

# main function:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Get datasets for experiments')
    parser.add_argument('--directory', type=str, help='Directory to save datasets')
    args = parser.parse_args()
    directory = args.directory

    if not os.path.exists(directory):
        os.makedirs(directory)

    ######################## Get covtype multiclass datasets
    if not os.path.exists(directory + '/covtype_multi.test'):
        covtype = fetch_ucirepo(id=31)

        X = covtype.data.features
        y = covtype.data.targets
        X = X.to_numpy()
        y = y.apply(LabelEncoder().fit_transform).to_numpy()
        fetch_data(X, y, 'covtype_multi', True)