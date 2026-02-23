import pandas as pd
import numpy as np
import os
import itertools
# max_trees,max_depth, tinygbdt_penalty_feature,tinygbdt_penalty_split
datasets = ['covtype', 'wine', 'covtype_multi']

for data in datasets:
    for seed in [1,2,5,6,7]:
        df = pd.read_csv(f'./results/olddata/mooreseeds/check/{data}/{seed}/results.csv')
        df2 = pd.read_csv(f'./results/olddata/mooreseeds/newrun/{data}/{seed}results.csv')
        df3 = pd.concat([df,df2], ignore_index=True)
        df3.drop_duplicates(inplace=True)
        print(len(df3.index))
        this = len(df3.index)
        if len(df3.index) < 32076:
            if not os.path.exists(f'./results/valtest/normal/{data}/{seed}/'):
                os.makedirs(f'./results/valtest/normal/{data}/{seed}/')
            df3.to_csv(f'./results/valtest/normal/{data}/{seed}/results.csv')
        else:
            if not os.path.exists(f'./results/olddata/mooreseeds/check2/{data}/{seed}/'):
                os.makedirs(f'./results/olddata/mooreseeds/check2/{data}/{seed}/')
            df3.to_csv(f'./results/olddata/mooreseeds/check2/{data}/{seed}/results.csv')


