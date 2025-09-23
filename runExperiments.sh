#!/bin/bash

cd experiments || exit

model_dir=$WORK/toad/models

# rm -r $model_dir # ATTENTION: deletes all models in the models folder
mkdir -p $model_dir

data_dir=$WORK/toad/data

if [ -z "$2" ]; then
    start=-10
else
    start="$2"
fi

if [ -z "$3" ]; then
    step=1
else
    step="$3"
fi


ms=6400000
fp=0
tp=0

for dataset in "california_housing" "kin8nm"; do
    echo "$dataset"
    mkdir -p $model_dir/${dataset}
    for tree in  1 2 4 8 16 32 63 128 256 512 1024; do 
        for depth in 1 2 4 8; do 
            tp=0
            fp=0
            if "$1" config=train.conf objective=regression metric=rmse train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-default-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            if "$1" config=train.conf objective=regression metric=rmse train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test tinygbdt_forestsize=$ms max_depth=$depth num_trees=$tree output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            for i in $(seq $start $step 15); do
                for j in $(seq $start $step 15); do
                    fp=$(python3 -c "print(float(2**$i))" )
                    tp=$(python3 -c "print(float(2**$j))" )
                    if "$1" config=train.conf objective=regression metric=rmse train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                    if [ $i -eq $start ]; then
                        fp=0
                        "$1" config=train.conf objective=regression metric=rmse train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out;
                    fi
                    if [ $j -eq $start ]; then
                        tp=0
                        "$1" config=train.conf objective=regression metric=rmse train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out;
                    fi
                done
            done
        done
    done
done

fp=0
tp=0

for dataset in "breastcancer" "kr-vs-kp" "covtype" "mushroom"; do 
    echo "$dataset"
    mkdir -p $model_dir/${dataset}
    for tree in  1 2 3 4 5 6 7 8 9 10 15 20 30 40 50 100 200 500 1000; do 
        for depth in 3 5 7; do 
            tp=0
            fp=0
            if "$1" config=train.conf objective=binary metric=auc train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-default-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            if "$1" config=train.conf objective=binary metric=auc train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test tinygbdt_forestsize=$ms max_depth=$depth num_trees=$tree output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
            else
                echo "Training model fp $fp tp $tp failed / not complete"
            fi
            for i in $(seq $start $step 15); do
                for j in $(seq $start $step 15); do
                    fp=$(python3 -c "print(float(2**$i))" )
                    tp=$(python3 -c "print(float(2**$j))" )
                    if "$1" config=train.conf objective=binary metric=auc train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp trees $tree depth $depth complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                    if [ $i -eq $start ]; then
                        fp=0
                        "$1" config=train.conf objective=binary metric=auc train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out;
                    fi
                    if [ $j -eq $start ]; then
                        tp=0
                        "$1" config=train.conf objective=binary metric=auc train_data=$data_dir/${dataset}.train valid_data=$data_dir/${dataset}.test max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=$model_dir/${dataset}/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > $model_dir/${dataset}/data-${dataset}-ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out;
                    fi
          done
          done
      done
    done
done

cd python || exit

pip3 install --user -r requirements.txt

for dataset in "breastcancer" "covtype" "kr-vs-kp" "mushroom" "kin8nm" "california_housing"; do
    python3 evaluate_models.py ${dataset}
done

cd ..
