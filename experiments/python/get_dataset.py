import openml

from sklearn.model_selection import train_test_split
from sklearn.datasets import dump_svmlight_file
import numpy as np
import os
import re

# Step 1: Fetch the Kin8nm dataset from OpenML
# The OpenML ID for the kin8nm dataset is 189
dataset = openml.datasets.get_dataset(189)
X, y, _, attribute_names = dataset.get_data(target=dataset.default_target_attribute, dataset_format='array')

# Step 2: Split the dataset into an 80/20 train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Save the datasets in LIBSVM format
name = "openml_kin8nm"

# Save the training data
dump_svmlight_file(X_train, y_train, "openml_kin8nm.train")

# Save the test data
dump_svmlight_file(X_test, y_test, "openml_kin8nm.test")
