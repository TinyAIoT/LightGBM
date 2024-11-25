#!/bin/bash


cd experiments || exit

ms=64000

for dataset in "kin8nm" "california_housing"; do
  for i in $(seq -10 1 15); do
      for j in $(seq -10 1 15); do
          for tree in 5 10 15 20 30 40 50 100 500; do
              for depth in 3; do
                fp=$(python3 -c "print(float(2**$i))" )
                tp=$(python3 -c "print(float(2**$j))" )
                if "../lightgbm" config=train.conf objective=regression train_data=data/${dataset}.libsvm.train valid_data=data/${dataset}.libsvm.test config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.txt > Model/data-${dataset}ms-$ms-fp-$fp-tp-$tp-tree-${tree}-depth-${depth}.out; then
                    echo "Training model fp $fp tp $tp complete"
                else
                    echo "Training model fp $fp tp $tp failed / not complete"
                fi
              done
          done
      done
  done
 done

cd Model || exit

find ./ -name 'data-kin8nmms-64000-fp-*' -type f -print0 | xargs -0 mv -t ../data/All/kin8nm/
find ./ -name 'data-california_housingms-64000-fp-*' -type f -print0 | xargs -0 mv -t ../data/All/california_housing/

cd ..

./genData.sh

