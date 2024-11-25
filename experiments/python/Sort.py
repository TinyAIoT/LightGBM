import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Name of the dataset")
parser.add_argument('string_arg', type=str, help='the datasetname')
args = parser.parse_args()

# You can access the arguments using args.string_arg and args.directory
print(f"String argument: {args.string_arg}")
df = pd.read_csv('../results/' + args.string_arg + '/simple_all.csv')
df_sorted = df.sort_values(by=['tinygbdt_penalty_feature', 'tinygbdt_penalty_split'])
df_sorted_reset = df_sorted.reset_index(drop=True)
print(df.head(100))
sequence = [5, 10, 15, 20, 30, 40, 50, 100, 200, 500]
num_repeats = len(df_sorted_reset) // len(sequence)  # Calculate how many full sequence repeats are needed
remainder = len(df_sorted_reset) % len(sequence)

# Create the full repeated sequence
repeated_sequence = np.tile(sequence, num_repeats)
if remainder > 0:
    repeated_sequence = np.append(repeated_sequence, sequence[:remainder])

# Add the new column to the DataFrame
df_sorted_reset['max_trees'] = repeated_sequence
print(df_sorted_reset.head(50))

df_sorted_reset.to_csv('../results/' + args.string_arg + '/simple_all2.csv', index=False)
