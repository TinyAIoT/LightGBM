# Local Experiments

The run scripts in this repository allow you to test some config locally, in a way close to the high performance cluster.
- `./experiments/localrun/toad/run.sh` -> Only runs toad please look at lightgbm for recommendation for building! (Also depends on your hardware)
- `./experiments/localrun/baselines/run.sh` -> Runs the baselines.


If you want to test multiple settings you might want to build a bash wrapper around the run scripts.
`./lightgbm config=train.conf objective=regression num_classes=1 metric=rmse train_data=./experiments/data/1/kin8nm.train valid_data=./experiments/data/1/kin8nm.val max_tree=8 max_depth=4 toad_forestsize=64000 toad_penalty_threshold=0.0 toad_penalty_feature=0.0 output_model=./experiments/local/model/kin8nm1/testkin.txt`
