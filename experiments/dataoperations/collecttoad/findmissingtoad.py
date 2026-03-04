import pandas as pd
import numpy as np
import os
import itertools

def write_joblist(data, sed, remaining):
    out_path = f'./results/valtest/jobstoad/{data}-{sed}-joblist.txt'
    with open(out_path, "w") as f:
        for max_tree, max_depth, pen_feat, pen_split in remaining:
            line = f"{data} {max_tree} {max_depth} {pen_feat} {pen_split} {sed}\n"
            f.write(line)

    print(f"Datei '{out_path}' wurde erstellt. Missing {len(remaining)} items.")


datasets = ['covtype', 'wine', 'covtype_multi', 'california_housing', 'kin8nm', 'mushroom']
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
trees   = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
depths  = [1, 2, 4, 8]
penalties = [
    0, 0.000976562, 0.00195312, 0.00390625, 0.0078125,
    0.015625, 0.03125, 0.0625, 0.125, 0.25,
    0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256,
    512, 1024, 2048, 4096, 8192, 16384, 32768]
for data in datasets:
    for sed in seeds:
        path = f'./results/valtest/normal/{data}/{sed}/results.csv'
        if not os.path.exists(path):
            print(f"No results found for {data}/{sed}")
            continue

        df_done = pd.read_csv(path, usecols=[
        "max_trees", "max_depth",
        "toad_penalty_feature", "toad_penalty_threshold"])

        all_combos = list(itertools.product(
            trees,
            depths,
            penalties,
            penalties
        ))
        done_set = set(
            df_done.itertuples(index=False, name=None)
        )
        remaining = [
            combo for combo in all_combos
            if combo not in done_set
        ]

        if len(remaining) > 0:
            write_joblist(data, sed, remaining)

