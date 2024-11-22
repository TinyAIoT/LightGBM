#!/bin/bash

if cmake -B build -S . -DUSE_CUDA=0 -DUSE_DEBUG=ON; then
    if cmake --build build -j4 --config Release; then
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
rm -rf Model
rm -rf Output
mkdir Model
mkdir Output

#for learning_rate in 0.1; do
#  for trees in 1 2 3; do
#    for depth in 3 5; do
#      echo "setting done ${learning_rate} ${trees} ${depth}"
#      "../lightgbm" config=train.conf num_trees=$trees max_depth=$depth learning_rate=$learning_rate output_model=Model/model_trees${trees}_depth${depth}.txt > Output/train_trees${trees}_depth${depth}.output
#      "../lightgbm" config=predict.conf input_model=Model/model_trees${trees}_depth${depth}.txt > Predict_trees${trees}_depth${depth}.output
#      echo -n "${learning_rate}" >> /Users/ninaherrmann/Research/LightGBM/stats.txt
#    done
#  done
#done

ms=64000
for i in $(seq -10 1 15); do
    for j in $(seq -10 1 15); do
        echo "-${i}-j-${j}"
        fp=$(python3 -c "print(float(2**$i))" )
        tp=$(python3 -c "print(float(2**$j))" )
        #      "../Release/lightgbm" config=train.conf num_trees=$trees max_depth=$depth learning_rate=$learning_rate output_model=Model/model_trees${trees}_depth${depth}.txt > Output/train_trees${trees}_depth${depth}.output

        if "../lightgbm" config=train.conf max_depth=3 num_trees=100 tinygbdt_forestsize=$ms tinygbdt_penalty_split=$tp tinygbdt_penalty_feature=$fp output_model=Model/model.$ms.0.ms.$fp.fp.$tp.tp.grid.txt > Output/train.$ms.0.ms.$fp.fp.$tp.tp.grid.out; then
            echo "Training model fp $fp tp $tp complete"
        else
            echo "Training model fp $fp tp $tp failed / not complete"
            # exit 1
        fi
    done
done
#cd examples/binary_classification || exit
#"../../lightgbm" config=train.conf output_model=model1.txt > train.output
#cd ../..
# python3 plot_model.py
