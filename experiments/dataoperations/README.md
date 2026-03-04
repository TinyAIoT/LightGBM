# Data Operation
Data processing includes:

1. Collecting dataset before models are trained --> `get_datasets.py`
2. Collecting results in a structured way, as depending on the cluster environment data might be collected in different ways (`collectbaselines` and `collecttoad`)

## `get_dataset.py`

By default collects all of
```python
seedsdefault = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
datasetsdefault = ['breastcancer', 'kr-vs-kp', 'mushroom', 'covtype', 'covtype_mutli', 'wine', 'kin8nm', 'california_housing']
```
As a default all data are saved to `./data`, which can be adapted with the parameter `--directory`.
In case you want to test something locally you can adapt `--seeds` and `--datasets` with a sequence of strings. (e.g. `python dataoperations/get_datasets.py --seeds 1 2 --datasets breastcancer kin8nm`).
Note that breastcancer and kr-vs-kp are collected with 5 splits for kfolds while bigger datasets are split in 72/8/20 train/val/test split. Therefore, they will look different in the data folder:

```bash
├── 10 (randomseed)
│         ├── 0 (kfold - for smaller datasets)
│         │         ├── breastcancer.val
│         │         ├── breastcancer.train
│         ├── xx (further folds)
│         │         ├── breastcancer.val
│         │         ├── breastcancer.train
│         ├── 4 (we used 5 however do what suits your dataset)
│         │         ├── breastcancer.val
│         │         ├── breastcancer.train
│         ├── breastcancer.train
│         ├── breastcancer.val (VALIDATION FOR SMALLER DATASETS ALSO HERE!!)
│         ├── kin8nm.test (all three splits for bigger datasets)
│         ├── kin8nm.train
│         ├── kin8nm.test
│         ├── xxxx (more datasets)
xxx (more randomseeds)
```

New datasets have to implemented yourself.

### Troubleshooting
Mac sometimes experiences ceritficates issues.
`urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: Missing Subject Key Identifier (_ssl.c:1032)>`
Quick but not secure fix is to include:

```python
ssl._create_default_https_context = ssl._create_unverified_context
```

## `collectbaselines`

See documentation in the folder.

## `collecttoad`

See documentation in the folder.
