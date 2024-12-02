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

# cd experiments/python || exit

# TODO Call fetch Data

# TODO adapt when testing is not longer necessary
cd examples/binary_classification || exit

for tree in 1 2 3 5 10 50 100; do
  for depth in 3 5 7; do
    if "../../lightgbm" config=train.conf max_depth=$depth num_trees=$tree tinygbdt_forestsize=50000 tinygbdt_penalty_split=0.9 tinygbdt_penalty_feature=0.8 output_model=Model/tree-${tree}-depth-${depth}-fp-0.9-tp-0.8.txt > Model/tree-${tree}-depth-${depth}-fp-0.9-tp-0.8.out; then
        echo "Training model Tree ${tree} Depth ${depth} complete"
    else
        echo "Training model Tree ${tree} Depth ${depth} failed / not complete"
    fi
  done
done
