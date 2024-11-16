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
input_file="train.conf"

for new_number in 5 10 15 20 25 30 35 40 45 50; do
  # Use a temporary file for in-place editing
  sed "s/num_trees = [0-9]*/num_trees = $new_number/" "$input_file" > tmpfile && mv tmpfile "$input_file"
  echo "Replaced num_trees with $new_number in $input_file"
  sed "s/output_model = LightGBM_model[0-9]*.txt/output_model = LightGBM_model$new_number.txt/" "$input_file" > tmpfile && mv tmpfile "$input_file"
  "../lightgbm" config=train.conf > train$new_number.output
done

"../lightgbm" config=predict.conf > predict.output

cd ..
