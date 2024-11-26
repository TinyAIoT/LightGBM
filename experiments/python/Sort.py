import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Name of the dataset")
parser.add_argument('string_arg', type=str, help='the datasetname')
args = parser.parse_args()

# You can access the arguments using args.string_arg and args.directory
print(f"String argument: {args.string_arg}")
df = pd.read_csv('../results/' + args.string_arg + '/smallvalues.csv')
df_sorted = df.sort_values(by=['tinygbdt_penalty_feature', 'tinygbdt_penalty_split'])
df_sorted_reset = df_sorted.reset_index(drop=True)
print(df.head(500))
sequence2 = [5, 5, 5,
            10, 10, 10,
            15, 15, 15,
            20, 20, 20,
            30, 30, 30,
            40, 40, 40,
            50, 50, 50,
            100, 100, 100,
            200, 200, 200,
            500, 500, 500,
            1000, 1000, 1000,
            5000, 5000, 5000,
            10000, 10000, 10000,
            100000, 100000, 100000]
sequence = [3,3]
num_repeats = len(df_sorted_reset) // len(sequence)  # Calculate how many full sequence repeats are needed
remainder = len(df_sorted_reset) % len(sequence)
# Create the full repeated sequence
repeated_sequence = np.tile(sequence, num_repeats)
if remainder > 0:
    repeated_sequence = np.append(repeated_sequence, sequence[:remainder])

# Add the new column to the DataFrame
df_sorted_reset['depth'] = repeated_sequence
print(df_sorted_reset.head(50))

df_sorted_reset.to_csv('../results/' + args.string_arg + '/smallv.csv', index=False)
