#!/bin/bash

cd experiments || exit

rm -r models # ATTENTION: deletes all models in the models folder
mkdir -p models 

ms=64000

for dataset in "california_housing" "kin8nm"; do
    mkdir -p models/${dataset}
    for tree in  1 2 3 4 5 6 7 8 9 10 15 20 30 40 50 100 200 500 1000 10000; do 
        for depth in 3 5 7; do 
            if "$1" config=train.conf objective=regression metric=rmse train_data=data/${dataset}.train valid_data=data/${dataset}.test max_depth=$depth num_trees=$tree output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            if "$1" config=train.conf objective=regression metric=rmse train_data=data/${dataset}.train valid_data=data/${dataset}.test tinygbdt_forestsize=$ms max_depth=$depth num_trees=$tree output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            for i in $(seq -10 1 15); do
                for j in $(seq -10 1 15); do
                    fp=$(python3 -c "print(float(2**$i))" )
                    tp=$(python3 -c "print(float(2**$j))" )
                    if "$1" config=train.conf objective=regression metric=rmse train_data=data/${dataset}.train valid_data=data/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                done
            done
        done
    done
done

for dataset in "breastcancer" "kr-vs-kp" "mushroom" "covtype"; do 
    mkdir -p models/${dataset}
    for tree in  1 2 3 4 5 6 7 8 9 10 15 20 30 40 50 100 200 500 1000 10000; do 
        for depth in 3 5 7; do 
            if "$1" config=train.conf objective=regression metric=rmse train_data=data/${dataset}.train valid_data=data/${dataset}.test max_depth=$depth num_trees=$tree output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            if "$1" config=train.conf objective=regression metric=rmse train_data=data/${dataset}.train valid_data=data/${dataset}.test tinygbdt_forestsize=$ms max_depth=$depth num_trees=$tree output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            for i in $(seq -10 1 15); do
                for j in $(seq -10 1 15); do
                    fp=$(python3 -c "print(float(2**$i))" )
                    tp=$(python3 -c "print(float(2**$j))" )
                    if "$1" config=train.conf objective=binary metric=auc train_data=data/${dataset}.train valid_data=data/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=models/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > models/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
          done
          done
      done
    done
done

cd python || exit

for dataset in "breastcancer" "covtype" "kr-vs-kp" "mushroom" "kin8nm" "california_housing"; do
    python3 evaluate_models.py ${dataset}
done

cd ..