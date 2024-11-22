import openml
import pandas as pd

# Retrieve metadata for all datasets
all_datasets = openml.datasets.list_datasets(output_format='dataframe')

# Filter for regression datasets
# We filter on 'NumberOfClasses' equal to 0 indicating regression
regression_datasets = all_datasets[all_datasets['NumberOfClasses'] == 0]

# Display some basic information about the regression datasets
print(regression_datasets[['did', 'name', 'NumberOfInstances', 'NumberOfFeatures', 'NumberOfClasses']].head())
binary_datasets = openml.datasets.list_datasets(output_format="dataframe")
binary_datasets = binary_datasets[binary_datasets['NumberOfClasses'] == 2]

# Show some basic information about the datasets
print(binary_datasets[['did', 'name', 'NumberOfInstances', 'NumberOfFeatures', 'NumberOfClasses', 'MajorityClassSize']].head())
