import numpy
import pandas as pd
import matplotlib.pyplot as plt


min_df = pd.read_csv("examples/min/min.train", sep='\t')
print(min_df.info)
# Define the number of quantiles (bins) you want
num_bins = 10
fig, axes = plt.subplots(2, 2, figsize=(8, 6))

for x in [1, 2, 3, 4]:
    # Use qcut to get the bin edges such that each bin has approximately the same number of data points
    filtered_data = min_df.iloc[:, x][min_df.iloc[:, x] != 0]
    print(f"MINIMUM OF COLUMN {x}")
    print(min(filtered_data))
    if filtered_data.nunique() < num_bins:
        print(f"Not enough unique values in column {x} to create {num_bins} bins.")
        ax = axes.ravel()[x-1]
        ax.set_title(f'Not enough data in column {x}')
        ax.axis('off')
        continue
    try:
        quantile_bins = pd.qcut(filtered_data, q=num_bins, duplicates='drop')
        # Get the bin edges and counts for the quantiles
        bin_counts = quantile_bins.value_counts(sort=False)
        # Plot the histogram
        ax = axes.ravel()[x-1]
        bin_counts.plot(kind='bar', ax=ax)
        # Add title and labels
        ax.set_title(f'Histogram {x} with Equal Frequency Bins')
        ax.set_xlabel('Quantile Bins')
        ax.set_ylabel('Count of Data Points')
    except ValueError as e:
        print(f"Error in column {x}: {e}")
        ax.set_title(f'Error in column {x}')
        ax.axis('off')  # D

plt.tight_layout()
plt.show()
# Check for missing values or inconsistencies

# for x in range(4):
#     filtered_data = min_df.iloc[:, x][min_df.iloc[:, x] != 0]
#     ax = axes.ravel()[x]
#     counts, bin_edges, _ = ax.hist(filtered_data, bins=8)
#     plt.xticks(bin_edges)
#     ax.set_title(f'Histogram {x+1}')
