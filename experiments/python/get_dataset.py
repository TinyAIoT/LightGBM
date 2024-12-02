
from sklearn.model_selection import train_test_split
import sklearn.datasets as datasets
import numpy as np
import wget, bz2
import os
from ucimlrepo import fetch_ucirepo 
from sklearn.preprocessing import LabelEncoder
  
directory = '../data'

if not os.path.exists(directory):
    os.makedirs(directory)

########################
# Covtype dataset https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html
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

X_train, X_test, y_train, y_test = train_test_split(covtype_libsvm[0], covtype_libsvm[1], test_size=0.2, random_state=42)
datasets.dump_svmlight_file(X_train, y_train, os.path.join(directory, 'covtype.train'), zero_based=False)
datasets.dump_svmlight_file(X_test, y_test, os.path.join(directory, 'covtype.test'), zero_based=False)
os.remove(os.path.join(directory, 'covtype.libsvm.binary.bz2'))
os.remove(os.path.join(directory, 'covtype.libsvm.binary'))

########################
# California housing dataset https://scikit-learn.org/dev/modules/generated/sklearn.datasets.fetch_california_housing.html
housing = datasets.fetch_california_housing()

X_train, X_test, y_train, y_test = train_test_split(housing.data, housing.target, test_size=0.2, random_state=42)
datasets.dump_svmlight_file(X_train, y_train, os.path.join(directory, 'california_housing.train'), zero_based=False)
datasets.dump_svmlight_file(X_test, y_test, os.path.join(directory, 'california_housing.test'), zero_based=False)

########################
# kin8nm dataset https://k8sapi.openml.org/d/189
kin8nm = datasets.fetch_openml(data_id=189)

X_train, X_test, y_train, y_test = train_test_split(kin8nm.data, kin8nm.target, test_size=0.2, random_state=42)
datasets.dump_svmlight_file(X_train, y_train, os.path.join(directory, 'kin8nm.train'), zero_based=False)
datasets.dump_svmlight_file(X_test, y_test, os.path.join(directory, 'kin8nm.test'), zero_based=False)

########################
# Mushroom dataset https://archive.ics.uci.edu/dataset/73/mushroom
mushroom = fetch_ucirepo(id=73) 

X = mushroom.data.features
y = mushroom.data.targets
X = X.apply(LabelEncoder().fit_transform).to_numpy()
y = y.apply(LabelEncoder().fit_transform).to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
datasets.dump_svmlight_file(X_train, y_train.flatten(), os.path.join(directory, 'mushroom.train'), zero_based=False)
datasets.dump_svmlight_file(X_test, y_test.flatten(), os.path.join(directory, 'mushroom.test'), zero_based=False)

########################
# chess kr-vs-kp dataset https://archive.ics.uci.edu/dataset/22/chess+king+rook+vs+king+pawn
chess = fetch_ucirepo(id=22) 

X = chess.data.features
y = chess.data.targets
X = X.apply(LabelEncoder().fit_transform).to_numpy()
y = y.apply(LabelEncoder().fit_transform).to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
datasets.dump_svmlight_file(X_train, y_train.flatten(), os.path.join(directory, 'kr-vs-kp.train'), zero_based=False)
datasets.dump_svmlight_file(X_test, y_test.flatten(), os.path.join(directory, 'kr-vs-kp.test'), zero_based=False)

########################
# breastcancer wisconsin (diagnostic) https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
breastcancer = fetch_ucirepo(id=17) 

X = breastcancer.data.features
y = breastcancer.data.targets
X = X.apply(LabelEncoder().fit_transform).to_numpy()
y = y.apply(LabelEncoder().fit_transform).to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
datasets.dump_svmlight_file(X_train, y_train.flatten(), os.path.join(directory, 'breastcancer.train'), zero_based=False)
datasets.dump_svmlight_file(X_test, y_test.flatten(), os.path.join(directory, 'breastcancer.test'), zero_based=False)
