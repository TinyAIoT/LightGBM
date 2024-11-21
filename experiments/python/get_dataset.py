from sklearn.datasets import fetch_california_housing, load_svmlight_file, dump_svmlight_file
import pandas as pd
import numpy as np
import collections
from sklearn.model_selection import train_test_split

# housing = fetch_california_housing(as_frame=True)

# df = pd.DataFrame(housing.frame)

# # print(housing.frame)

# # train, test = train_test_split(housing.frame, test_size=0.2, random_state=42)
# X_train, X_test, y_train, y_test = train_test_split(housing.data, housing.target, test_size=0.2, random_state=42)
# dump_svmlight_file(X_train, y_train, '../data/california_housing.libsvm.train', zero_based=False)
# dump_svmlight_file(X_test, y_test, '../data/california_housing.libsvm.test', zero_based=False)

# print(train)
# print(test)

# housing.frame.to_csv('../california_housing.csv', index=False)
# train.to_csv('../california_housing.train.csv', index=False)
# test.to_csv('../california_housing.test.csv', index=False)

covtype_libsvm = load_svmlight_file('../data/covtype.libsvm.binary/covtype.libsvm.binary')
# print(covtype_libsvm[0])
# print(covtype_libsvm[1])

X_train, X_test, y_train, y_test = train_test_split(covtype_libsvm[0], covtype_libsvm[1], test_size=0.2, random_state=42)
# print(X_train)
# print(X_test)
# print(y_train)
print(type(y_test))
print(len(np.where(y_test == 1.)))
print(len(np.where(y_test == 0.)))
counter = collections.Counter(y_test)
print(counter)
counter = collections.Counter(y_train)
print(counter)

# dump_svmlight_file(X_train, y_train, '../data/covtype.libsvm.binary/covtype.libsvm.binary.train', zero_based=False)
# dump_svmlight_file(X_test, y_test, '../data/covtype.libsvm.binary/covtype.libsvm.binary.test', zero_based=False)