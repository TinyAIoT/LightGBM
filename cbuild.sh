#!/bin/bash

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
rm -rf Model
rm -rf Output
mkdir Model
mkdir Output

for learning_rate in 0.1; do
  for trees in 1 2 3; do
    for depth in 3 5; do
      echo "setting done ${learning_rate} ${trees} ${depth}"
      "../lightgbm" config=train.conf num_trees=$trees max_depth=$depth learning_rate=$learning_rate output_model=Model/model_trees${trees}_depth${depth}.txt > Output/train_trees${trees}_depth${depth}.output
      "../lightgbm" config=predict.conf input_model=Model/model_trees${trees}_depth${depth}.txt > Predict/Predict_trees${trees}_depth${depth}.output
      echo -n "${learning_rate}" >> /Users/ninaherrmann/Research/LightGBM/stats.txt
    done
  done
done

cd ..
#cd examples/binary_classification || exit
#"../../lightgbm" config=train.conf output_model=model1.txt > train.output
#cd ../..
# python3 plot_model.py
