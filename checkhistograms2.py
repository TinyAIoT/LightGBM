import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("examples/min/min.train", sep='\t', header=None)

# Function to create bins with one bin reserved for zeros and dynamic binning based on value range
def create_bins_with_zero(df_column, num_bins=9):
    # Separate zero and non-zero values
    zero_values = df_column[df_column == 0]
    non_zero_values = df_column[df_column != 0]

    # Check for presence of negative values
    has_negative = non_zero_values.min() < 0

    if has_negative:
        # If there are negative numbers, create bins with a special bin for 0
        non_zero_bins = pd.qcut(non_zero_values, num_bins - 1, duplicates='drop')
        bins = ['0.000 to -0.000'] + non_zero_bins.cat.categories.tolist()
    else:
        # If no negative numbers, start bins at zero
        non_zero_bins = pd.qcut(non_zero_values, num_bins - 1, duplicates='drop')
        bins = non_zero_bins.cat.categories.tolist()
    
    # Create a new column with NaN values
    binned_column = pd.Series(np.nan, index=df_column.index)

    # Fill in the bins for non-zero values
    binned_column.loc[non_zero_values.index] = non_zero_bins
    
    # Assign all zero values to the zero-bin
    binned_column.loc[zero_values.index] = 'Zero bin'
    
    return binned_column

#n_cols = 2
#n_rows = (len(df.columns) - 1) // n_cols + 1  # Calculate required rows

# Create the figure and a grid of subplots
#fig, axes = plt.subplots(n_rows, n_cols * 2, figsize=(16, n_rows * 4), sharex=False, sharey=False)

# Flatten the axes array for easy access
#axes = axes.flatten()

# Apply the binning function to each column and store the binned data
for col in df.columns[1:]:
    print(df[col].dtype)
    print(df[col].head())
    df[f'{col}_binned'] = create_bins_with_zero(df[col])

counter = 0
print(df.columns)
# Plotting each of the 4 original columns with the corresponding binned data
for col in [1, 2, 3]:
    #plt.figure(figsize=(12, 6))
    
    # Plot histogram of the original column data
    plt.subplot(1, 2, 1)

    plt.hist(df[col], bins=10, color='blue', alpha=0.7)
    plt.title(f'Original Data: {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    #axes[counter].hist(df[col], bins=10, color='blue', alpha=0.7)
    #axes[counter].set_title(f'Original Data: {col}')
    #axes[counter].set_xlabel(col)
    #axes[counter].set_ylabel('Frequency')

    counter += 1
    # Plot histogram of the binned data with counts
    plt.subplot(1, 2, 2) 
    bin_counts = df[f'{col}_binned'].value_counts(sort=False)
    if col == 3:
        print('TRYING TO SAVE CSV !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        df.to_csv('examples/min/min_binned.csv', sep='\t', index=False)

    bin_counts.plot(kind='bar', color='green', alpha=0.7)
    plt.title(f'Binned Data: {col}')
    plt.xlabel('Bins')
    plt.ylabel('Count (including duplicates)')
    #bin_counts.plot(kind='bar', color='green', alpha=0.7, ax=axes[counter])
    #axes[counter].set_title(f'Binned Data: {col}')
    #axes[counter].set_xlabel('Bins')
    #axes[counter].set_ylabel('Count (including duplicates)')
    
    # Show counts on top of the bars
    for i, count in enumerate(bin_counts):
        #axes[counter].text(i, count, str(count), ha='center', va='bottom')
        plt.text(i, count, str(count), ha='center', va='bottom')
    counter += 1
    plt.show()


# Save the resulting binned dataframe to a new file
