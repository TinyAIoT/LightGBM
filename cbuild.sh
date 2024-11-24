#!/bin/bash


cd experiments || exit

ms=64000

for dataset in "covtype"; do
  for i in $(seq -10 1 15); do
      for j in $(seq -10 1 15); do
          for tree in 5 10 15 20 30 40 50 100 200 500 1000 5000 10000 100000; do
              for depth in 3 5 7; do
                fp=$(python3 -c "print(float(2**$i))" )
                tp=$(python3 -c "print(float(2**$j))" )
                if "../lightgbm" config=train.conf train_data=data/${dataset}.libsvm.binary.train valid_data=data/${dataset}.libsvm.binary.test config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > Output/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                    echo "Training model fp $fp tp $tp complete"
                else
                    echo "Training model fp $fp tp $tp failed / not complete"
                fi
              done
          done
      done
  done
 done

cd Model

find ./ -name 'data-covtypems-64000-fp-*' -type f -print0 | xargs -0 mv -t ../data/All/covtype/

cd ../Output

find ./ -name 'data-covtypems-64000-fp-*' -type f -print0 | xargs -0 mv -t ../data/All/covtype/

cd ..

./genData.sh

