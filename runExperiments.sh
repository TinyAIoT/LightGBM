#!/bin/bash

cd experiments || exit

./getdatasets.sh
#rm -r models # ATTENTION: deletes all models in the models folder
#mkdir -p models

# ./getdatasets.sh
runSettings () {
  task=$2
  metric=$3
  dataset=$4
  ms=64000
  mkdir -p models/${dataset}
  for tree in  1 2 3 4 5 6 7 8 9 10 15 20 30 40 50 100 200 500 1000; do
    for depth in 3 5 7; do
      if "$1" config=train.conf objective=$task metric=$metric train_data=data/${dataset}.train valid_data=data/${dataset}.test max_depth=$depth num_trees=$tree output_model=models/${dataset}/data-${dataset}-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-tree-${tree}-depth-${depth}.out; then
        echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
      else
        echo "Training model fp $fp tp $tp failed / not complete"
      fi
      if "$1" config=train.conf objective=$task metric=$metric train_data=data/${dataset}.train valid_data=data/${dataset}.test tinygbdt_forestsize=$ms max_depth=$depth num_trees=$tree output_model=models/${dataset}/data-${dataset}ms-$ms-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-tree-${tree}-depth-${depth}.out; then
        echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
      else
        echo "Training model fp $fp tp $tp failed / not complete"
      fi
      for i in $(seq -10 1 15); do
        for j in $(seq -10 1 15); do
          fp=$(python3 -c "print(float(2**$i))" )
          tp=$(python3 -c "print(float(2**$j))" )
          if "$1" config=train.conf objective=$task metric=$metric train_data=data/${dataset}.train valid_data=data/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
            echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
          else
            echo "Training model fp $fp tp $tp failed / not complete"
          fi
        done
      done
    done
  done
  cd python || exit
  python3 evaluate_models.py ${dataset}
  cd .. || exit
  rm -rf models/${dataset}
}
folder=$2
if [[ $folder == "breastcancer" ]]; then
  runSettings $1 binary auc breastcancer
fi
if [[ $folder == "kr-vs-kp" ]]; then
  runSettings $1 binary auc kr-vs-kp
fi
if [[ $folder == "mushroom" ]]; then
  runSettings $1 binary auc mushroom
fi
if [[ $folder == "covtype" ]]; then
  runSettings $1 binary auc covtype
fi
if [[ $folder == "rcv1" ]]; then
  runSettings $1 binary auc rcv1
fi
if [[ $folder == "url_combined" ]]; then
  runSettings $1 binary auc url_combined
fi
if [[ $folder == "california_housing" ]]; then
  runSettings $1 regression rmse california_housing
fi
if [[ $folder == "kin8nm" ]]; then
  runSettings $1 regression rmse kin8nm
fi
if [[ $folder == "yearpredictionMSD" ]]; then
  runSettings $1 regression rmse yearpredictionMSD
fi
