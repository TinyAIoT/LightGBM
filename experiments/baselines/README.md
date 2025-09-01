# How To Evaluate Baseline Models

## CEGB
Run `"../../Release/lightgbm" config=train_cegb.conf > "logs/log.txt"` in bash terminal. 

### Docu 
Did some examplary runs on covtype binary dataset. 
Useful settings seem to need some fine-tuning. 
- Only setting `cegb_penalty_split = x` with x > 0 does not influence the resulting trees. 
- Setting cegb_penalty_feature_coupled for each feature leads to changes, but with every feature=1 not to much change. Applying multiplier with e.g. `cegb_tradeoff = 1000` results in way fewer features used. 
- Setting cegb_penalty_feature_lazy for each feature only creates one node. Decreasing by introducing multiplier with `cegb_tradeoff = 0.1` leads to mostly using feature 1. With the multiplier, setting feature 1 penalty to another value is very sensitive (i.e. 1, 10, 1, 1, ..). 1.2 has no influence, 1.3 removes all except one node. 