#!/bin/bash

cd .. || exit

if cmake -B build -S . -DUSE_CUDA=0 -DUSE_DEBUG=ON; then
    if cmake --build build -j4; then
        echo "build complete"
    else
        echo "cmake --build build -j4 failed"
        exit 1
    fi
else
    echo "CMake configuration failed"
    exit 1
fi

cd experiments || exit

ms=64000

for csvfile in data/*.train.csv; do
  trainname="${trainfile#data/}"
  basename="${trainname%.*}"
    for tree in 1 2 3 4 5 6 7 8 9 10 15 20 30 40 50 100 200 500 1000 10000; do
        for depth in 3 5 7; do
            if [[ trainname == *"kin8nm"* ]] || [[ trainname == *"california_housing"* ]]; then
              if "../lightgbm" config=train.conf objective=regression train_data=data/trainname valid_data=data/${basename}.test.csv config=train.conf max_depth=$depth num_trees=$tree output_model=Model/data-${basename}-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}-tree-${tree}-depth-${depth}.out; then
                  echo "Training model fp $fp tp $tp complete"
              else
                  echo "Training model fp $fp tp $tp failed / not complete"
              fi
            else
              if "../lightgbm" config=train.conf objective=binary train_data=data/trainname valid_data=data/${basename}.test.csv config=train.conf max_depth=$depth num_trees=$tree output_model=Model/data-${basename}-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}-tree-${tree}-depth-${depth}.out; then
                  echo "Training model fp $fp tp $tp complete"
              else
                  echo "Training model fp $fp tp $tp failed / not complete"
              fi
            fi
            for i in $(seq -10 1 15); do
                  for j in $(seq -10 1 15); do
                  fp=$(python3 -c "print(float(2**$i))" )
                  tp=$(python3 -c "print(float(2**$j))" )
                  if [[ trainname == *"kin8nm"* ]] || [[ trainname == *"california_housing"* ]]; then
                    if "../lightgbm" config=train.conf objective=regression train_data=data/trainname valid_data=data/${basename}.test.csv config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/data-${basename}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                  else
                    if "../lightgbm" config=train.conf objective=binary train_data=data/trainname valid_data=data/${basename}.test.csv config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/data-${basename}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                  fi
                done
            done
        done
    done
done
for trainfile in data/*.train; do
  trainname="${trainfile#data/}"
  basename="${trainfile%.*}"
  for tree in 1 2 3 4 5 6 7 8 9 10 15 20 30 40 50 100 200 500 1000 10000; do
      for depth in 3 5 7; do
        if [[ trainname == *"kin8nm"* ]] || [[ trainname == *"california_housing"* ]]; then
          if "../lightgbm" config=train.conf objective=regression train_data=data/trainname valid_data=data/${basename}.test.csv config=train.conf max_depth=$depth num_trees=$tree output_model=Model/data-${basename}-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}-tree-${tree}-depth-${depth}.out; then
              echo "Training model fp $fp tp $tp complete"
          else
              echo "Training model fp $fp tp $tp failed / not complete"
          fi
        else
          if "../lightgbm" config=train.conf objective=binary train_data=data/trainname valid_data=data/${basename}.test.csv config=train.conf max_depth=$depth num_trees=$tree output_model=Model/data-${basename}-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}-tree-${tree}-depth-${depth}.out; then
              echo "Training model fp $fp tp $tp complete"
          else
              echo "Training model fp $fp tp $tp failed / not complete"
          fi
        fi
          for i in $(seq -10 1 15); do
                for j in $(seq -10 1 15); do
                  fp=$(python3 -c "print(float(2**$i))" )
                  tp=$(python3 -c "print(float(2**$j))" )
                  if [[ trainname == *"kin8nm"* ]] || [[ trainname == *"california_housing"* ]]; then
                    if "../lightgbm" config=train.conf objective=regression train_data=data/trainname valid_data=data/${basename}.libsvm.test config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/data-${basename}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                  else
                    if "../lightgbm" config=train.conf objective=binary train_data=data/trainname valid_data=data/${basename}.libsvm.test config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/data-${basename}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                        echo "Training model fp $fp tp $tp complete"
                    else
                        echo "Training model fp $fp tp $tp failed / not complete"
                    fi
                  fi
                done
            done
        done
    done
done